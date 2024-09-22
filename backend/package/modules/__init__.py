__all__ = ["get_engine_modules"]


def get_engine_modules():
    from .ai_api_engine.elevenlabs_tts_engine import ElevenLabs_TTS_Engine
    from .ai_api_engine.piper_tts_engine import Piper_TTS_Engine
    from .script_db_engine.excel_script_db_engine import Excel_Script_DB_Engine

    return {
        "ai_api_engine": {
            "Piper_TTS_Engine": Piper_TTS_Engine,
            "ElevenLabs_TTS_Engine": ElevenLabs_TTS_Engine,
        },
        "script_db_engine": {
            "Excel_Script_DB_Engine": Excel_Script_DB_Engine,
        },
    }
