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

enum class NameKeys {

};
struct Name {

};
inline void from_json(const json& j, Name& s) {
    s.key = j.value("key", "");
}
inline void to_json(json& j, const Name& s) {
    j = json{};
    if (!s.key.empty()) {j["key"]=s.key;}
}


*/


//==============================================================================
/* The AI API Models
*/
enum class VoiceSettingsKeys {
    voice_id, name, settings, description, files, labels
};
struct VoiceSettings {
    std::string voice_id = "";
    std::string name = "";
    json settings = {};
    std::string description = "";
    std::vector<std::string> files = {};
    json labels = {};
};
bool const isEmpty(const VoiceSettings& v) {
    return {
        v.voice_id.empty() &&
        v.name.empty() &&
        v.settings == json{} &&
        v.description.empty() &&
        v.files.size() == 0 &&
        v.labels == json{}
    };
};
inline void from_json(const json& j, VoiceSettings& s) {
    s.voice_id = j.value("voice_id", "");
    s.name = j.value("name", "");
    s.settings = j.value("settings", json{});
    s.description = j.value("description", "");
    if (j.contains("files") && j["files"].is_array()) { s.files = j["files"].get<std::vector<std::string>>(); }
    s.labels = j.value("labels", json{});
}
inline void to_json(json& j, const VoiceSettings& s) {
    j = json{};
    if (!s.voice_id.empty()) { j["voice_id"] = s.voice_id; }
    if (!s.name.empty()) { j["name"] = s.name; }
    if (s.settings != json{}) { j["settings"] = s.settings; }
    if (!s.description.empty()) { j["description"] = s.description; }
    if (s.files.size() > 0) { j["files"] = s.files; }
    if (s.labels != json{}) { j["labels"] = s.labels; }
}

enum class TextToSpeechKeys {
    text, voice, voice_settings, model, seed
};
struct TextToSpeech {
    std::string text = "";
    std::string voice = "";
    VoiceSettings voice_settings = VoiceSettings{};
    std::string model = "";
    int seed = -1;
};
inline void from_json(const json& j, TextToSpeech& s) {
    s.text = j.value("text", "");
    s.voice = j.value("voice", "");
    if (j.contains("voice_settings") && j["voice_settings"].is_object()) { s.voice_settings = j["voice_settings"].get<VoiceSettings>(); }
    s.model = j.value("model", "");
    s.seed = j.value("seed", -1);
}
inline void to_json(json& j, const TextToSpeech& s) {
    j = json{};
    if (!s.text.empty()) { j["text"] = s.text; }
    if (!s.voice.empty()) { j["voice"] = s.voice; }
    if (!isEmpty(s.voice_settings)) { j["voice_settings"] = s.voice_settings; }
    if (!s.model.empty()) { j["model"] = s.model; }
    if (s.seed != -1) { j["seed"] = s.seed; }
}



//==============================================================================
/* The Audio Models
*/ 
enum class AudioFormatKeys {
    codec, sample_rate, channels, bit_depth, bit_rate, normalization_type
};
struct AudioFormat {
    std::string codec = "";
    std::string sample_rate = "";
    std::string channels = "";
    std::string bit_depth = "";
    std::string bit_rate = "";
    std::string normalization_type = "";
};
inline void from_json(const json& j, AudioFormat& s) {
    s.codec = j.value("codec", "");
    s.sample_rate = j.value("sample_rate", "");
    s.channels = j.value("channels", "");
    s.bit_depth = j.value("bit_depth", "");
    s.bit_rate = j.value("bit_rate", "");
    s.normalization_type = j.value("normalization_type", "");
}
inline void to_json(json& j, const AudioFormat& s) {
    j = json{};
    if (!s.codec.empty()) { j["codec"] = s.codec; }
    if (!s.sample_rate.empty()) { j["sample_rate"] = s.sample_rate; }
    if (!s.channels.empty()) { j["channels"] = s.channels; }
    if (!s.bit_depth.empty()) { j["bit_depth"] = s.bit_depth; }
    if (!s.bit_rate.empty()) { j["bit_rate"] = s.bit_rate; }
    if (!s.normalization_type.empty()) { j["normalization_type"] = s.normalization_type; }
}

//==============================================================================
/* The Engine Backend Models
*/

enum class Engine_ModulesKeys {

};
struct Engine_Modules {

};
inline void from_json(const json& j, Name& s) {
    s.key = j.value("key", "");
}
inline void to_json(json& j, const Name& s) {
    j = json{};
    if (!s.key.empty()) { j["key"] = s.key; }
}

//==============================================================================
/* The Script Models
*/
enum class CharacterInfoKeys {
    id, character_name, voice_talent, script_name, number_of_lines, gender
};
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
    j = json{};
    if (!s.id.empty()) { j["id"] = s.id; }
    if (!s.character_name.empty()) { j["character_name"] = s.character_name; }
    if (!s.voice_talent.empty()) { j["voice_talent"] = s.voice_talent; }
    if (!s.script_name.empty()) { j["script_name"] = s.script_name; }
    if (s.number_of_lines != 0) { j["number_of_lines"] = s.number_of_lines; }
    if (!s.gender.empty()) { j["gender"] = s.gender; }
};

enum class ScriptLineKeys {
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
    j = json{};
    if (!s.id.empty()) j["id"] = s.id;
    if (!s.source_text.empty()) j["source_text"] = s.source_text;
    if (!s.translation.empty()) j["translation"] = s.translation;
    if (!s.time_restriction.empty()) j["time_restriction"] = s.time_restriction;
    if (!s.voice_talent.empty()) j["voice_talent"] = s.voice_talent;
    if (!s.character_name.empty()) j["character_name"] = s.character_name;
    if (!s.reference_audio_path.empty()) j["reference_audio_path"] = s.reference_audio_path;
    if (!s.delivery_audio_path.empty()) j["delivery_audio_path"] = s.delivery_audio_path;
    if (!s.generated_audio_path.empty()) j["generated_audio_path"] = s.generated_audio_path;
};

//==============================================================================
/* The Session Models
*/