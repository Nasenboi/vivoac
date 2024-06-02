/*
  ==============================================================================

    v_DataModels.h
    Created: 30 May 2024 12:06:00pm
    Author:  cboen

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>
#include "nlohmann/json.hpp"
using json = nlohmann::json;

//==============================================================================
/* The Data Models for the HTTPClient connection
*/


//==============================================================================
/* The Script Models
*/

struct CharacterInfo {
    std::string id = "";
    std::string character_name = "";
    std::string voice_talent = "";
    std::string script_name = "";
    int number_of_lines = 0;
    std::string gender = "";
};
inline void from_json(const json& j, CharacterInfo& s) {
    s.id = j.value("id", "");
    s.character_name = j.value("character_name", "");
    s.voice_talent = j.value("voice_talent", "");
    s.script_name = j.value("script_name", "");
    s.number_of_lines = j.value("number_of_lines", 0);
    s.gender = j.value("gender", "");
};
inline void to_json(json& j, const CharacterInfo& s) {
    j = json{
        {"id", s.id},
        {"character_name", s.character_name},
        {"voice_talent", s.voice_talent},
        {"script_name", s.script_name},
        {"number_of_lines", s.number_of_lines},
        {"gender", s.gender}
    };
};

enum ScriptLineKeys {
    id, source_text, translation, time_restriction, voice_talent,
    character_name, reference_audio_path, delivery_audio_path,
    generated_audio_path
};
struct ScriptLine {
    std::string id = "";
    std::string source_text = "";
    std::string translation = "";
    std::string time_restriction = "";
    std::string voice_talent = "";
    std::string character_name = "";
    std::string reference_audio_path = "";
    std::string delivery_audio_path = "";
    std::string generated_audio_path = "";
};
inline void from_json(const json& j, ScriptLine& s) {
    s.id = j.value("id", "");
    s.source_text = j.value("source_text", "");
    s.translation = j.value("translation", "");
    s.time_restriction = j.value("time_restriction", "");
    s.voice_talent = j.value("voice_talent", "");
    s.character_name = j.value("character_name", "");
    s.reference_audio_path = j.value("reference_audio_path", "");
    s.delivery_audio_path = j.value("delivery_audio_path", "");
    s.generated_audio_path = j.value("generated_audio_path", "");
};
inline void to_json(json& j, const ScriptLine& s) {
    j = json{
        {"id", s.id},
        {"source_text", s.source_text},
        {"translation", s.translation},
        {"time_restriction", s.time_restriction},
        {"voice_talent", s.voice_talent},
        {"character_name", s.character_name},
        {"reference_audio_path", s.reference_audio_path},
        {"delivery_audio_path", s.delivery_audio_path},
        {"generated_audio_path", s.generated_audio_path}
    };
};

//==============================================================================
/* The Audio Models
*/ 

//==============================================================================
/* The AI API Models
*/

//==============================================================================
/* The Session Models
*/

