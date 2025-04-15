from typing import Literal, cast
from vosk import Model, KaldiRecognizer  # Ensure the 'vosk' library is installed
import wave
import json
from phonemizer import phonemize
from phonemizer.backend import EspeakBackend
import bpy 
import os

from ..LIPSYNC2D_Utils import get_package_name
from ..Core.phoneme_to_viseme import phoneme_to_viseme_arkit_v2 as phoneme_to_viseme

class LIPSYNC2D_OT_AnalyzeAudio(bpy.types.Operator):
    bl_idname = "audio.cgp_analyze_audio"
    bl_label = "Analyze audio"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene is not None or context.active_object is not None

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        prefs = context.preferences.addons[get_package_name()].preferences # type: ignore
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
        
        self.set_backend_library()
        props = obj.lipsync2d_props # type: ignore
        self.based_fps = context.scene.render.fps * context.scene.render.fps_base

        model = Model(lang=prefs.current_lang)  # Ensure vosk library dependency is satisfied (install it via pip)
        result = self.vosk_recognize_voice(file_path, model)
        words_timings = result['result']

        os.remove(file_path) # Need to be removed AFTER vosk_recognize_voice
        
        self.clear_previous_keyframes(obj)
        self.insert_keyframe_on_phoneme(words_timings, obj, props)
        self.set_constant_interpolation(obj)

        return {'FINISHED'}

    def clear_previous_keyframes(self, obj):
        action = obj.animation_data.action if obj.animation_data else None
        if action:
            for fcurve in action.fcurves:
                print(fcurve.data_path)
                if fcurve.data_path == "lipsync2d_props.lip_sync_2d_sprite_sheet_index": 
                    fcurve.keyframe_points.clear()

    def set_constant_interpolation(self, obj):
        action = obj.animation_data.action if obj.animation_data else None

        if action:
            for fcurve in action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'CONSTANT'

    def insert_keyframe_on_phoneme(self, words_timings, obj, props):
        words = [word['word'] for word in words_timings]
        total_words = len(words)
        phonemes = self.extract_phonemes(words)
        
        for index, word_timing in enumerate(words_timings):
            start = word_timing['start']
            end = word_timing['end']

            word_frame_start = self.time_to_frame(start)
            word_frame_end = self.time_to_frame(end)

            phoneme = phonemes[index].strip()
            visemes = [ipaphoneme_to_viseme(p) for p in phoneme]
            visemes_len = len(visemes)
            duration = word_frame_end - word_frame_start
            visemes_parts = duration / len(visemes)
            next_start = words_timings[index + 1]['start'] if index < total_words - 1 else -1
            delay_until_next_word = next_start - word_frame_end / self.based_fps

            for viseme_index, v in enumerate(visemes):
                add_sil_at_word_end = ((delay_until_next_word > .100) and (viseme_index + 1) == visemes_len) or (index == total_words -1)
                viseme_frame_start = word_frame_start + round(viseme_index*visemes_parts)
                
                gindex = props[f"lip_sync_2d_viseme_{v}"]

                if gindex > 9:
                    gindex = 1

                props["lip_sync_2d_sprite_sheet_index"] = gindex
                obj.keyframe_insert("lipsync2d_props.lip_sync_2d_sprite_sheet_index", frame=viseme_frame_start)
                if add_sil_at_word_end:
                    props["lip_sync_2d_sprite_sheet_index"] = props[f"lip_sync_2d_viseme_sil"]
                    obj.keyframe_insert("lipsync2d_props.lip_sync_2d_sprite_sheet_index", frame=word_frame_end)

    def extract_phonemes(self, words):
        phonemes = cast(list[str],phonemize(words, language='fr-fr', backend='espeak', strip=False))
        return phonemes

    def time_to_frame(self, time):
        return round(time * self.based_fps)

    def set_backend_library(self):
        EspeakBackend.set_library("C:\\Program Files\\eSpeak NG\\libespeak-ng.dll")

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
    output_path = "/tmp/cgp_lipsync_extracted_audio.wav"

    bpy.ops.sound.mixdown(
        filepath=output_path,
        container='WAV',
        codec='PCM',
        format='S16',
        mixrate=16000,    # Sample rate for Vosk
        channels='MONO'   # Vosk prefers mono
    )

    return output_path


def ipaphoneme_to_viseme(ipa_phoneme):
    clean = ipa_phoneme.strip("ː̥̬̃012")  # remove length, nasal, stress etc
    return phoneme_to_viseme.get(clean, "UNK")
    
