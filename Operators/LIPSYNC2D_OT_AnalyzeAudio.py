import json
import os
import wave
from typing import Literal, cast

import bpy
from vosk import KaldiRecognizer, Model

from ..Core.Animator.LIPSYNC2D_PoseAssetsAnimator import LIPSYNC2D_PoseAssetsAnimator

from ..Core.Animator.LIPSYNC2D_ShapeKeysAnimator import LIPSYNC2D_ShapeKeysAnimator
from ..Core.Animator.LIPSYNC_SpriteSheetAnimator import LIPSYNC_SpriteSheetAnimator
from ..Core.Animator.protocols import LIPSYNC2D_LipSyncAnimator
from ..Core.LIPSYNC2D_DialogInspector import LIPSYNC2D_DialogInspector
from ..Core.LIPSYNC2D_VoskHelper import LIPSYNC2D_VoskHelper
from ..Core.Timeline.LIPSYNC2D_Timeline import LIPSYNC2D_Timeline
from ..LIPSYNC2D_Utils import get_package_name
from ..lipsync_types import BpyObject


class LIPSYNC2D_OT_AnalyzeAudio(bpy.types.Operator):
    bl_idname = "sound.cgp_analyze_audio"
    bl_label = "Bake audio"
    bl_description = "Analyze audio and insert Keyframes on detected phonemes"
    bl_options = {"REGISTER", "UNDO"}

    animator: LIPSYNC2D_LipSyncAnimator

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.animator: LIPSYNC2D_LipSyncAnimator

    @classmethod
    def poll(cls, context):
        if context.active_object is None:
            return False

        animator = LIPSYNC2D_OT_AnalyzeAudio.get_animator(context.active_object)
        return animator.poll(cls, context)

    def execute(
        self, context: bpy.types.Context
    ) -> set[
        Literal["RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"]
    ]:
        prefs = context.preferences.addons[get_package_name()].preferences  # type: ignore
        obj = context.active_object

        if (
            context.scene is None
            or obj is None
            or context.scene.sequence_editor is None
        ):
            self.report(type={"ERROR"}, message="No Sequence Editor found")
            return {"CANCELLED"}

        all_strips = context.scene.sequence_editor.strips_all
        has_sound = any(strip.type == "SOUND" for strip in all_strips)

        if not has_sound:
            self.report(type={"ERROR"}, message="No sound detected in Sequence Editor")
            return {"CANCELLED"}

        self.set_bake_range()
        file_path = extract_audio()

        if not os.path.isfile(f"{file_path}"):
            self.report(
                type={"ERROR"},
                message="Error while importing extracted audio WAV file from /tmp",
            )
            self.reset_bake_range()
            return {"CANCELLED"}

        model = self.get_model(prefs)
        result = self.vosk_recognize_voice(file_path, model)

        if "result" not in result:
            self.reset_bake_range()
            os.remove(file_path)  # Need to be removed AFTER vosk_recognize_voice
            return {"FINISHED"}

        recognized_words = result["result"]

        os.remove(file_path)  # Need to be removed AFTER vosk_recognize_voice

        dialog_inspector = LIPSYNC2D_DialogInspector(context.scene.render)
        words = [word["word"] for word in recognized_words]
        total_words = len(words)
        phonemes = LIPSYNC2D_DialogInspector.extract_phonemes(words, context)

        auto_obj = self.get_animator(obj)
        props = obj.lipsync2d_props  # type: ignore
        debug_entries = [] if props.lip_sync_2d_debug_output else None

        auto_obj.setup(obj)
        self.auto_insert_keyframes(
            auto_obj, obj, recognized_words, dialog_inspector, total_words, phonemes, debug_entries
        )
        auto_obj.set_interpolation(obj)
        auto_obj.cleanup(obj)
        self.reset_bake_range()

        if debug_entries is not None:
            self.write_debug_output(debug_entries)

        if bpy.context.view_layer:
            bpy.context.view_layer.update()

        self.report(
            {"INFO"}, message=f"{auto_obj.inserted_keyframes} keyframes inserted"
        )

        return {"FINISHED"}

    def auto_insert_keyframes(
        self,
        auto_obj: LIPSYNC2D_LipSyncAnimator,
        obj: BpyObject,
        recognized_words,
        dialog_inspector: LIPSYNC2D_DialogInspector,
        total_words,
        phonemes,
        debug_entries: list | None = None,
    ):
        props = obj.lipsync2d_props  # type: ignore
        words = enumerate(recognized_words)

        for index, recognized_word in words:
            is_last_word = index == total_words - 1
            word_timing = dialog_inspector.get_word_timing(recognized_word)
            current_phonemes = phonemes[index]
            visemes_data = dialog_inspector.get_visemes(
                current_phonemes, word_timing["duration"]
            )
            
            if debug_entries is not None:
                debug_entries.append({
                    "word": recognized_word["word"],
                    "phonemes": current_phonemes,
                    "visemes": visemes_data,
                    "start": word_timing["word_frame_start"],
                })

            next_word_timing = dialog_inspector.get_next_word_timing(
                recognized_words, index
            )

            # Last viseme is inserted a bit before end of word.
            # This ensures that delay_until_next_word uses correct timing
            corrected_word_end_frame = (
                LIPSYNC2D_ShapeKeysAnimator.get_corrected_end_frame(
                    word_timing["word_frame_start"], visemes_data
                )
            )
            delay_until_next_word = (
                next_word_timing["word_frame_start"] - corrected_word_end_frame
            )

            auto_obj.insert_keyframes(
                obj,
                props,
                visemes_data,
                word_timing,
                delay_until_next_word,
                is_last_word,
                index,
            )

    def write_debug_output(self, entries):
        text_name = "LipSync Debug"
        text = bpy.data.texts.get(text_name)
        if text is None:
            text = bpy.data.texts.new(text_name)
        else:
            text.clear()

        # Header
        output = [
            f"{'Word':<15} {'Start':<10} {'Phonemes':<15} {'Viseme':<10} {'Frame':<10}",
            "-" * 60
        ]

        for entry in entries:
            word = entry['word']
            start_frame = entry['start']
            phonemes = entry['phonemes']  # list of phonemes strings
            phonemes_str = " ".join(phonemes)
            
            viseme_data = entry['visemes']
            visemes_list = viseme_data['visemes']
            part_duration = viseme_data['visemes_parts']
            
            # First line with word info
            first_viseme = visemes_list[0] if visemes_list else ""
            first_viseme_frame = f"{start_frame:.2f}"
            
            # If no visemes, just print word info
            if not visemes_list:
                output.append(f"{word:<15} {start_frame:<10} {phonemes_str:<15}")
                continue

            # Print first viseme with word info
            output.append(f"{word:<15} {start_frame:<10} {phonemes_str:<15} {visemes_list[0]:<10} {first_viseme_frame:<10}")

            # Print remaining visemes
            current_frame = start_frame
            for i in range(1, len(visemes_list)):
                current_frame += part_duration
                viseme = visemes_list[i]
                output.append(f"{'':<15} {'':<10} {'':<15} {viseme:<10} {current_frame:.2f}")
            
            # Add a separator blank line or just spacing
            # output.append("") 
                
        text.write("\n".join(output))

    @staticmethod
    def get_animator(obj: BpyObject) -> LIPSYNC2D_LipSyncAnimator:
        props = obj.lipsync2d_props  # type: ignore
        type = props.lip_sync_2d_lips_type

        automations = {
            "SPRITESHEET": LIPSYNC_SpriteSheetAnimator,
            "SHAPEKEYS": LIPSYNC2D_ShapeKeysAnimator,
            "POSEASSETS": LIPSYNC2D_PoseAssetsAnimator,
        }

        return automations[type]()

    @LIPSYNC2D_VoskHelper.setextensionpath
    def get_model(self, prefs):
        model = Model(lang=prefs.current_lang)
        return model

    def vosk_recognize_voice(self, file_path: str, model: Model):
        with wave.open(file_path, "rb") as wf:
            # Check audio format
            if (
                wf.getnchannels() != 1
                or wf.getsampwidth() != 2
                or wf.getcomptype() != "NONE"
            ):
                raise ValueError("Audio file must be WAV format mono PCM.")

            # Setup recognizer
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)

            # Read and process audio
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    pass
            result = json.loads(rec.FinalResult())
        return result

    def set_bake_range(self) -> None:
        if bpy.context.scene is None:
            return

        props = bpy.context.active_object.lipsync2d_props  # type: ignore
        bake_start = props.lip_sync_2d_bake_start
        bake_end = props.lip_sync_2d_bake_end
        use_bake_range = props.lip_sync_2d_use_bake_range

        if not use_bake_range:
            return

        self.frame_start = LIPSYNC2D_Timeline.get_frame_start()
        self.frame_end = LIPSYNC2D_Timeline.get_frame_end()

        bpy.context.scene.frame_start = max(0, bake_start)
        # Bake end should never be lower than bake start
        bpy.context.scene.frame_end = max(bake_start, bake_end)

    def reset_bake_range(self) -> None:
        if bpy.context.scene is None:
            return
        props = bpy.context.active_object.lipsync2d_props  # type: ignore
        use_bake_range = props.lip_sync_2d_use_bake_range

        if not use_bake_range:
            return

        bpy.context.scene.frame_start = self.frame_start
        bpy.context.scene.frame_end = self.frame_end


def extract_audio():
    package_name = cast(str, get_package_name())
    output_path = bpy.utils.extension_path_user(package_name, path="tmp", create=True)
    filepath = os.path.join(output_path, "cgp_lipsync_extracted_audio.wav")

    bpy.ops.sound.mixdown(
        filepath=filepath,
        check_existing=False,
        container="WAV",
        codec="PCM",
        format="S16",
        mixrate=16000,  # Sample rate for Vosk
        channels="MONO",  # Vosk prefers mono
    )

    return filepath
