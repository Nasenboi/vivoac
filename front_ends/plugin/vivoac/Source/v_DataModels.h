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
inline bool const isEmpty(const VoiceSettings& s) {
    return {
        s.voice_id.empty() &&
        s.name.empty() &&
        s.settings == json{} &&
        s.description.empty() &&
        s.files.size() == 0 &&
        s.labels == json{}
    };
};
inline void from_json(const json& j, VoiceSettings& s) {
    if (j.contains("voice_id") && j["voice_id"].is_string()) { s.voice_id = j["voice_id"]; }
    if (j.contains("name") && j["name"].is_string()) { s.name = j["name"]; }
    if (j.contains("settings") && j["settings"].is_object()) { s.settings = j["settings"]; }
    if (j.contains("description") && j["description"].is_string()) { s.description = j["description"]; }
    if (j.contains("files") && j["files"].is_array()) { s.files = j["files"].get<std::vector<std::string>>(); }
    if (j.contains("labels") && j["labels"].is_object()) { s.labels = j["labels"]; }
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
inline bool isEmpty(const TextToSpeech& s) {
    return {
        s.text.empty() &&
        s.voice.empty() &&
        s.model.empty() &&
        s.seed == -1 &&
        isEmpty(s.voice_settings)
    };
}
inline void from_json(const json& j, TextToSpeech& s) {
    if (j.contains("text") && j["text"].is_string()) { s.text = j["text"]; }
    if (j.contains("voice") && j["voice"].is_string()) { s.voice = j["voice"]; }
    if (j.contains("voice_settings") && j["voice_settings"].is_object()) { s.voice_settings = j["voice_settings"].get<VoiceSettings>(); }
    if (j.contains("model") && j["model"].is_string()) { s.model = j["model"]; }
    if (j.contains("seed") && j["seed"].is_number_integer()) { s.seed = j["seed"]; }
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
    int sample_rate = -1;
    int channels = -1;
    std::string bit_depth = "";
    std::string bit_rate = "";
    std::string normalization_type = "";
};
inline bool const isEmpty(const AudioFormat& s) {
    return {
        s.codec.empty() &&
        s.sample_rate == -1 &&
        s.channels == -1 &&
        s.bit_depth.empty() &&
        s.bit_rate.empty() &&
        s.normalization_type.empty()
    };
};
inline void from_json(const json& j, AudioFormat& s) {
    if (j.contains("codec") && j["codec"].is_string()) { s.codec = j["codec"]; }
	if (j.contains("sample_rate") && j["sample_rate"].is_number_integer()) { s.sample_rate = j["sample_rate"]; }
	if (j.contains("channels") && j["channels"].is_number_integer()) { s.channels = j["channels"]; }
	if (j.contains("bit_depth") && j["bit_depth"].is_string()) { s.bit_depth = j["bit_depth"]; }
	if (j.contains("bit_rate") && j["bit_rate"].is_string()) { s.bit_rate = j["bit_rate"]; }
	if (j.contains("normalization_type") && j["normalization_type"].is_string()) { s.normalization_type = j["normalization_type"]; }    
}
inline void to_json(json& j, const AudioFormat& s) {
    j = json{};
    if (!s.codec.empty()) { j["codec"] = s.codec; }
    if (s.sample_rate != -1) { j["sample_rate"] = s.sample_rate; }
    if (s.channels != -1) { j["channels"] = s.channels; }
    if (!s.bit_depth.empty()) { j["bit_depth"] = s.bit_depth; }
    if (!s.bit_rate.empty()) { j["bit_rate"] = s.bit_rate; }
    if (!s.normalization_type.empty()) { j["normalization_type"] = s.normalization_type; }
}

//==============================================================================
/* The Engine Backend Models
*/

enum class EngineModulesKeys {
    ai_api_engine_module, audio_file_engine_module, script_db_engine_module
};
struct EngineModules {
    std::string ai_api_engine_module = "";
    std::string audio_file_engine_module = "";
    std::string script_db_engine_module = "";
};
inline bool isEmpty(const EngineModules& s) {
    return {
        s.ai_api_engine_module.empty() &&
        s.audio_file_engine_module.empty() &&
        s.script_db_engine_module.empty()
    };
}
inline void from_json(const json& j, EngineModules& s) {
    if (j.contains("ai_api_engine_module") && j["ai_api_engine_module"].is_string()) { s.ai_api_engine_module = j["ai_api_engine_module"]; }
    if (j.contains("audio_file_engine_module") && j["audio_file_engine_module"].is_string()) { s.audio_file_engine_module = j["audio_file_engine_module"]; }
    if (j.contains("script_db_engine_module") && j["script_db_engine_module"].is_string()) { s.script_db_engine_module = j["script_db_engine_module"]; }
}
inline void to_json(json& j, const EngineModules& s) {
    j = json{};
    if (!s.ai_api_engine_module.empty()) { j["ai_api_engine_module"] = s.ai_api_engine_module; }
    if (!s.audio_file_engine_module.empty()) { j["audio_file_engine_module"] = s.audio_file_engine_module; }
    if (!s.script_db_engine_module.empty()) { j["script_db_engine_module"] = s.script_db_engine_module; }
}
const struct PossibleEngineModules {
    const std::array<std::string, 2> ai_api_engine_modules {
        "AI_API_Engine", "Piper_TTS_Engine"
    };
    const std::array<std::string, 1> audio_file_engine_modules {
        "Audio_File_Engine"
    };
    const std::array<std::string, 2> script_db_engine_modules {
        "Script_DB_Engine", "Excel_Script_DB_Engine"
    };
};

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
    int number_of_lines = -1;
    std::string gender = "";
};
inline void from_json(const json& j, CharacterInfo& s) {
    if (j.contains("id") && j["id"].is_string()) { s.id = j["id"]; }
    if (j.contains("character_name") && j["character_name"].is_string()) { s.character_name = j["character_name"]; }
    if (j.contains("voice_talent") && j["voice_talent"].is_string()) { s.voice_talent = j["voice_talent"]; }
    if (j.contains("script_name") && j["script_name"].is_string()) { s.script_name = j["script_name"]; }
    if (j.contains("gender") && j["gender"].is_string()) { s.gender = j["gender"]; }
    if (j.contains("number_of_lines") && j["number_of_lines"].is_number_integer()) { s.number_of_lines = j["number_of_lines"]; }
};
inline void to_json(json& j, const CharacterInfo& s) {
    j = json{};
    if (!s.id.empty()) { j["id"] = s.id; }
    if (!s.character_name.empty()) { j["character_name"] = s.character_name; }
    if (!s.voice_talent.empty()) { j["voice_talent"] = s.voice_talent; }
    if (!s.script_name.empty()) { j["script_name"] = s.script_name; }
    if (s.number_of_lines != -1) { j["number_of_lines"] = s.number_of_lines; }
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
inline bool isEmpty(const ScriptLine& s) {
	return {
		s.id.empty() &&
		s.source_text.empty() &&
		s.translation.empty() &&
		s.time_restriction.empty() &&
		s.voice_talent.empty() &&
		s.character_name.empty() &&
		s.reference_audio_path.empty() &&
		s.delivery_audio_path.empty() &&
		s.generated_audio_path.empty()
	};
}
inline void from_json(const json& j, ScriptLine& s) {
    DBG(j.dump(4));
    if (j.contains("id") && j["id"].is_string()) { s.id = j["id"]; }
    else if (j.contains("id") && j["id"].is_number()) { s.id = std::string(j["id"]); }
	if (j.contains("source_text") && j["source_text"].is_string()) { s.source_text = j["source_text"]; }
	if (j.contains("translation") && j["translation"].is_string()) { s.translation = j["translation"]; }
	if (j.contains("time_restriction") && j["time_restriction"].is_string()) { s.time_restriction = j["time_restriction"]; }
	if (j.contains("voice_talent") && j["voice_talent"].is_string()) { s.voice_talent = j["voice_talent"]; }
	if (j.contains("character_name") && j["character_name"].is_string()) { s.character_name = j["character_name"]; }
	if (j.contains("reference_audio_path") && j["reference_audio_path"].is_string()) { s.reference_audio_path = j["reference_audio_path"]; }
	if (j.contains("delivery_audio_path") && j["delivery_audio_path"].is_string()) { s.delivery_audio_path = j["delivery_audio_path"]; }
	if (j.contains("generated_audio_path") && j["generated_audio_path"].is_string()) { s.generated_audio_path = j["generated_audio_path"]; }
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

enum class SessionSettingsKeys {
    audio_format
};
struct SessionSettings {
    AudioFormat audio_format = AudioFormat{};
};
inline bool const isEmpty(const SessionSettings& s) {
    return {
        isEmpty(s.audio_format)
    };
};
inline void from_json(const json& j, SessionSettings& s) {
    if (j.contains("audio_format") && j["audio_format"].is_object()) { s.audio_format = j["audio_format"].get<AudioFormat>(); }
}
inline void to_json(json& j, const SessionSettings& s) {
    j = json{};
    if (!isEmpty(s.audio_format)) { j["audio_format"] = s.audio_format; }
}

//==============================================================================
/* The Settings Models
*/

enum class PluginSettingsKeys {
    textToSpeech, engineModules, sessionSettings, generatedAudioPath, url, port, api_key
};
struct PluginSettings {
    TextToSpeech textToSpeech = TextToSpeech{};
    EngineModules engineModules = EngineModules{};
    SessionSettings sessionSettings = SessionSettings{};
    json aiApiEngineSettings = {};
    json audioFileEngineSettings = {};
    json scriptDbEngineSettings = {};

    std::string generatedAudioPath = "";
    std::string url = "";
    std::string port = "";
    std::string api_key = "";
};
inline void from_json(const json& j, PluginSettings& s) {
    if (j.contains("textToSpeech") && j["textToSpeech"].is_object()) { s.textToSpeech = j["textToSpeech"].get<TextToSpeech>(); }
    if (j.contains("engineModules") && j["engineModules"].is_object()) { s.engineModules = j["engineModules"].get<EngineModules>(); }
    if (j.contains("sessionSettings") && j["sessionSettings"].is_object()) { s.sessionSettings = j["sessionSettings"].get<SessionSettings>(); }
    if (j.contains("aiApiEngineSettings") && j["aiApiEngineSettings"].is_object()) { s.aiApiEngineSettings = j["aiApiEngineSettings"]; }
    if (j.contains("audioFileEngineSettings") && j["audioFileEngineSettings"].is_object()) { s.audioFileEngineSettings = j["audioFileEngineSettings"]; }
    if (j.contains("scriptDbEngineSettings") && j["scriptDbEngineSettings"].is_object()) { s.scriptDbEngineSettings = j["scriptDbEngineSettings"]; }
    if (j.contains("generatedAudioPath")) { s.generatedAudioPath = j["generated_audio_path"]; };
    if (j.contains("url")) { s.url = j["url"]; };
    if (j.contains("port")) { s.port = j["port"]; };
    if (j.contains("api_key")) { s.api_key = j["api_key"]; };
}
inline void to_json(json& j, const PluginSettings& s) {
    j = json{};
    if (!isEmpty(s.textToSpeech)) { j["textToSpeech"] = s.textToSpeech; }
    if (!isEmpty(s.engineModules)) { j["engineModules"] = s.engineModules; }
    if (!isEmpty(s.sessionSettings)) { j["sessionSettings"] = s.sessionSettings; }
    if (!s.aiApiEngineSettings.empty()) { j["aiApiEngineSettings"] = s.aiApiEngineSettings; }
    if (!s.audioFileEngineSettings.empty()) { j["audioFileEngineSettings"] = s.audioFileEngineSettings; }
    if (!s.scriptDbEngineSettings.empty()) { j["scriptDbEngineSettings"] = s.scriptDbEngineSettings; }
    if (!s.url.empty()) j["url"] = s.url;
    if (!s.port.empty()) j["port"] = s.port;
    if (!s.api_key.empty()) j["api_key"] = s.api_key;
}