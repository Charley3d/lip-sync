import time
import json
import os
import tracemalloc
import wave
from typing import Literal, cast

import bpy
from vosk import KaldiRecognizer, Model

from ..Core.Animator.LIPSYNC2D_ShapeKeysAnimator import LIPSYNC2D_ShapeKeysAnimator
from ..Core.Animator.LIPSYNC_SpriteSheetAnimator import LIPSYNC_SpriteSheetAnimator
from ..Core.Animator.protocols import LIPSYNC2D_LipSyncAnimator
from ..Core.LIPSYNC2D_DialogInspector import LIPSYNC2D_DialogInspector
from ..Core.LIPSYNC2D_VoskHelper import LIPSYNC2D_VoskHelper
from ..LIPSYNC2D_Utils import get_package_name
from ..lipsync_types import BpyObject, BpyShapeKey


class LIPSYNC2D_OT_AnalyzeAudio(bpy.types.Operator):
    bl_idname = "sound.cgp_analyze_audio"
    bl_label = "Analyze audio"
    bl_options = {'REGISTER', 'UNDO'}

    animator: LIPSYNC2D_LipSyncAnimator

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.animator: LIPSYNC2D_LipSyncAnimator

    @classmethod
    def poll(cls, context):
        if context.active_object is None:
            return False

        animator = LIPSYNC2D_OT_AnalyzeAudio.get_animator(context.active_object)
        return True # animator.poll(cls, context)

    def execute(self, context: bpy.types.Context) -> set[
        Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        prefs = context.preferences.addons[get_package_name()].preferences  # type: ignore
        obj = context.active_object

        if context.scene is None or obj is None or context.scene.sequence_editor is None:
            self.report(type={'ERROR'}, message="No Sequence Editor found")
            return {'CANCELLED'}

        all_strips = context.scene.sequence_editor.strips_all
        has_sound = any(strip.type == 'SOUND' for strip in all_strips)

        if not has_sound:
            self.report(type={'ERROR'}, message="No sound detected in Sequence Editor")
            return {'CANCELLED'}

        file_path = extract_audio()

        if not os.path.isfile(f"{file_path}"):
            self.report(type={'ERROR'}, message="Error while importing extracted audio WAV file from /tmp")
            return {'CANCELLED'}

        model = self.get_model(prefs)
        result = self.vosk_recognize_voice(file_path, model)

        if "result" not in result:
            return {'FINISHED'}

        recognized_words = result['result']

        os.remove(file_path)  # Need to be removed AFTER vosk_recognize_voice

        dialog_inspector = LIPSYNC2D_DialogInspector(context.scene.render)
        words = [word['word'] for word in recognized_words]
        total_words = len(words)
        phonemes = LIPSYNC2D_DialogInspector.extract_phonemes(words, context)


        auto_obj = self.get_animator(obj)
        start_total = time.time()
        
        start = time.time()
        auto_obj.setup(obj)
        end = time.time()
        print(f"Setup: {end - start:.9f}seconds")
        # auto_obj.clear_previous_keyframes(obj)

        tracemalloc.start()
        start = time.time()
        self.auto_insert_keyframes(auto_obj, obj, recognized_words, dialog_inspector, total_words, phonemes)
        end = time.time()
        print(f"auto_insert_keyframes: {end - start:.9f}seconds")
        # Show memory stats
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Current memory usage: {current / 1024:.2f} KB")
        print(f"Peak memory usage: {peak / 1024:.2f} KB")

        start = time.time()
        auto_obj.set_interpolation(obj)
        end = time.time()
        print(f"set_interpolation: {end - start:.9f}seconds")

        start = time.time()
        # auto_obj.cleanup(obj)
        end = time.time()
        print(f"cleanup: {end - start:.9f}seconds")

        end = time.time()
        print(f"Total: {end - start_total:.9f}seconds")

        print(auto_obj.inserted_keyframes)
        self.report({"INFO"}, message=f"{auto_obj.inserted_keyframes} keyframes inserted")

        return {'FINISHED'}

    def auto_insert_keyframes(self, auto_obj: LIPSYNC2D_LipSyncAnimator, obj: BpyObject, recognized_words,
                              dialog_inspector: LIPSYNC2D_DialogInspector, total_words, phonemes):
        props = obj.lipsync2d_props  # type: ignore
        words = enumerate(recognized_words)

        for index, recognized_word in words:
            is_last_word = (index == total_words - 1)
            word_timing = dialog_inspector.get_word_timing(recognized_word)
            visemes_data = dialog_inspector.get_visemes(phonemes[index], word_timing["duration"])
            next_word_timing = dialog_inspector.get_next_word_timing(recognized_words, index)

            # Last viseme is inserted a bit before end of word. 
            # This ensures that delay_until_next_word uses correct timing
            corrected_word_end_frame = LIPSYNC2D_ShapeKeysAnimator.get_corrected_end_frame(word_timing["word_frame_start"], visemes_data)
            delay_until_next_word = next_word_timing["word_frame_start"] - corrected_word_end_frame

            auto_obj.insert_keyframes(obj, props, visemes_data, word_timing, delay_until_next_word, is_last_word, index)


    @staticmethod
    def get_animator(obj: BpyObject) -> LIPSYNC2D_LipSyncAnimator:
        props = obj.lipsync2d_props  # type: ignore
        type = props.lip_sync_2d_lips_type

        automations = {
            "SPRITESHEET": LIPSYNC_SpriteSheetAnimator,
            "SHAPEKEYS": LIPSYNC2D_ShapeKeysAnimator
        }

        return automations[type]()

    @LIPSYNC2D_VoskHelper.setextensionpath
    def get_model(self, prefs):
        model = Model(lang=prefs.current_lang)
        return model 

    def vosk_recognize_voice(self, file_path: str, model: Model):
        with wave.open(file_path, "rb") as wf:
            # Check audio format
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
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


def extract_audio():
    package_name = cast(str, get_package_name())
    output_path = bpy.utils.extension_path_user(package_name, path="tmp", create=True)
    filepath = os.path.join(output_path, "cgp_lipsync_extracted_audio.wav")

    bpy.ops.sound.mixdown(
        filepath=filepath,
        check_existing=False,
        container='WAV',
        codec='PCM',
        format='S16',
        mixrate=16000,  # Sample rate for Vosk
        channels='MONO'  # Vosk prefers mono
    )

    return filepath
