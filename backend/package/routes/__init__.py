__all__ = [
    "get_api_routes",
]


def get_api_routes():
    from .ai_api_handler.routes import AI_API_Handler_Router
    from .engine_backend.routes import Engine_Router
    from .script.routes import Script_Router
    from .user.routes import User_Router
    from .voice_talent.routes import Voice_Talent_Router

    return [
        AI_API_Handler_Router,
        Engine_Router,
        Script_Router,
        User_Router,
        Voice_Talent_Router,
    ]
