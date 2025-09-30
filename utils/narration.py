import pyttsx3
from gtts import gTTS
import os
import pygame
import tempfile

def narrate_result(result, confidence_yes, confidence_no, name=None, language="English", gender="Male"):
    """
    Narrates the predicted result of cancer recurrence using text-to-speech (TTS).

    This function generates a spoken narration of recurrence prediction results 
    based on model output, confidence scores, patient information, and user preferences.
    Narration is available in English (via `pyttsx3`) and Hindi (via `gTTS` + `pygame`).

    Parameters
    ----------
    result : str

    name : str, optional

    Behavior
    --------
    - Constructs a summary message including the patient name (if provided) and 
      recurrence confidence percentage.
    - Interprets the `result` string to provide one of:
        * "Recurrence is likely."
        * "Recurrence is borderline. Please consider further testing and specialist evaluation."
        * "No recurrence expected."
    - Narrates the constructed message in the selected language and voice.

    Exceptions
    ----------
    Prints an error message if narration fails due to missing dependencies,
    audio device issues, or unsupported configurations.

    """
    try:
        summary = f"Prediction for {name}. Confidence of recurrence is {confidence_yes * 100:.1f} percent." if name else "Prediction completed."

        if "likely" in result.lower():
            result_msg = "Recurrence is likely."
        elif "borderline" in result.lower():
            result_msg = "Recurrence is borderline. Please consider further testing and specialist evaluation."
        else:
            result_msg = "No recurrence expected."

        full_text_en = f"{summary}. {result_msg}"
        full_text_hi = f"{name} के लिए अनुमान। कैंसर की पुनरावृत्ति की संभावना {confidence_yes * 100:.1f} प्रतिशत है। परिणाम: {translate_result(result)}"

        if language == "English":
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')

            voice_map = {
                "Male": 0, 
                "Female": 1 
            }
            selected_voice = voices[voice_map.get(gender, 0)].id
            engine.setProperty('voice', selected_voice)
            engine.setProperty('rate', 160)

            engine.say(full_text_en)
            engine.runAndWait()

        elif language == "Hindi":
            tts = gTTS(text=full_text_hi, lang='hi')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                audio_path = fp.name

            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove(audio_path)

    except Exception as e:
        print("Narration error:", e)


def translate_result(result):
    if "likely" in result.lower():
        return "कैंसर की पुनरावृत्ति की संभावना है"
    elif "borderline" in result.lower():
        return "कैंसर की अनिश्चितता का मामला, कृपया आगे के परीक्षण और विशेषज्ञ मूल्यांकन पर विचार करें"
    else:
        return "कैंसर की पुनरावृत्ति की संभावना नहीं है"
