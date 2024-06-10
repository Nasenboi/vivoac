/*
  ==============================================================================

    v_HTTPClient.cpp
    Created: 29 May 2024 2:20:21pm
    Author:  cboen

  ==============================================================================
*/

#include <curl/curl.h>
#include "v_HTTPClient.h"
#include "nlohmann/json.hpp"

/*
    DBG("---------------------------");

    CURL* curl;
    CURLcode res;
    std::string url = "file://C:/Users/cboen/Documents/Programmierungen/GitStuff/vivoac/project-settings.json";
    std::string readBuffer;

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);

        if (res != CURLE_OK) {
            DBG("curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }
        else {
            try {
                json jsonObject = json::parse(readBuffer);
                DBG(jsonObject.dump(4));
            }
            catch (json::parse_error& e) {
                DBG("JSON parse error: " << e.what());
            }
        }
    }
    else {
        DBG("Failed to initialize CURL.");
    }
    DBG("---------------------------");
*/

using json = nlohmann::json;

HTTPClient::HTTPClient() {
    loadPluginSettings();
};

HTTPClient::~HTTPClient() {
    savePluginSettings();
};

//==============================================================================
/* 
*/
void HTTPClient::parameterChanged(const juce::String& parameterID, float newValue) {
    
};

//==============================================================================
/* Actual API Functions
*/

// == Session functions ==

void HTTPClient::initSession() {
    CURLcode res = doCurl("/session/create", HTTPMethod::Put);

    if (res != CURLE_OK) {
        DBG("curl_easy_perform() failed: \n" << curl_easy_strerror(res));
        return;
    }
    json j;
    try {
        j = json::parse(readBuffer);
        DBG(j.dump(4));
        sessionID = j.value("session_id", "");
    }
    catch (json::parse_error& e) {
        DBG("JSON parse error: " << e.what());
        sessionID = "";
    }
};

void HTTPClient::closeSession() {
    if (sessionID.empty()) return;
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));

    CURLcode res = doCurl("/session/close", HTTPMethod::Post, headers);
    if (res != CURLE_OK) {
        DBG("curl_easy_perform() failed: \n" << curl_easy_strerror(res));
        return;
    }
    json j;
    try {
        j = json::parse(readBuffer);
        DBG(j.dump(4));
        sessionID = "";
    }
    catch (json::parse_error& e) {
        DBG("JSON parse error: " << e.what());
        sessionID = "";
    }
}

void HTTPClient::reload() {
    closeSession();
    initSession();
}

// == Script functions ==

void HTTPClient::getScriptLines() {
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    json body = {};
    body["script_line"] = currentScriptLine;

    DBG("--------------------------------");
    CURLcode res = doCurl("/script/get", HTTPMethod::Post, headers, body);
    
    if (res != CURLE_OK) {
        DBG("curl_easy_perform() failed: \n" << curl_easy_strerror(res));
        return;
    }
    json j;
    try {
        j = json::parse(readBuffer);
        DBG(j.dump(4));
    }
    catch (json::parse_error& e) {
        DBG("JSON parse error: " << e.what());
    }
    DBG("-------------------------------");
};

// == Audio functions ==

// == ai api functions ==

// == Engine Functions == 
int HTTPClient::getEngineId(EngineModulesKeys key) {
    switch (key) {
    case EngineModulesKeys::ai_api_engine_module_index:
        return abs(engineModules.ai_api_engine_module_index);
        break;
    case EngineModulesKeys::audio_file_engine_module_index:
        return abs(engineModules.audio_file_engine_module_index);
        break;
    case EngineModulesKeys::script_db_engine_module_index:
        return abs(engineModules.script_db_engine_module_index);
        break;
    }
}

//==============================================================================
/* Class functionality
*/
CURLcode HTTPClient::doCurl(const std::string& path, const HTTPMethod& method,
    const HEADER_PARAMS header_params, json body_params) {
    CURLcode res;
    CURL* curl;

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();

    // Set headers if any
    struct curl_slist* headers;
    headers = NULL;
    for (const auto& h : header_params) {
        std::string headerString = h.first + ": " + h.second;
        headers = curl_slist_append(headers, headerString.c_str());
    }
    if (!body_params.empty()) {
        headers = curl_slist_append(headers, "Content-Type: application/json");
    }

    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    readBuffer.clear();

    auto curlURL = constructURL(path);
    if (curlURL.empty()) return CURLE_FAILED_INIT;

    curl_easy_setopt(curl, CURLOPT_URL, curlURL.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

    switch (method) {
    case HTTPMethod::Put:
        curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PUT");
        break;
    case HTTPMethod::Post:
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
        break;
    case HTTPMethod::Delete:
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "DELETE");
        break;
    case HTTPMethod::Get:
        curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "GET");
        break;
    };

    // Set body if it exists
    if (!body_params.is_null()) {
        curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "curl/7.38.0");
        curl_easy_setopt(curl, CURLOPT_MAXREDIRS, 50L);
        curl_easy_setopt(curl, CURLOPT_TCP_KEEPALIVE, 1L);

        std::string bodyStr = body_params.dump();
        curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, (long)bodyStr.size());
        curl_easy_setopt(curl, CURLOPT_COPYPOSTFIELDS, bodyStr.c_str());
        DBG("body: " << bodyStr.c_str());
    }

    const CURLcode result = curl_easy_perform(curl);
    curl_easy_cleanup(curl);
    curl = NULL;
    curl_slist_free_all(headers);
    headers = NULL;
    curl_global_cleanup();

    return result;
};

size_t HTTPClient::WriteCallback(void* contents, size_t size, size_t nmemb, std::string* s) {
    size_t newLength = size * nmemb;
    try {
        s->append((char*)contents, newLength);
    }
    catch (std::bad_alloc& e) {
        return 0;
    }
    return newLength;
};

std::string HTTPClient::constructURL(const std::string& path) {
    DBG("Path: " << path);
    std::stringstream ss;
    ss << url;
    if (!port.empty()) {
        ss << ":" << port;
    }
    if (!path.empty()) {
        ss << path;
    }

    DBG(ss.str());
    return ss.str();
}

// === Boring Update functions ===
 // AI API:
void HTTPClient::updateVoiceSettings(const VoiceSettingsKeys& key, const std::string& value ) {
    switch(key) {
    case VoiceSettingsKeys::voice_id :
        voiceSettings.voice_id = value;
        break;
    case VoiceSettingsKeys::name:
        voiceSettings.name = value;
        break;
    case VoiceSettingsKeys::description:
        voiceSettings.description = value;
        break;
    }
    updateTextToSpeech(TextToSpeechKeys::voice_settings, voiceSettings);
};
void HTTPClient::updateVoiceSettings(const VoiceSettingsKeys& key, const json& value) {
    switch (key) {
    case VoiceSettingsKeys::settings:
        voiceSettings.settings = value;
        break;
    case VoiceSettingsKeys::labels:
        voiceSettings.labels = value;
        break;
    }
    updateTextToSpeech(TextToSpeechKeys::voice_settings, voiceSettings);
};
void HTTPClient::updateVoiceSettings(const VoiceSettingsKeys& key, std::vector<std::string>& value) {
    switch (key) {
    case VoiceSettingsKeys::files:
        voiceSettings.files = value;
        break;
    }
    updateTextToSpeech(TextToSpeechKeys::voice_settings, voiceSettings);
};

void HTTPClient::updateTextToSpeech(const TextToSpeechKeys& key, const std::string& value ) {
    switch (key) {
    case TextToSpeechKeys::text:
        textToSpeech.text = value;
        break;
    case TextToSpeechKeys::voice:
        textToSpeech.voice = value;
        break;
    case TextToSpeechKeys::model:
        textToSpeech.model = value;
        break;
    }
    settings.textToSpeech = textToSpeech;
};
void HTTPClient::updateTextToSpeech(const TextToSpeechKeys& key, const VoiceSettings& value) {
    switch (key) {
    case TextToSpeechKeys::voice_settings:
        textToSpeech.voice_settings = value;
        break;
    }
};
void HTTPClient::updateTextToSpeech(const TextToSpeechKeys& key, const int& value) {
    switch (key) {
    case TextToSpeechKeys::seed:
        textToSpeech.seed = value;
        break;
    }
};

// Audio
void  HTTPClient::updateAudioFormat(const AudioFormatKeys& key, const std::string& value) {
    switch (key) {
    case AudioFormatKeys::codec:
        audioFormat.codec = value;
        break;
    case AudioFormatKeys::bit_depth:
        audioFormat.bit_depth = value;
        break;
    case AudioFormatKeys::bit_rate:
        audioFormat.bit_rate = value;
        break;
    case AudioFormatKeys::normalization_type:
        audioFormat.normalization_type = value;
        break;
    }
    updateSessionSettings(SessionSettingsKeys::audio_format, audioFormat);
};
void  HTTPClient::updateAudioFormat(const AudioFormatKeys& key, const int& value) {
    switch (key) {
    case AudioFormatKeys::sample_rate:
        audioFormat.sample_rate = value;
        break;
    case AudioFormatKeys::channels:
        audioFormat.channels = value;
        break;
    }
    updateSessionSettings(SessionSettingsKeys::audio_format, audioFormat);
};

// Engine Modules
void HTTPClient::updateSessionEngines(const EngineModulesKeys& key, const std::string& value ) {
    switch (key) {
    case EngineModulesKeys::ai_api_engine_module:
        engineModules.ai_api_engine_module = value;
        break;
    case EngineModulesKeys::audio_file_engine_module:
        engineModules.audio_file_engine_module = value;
        break;
    case EngineModulesKeys::script_db_engine_module:
        engineModules.script_db_engine_module = value;
        break;
    }
};
void HTTPClient::updateSessionEngines(const EngineModulesKeys& key, const int& value) {
    switch (key) {
    case EngineModulesKeys::ai_api_engine_module_index:
        engineModules.ai_api_engine_module_index = value;
        break;
    case EngineModulesKeys::audio_file_engine_module_index:
        engineModules.audio_file_engine_module_index = value;
        break;
    case EngineModulesKeys::script_db_engine_module_index:
        engineModules.script_db_engine_module_index = value;
        break;
    }
};
void HTTPClient::updateSessionEngineSettings(const EngineModulesKeys& key, const std::string& value) {
    json valueJ;
    try {
        valueJ = json{ value };
    }
    catch (json::parse_error& e) {
        DBG("JSON parse error: " << e.what());
    }

    switch (key) {
    case EngineModulesKeys::ai_api_engine_module:
        aiApiSettings = valueJ;
        break;
    case EngineModulesKeys::audio_file_engine_module:
        audioFileEngineSettings = valueJ;
        break;
    case EngineModulesKeys::script_db_engine_module:
        scriptDbEngineSettings = valueJ;
        break;
    }
};

// Script
void HTTPClient::updateCharacterInfo(const CharacterInfoKeys& key, const std::string& value ) {
    switch (key) {
    case CharacterInfoKeys::id:
        characterInfo.id = value;
        break;
    case CharacterInfoKeys::character_name:
        characterInfo.character_name = value;
        break;
    case CharacterInfoKeys::voice_talent:
        characterInfo.voice_talent = value;
        break;
    case CharacterInfoKeys::script_name:
        characterInfo.script_name = value;
        break;
    case CharacterInfoKeys::gender:
        characterInfo.gender = value;
        break;
    }
};
void HTTPClient::updateCharacterInfo(const CharacterInfoKeys& key, const int& value) {
    switch (key) {
    case CharacterInfoKeys::number_of_lines:
        characterInfo.number_of_lines = value;
        break;
    }
};

void HTTPClient::updateCurrentScriptLine(const ScriptLineKeys& key, const std::string& value) {
    switch (key) {
    case ScriptLineKeys::id:
        currentScriptLine.id = value;
        break;
    case ScriptLineKeys::source_text:
        currentScriptLine.source_text = value;
        break;
    case ScriptLineKeys::translation:
        currentScriptLine.translation = value;
        break;
    case ScriptLineKeys::time_restriction:
        currentScriptLine.time_restriction = value;
        break;
    case ScriptLineKeys::voice_talent:
        currentScriptLine.voice_talent = value;
        break;
    case ScriptLineKeys::character_name:
        currentScriptLine.character_name = value;
        break;
    case ScriptLineKeys::reference_audio_path:
        currentScriptLine.reference_audio_path = value;
        break;
    case ScriptLineKeys::delivery_audio_path:
        currentScriptLine.delivery_audio_path = value;
        break;
    case ScriptLineKeys::generated_audio_path:
        currentScriptLine.generated_audio_path = value;
        break;
    };
};


// Session
void HTTPClient::updateSessionSettings(const SessionSettingsKeys& key, const std::string& value ) {
    // Nothing to see here UwU
};

void HTTPClient::updateSessionSettings(const SessionSettingsKeys& key, const AudioFormat& value) {
    switch (key) {
    case SessionSettingsKeys::audio_format:
        sessionSettings.audio_format = value;
    }
};


// Plugin
void HTTPClient::loadPluginSettings() {
    const juce::String settingsLocation{ juce::File::getSpecialLocation(juce::File::commonApplicationDataDirectory).getFullPathName() + juce::File::getSeparatorString() + "vivoac" + juce::File::getSeparatorString() + "settings.json"};
    const juce::File settingsFile{ settingsLocation };
    settingsFile.create();
    const json settingsJ = json::parse(settingsFile.loadFileAsString().toStdString());
    settings = settingsJ;

    textToSpeech = settings.textToSpeech;
    engineModules = settings.engineModules;
    sessionSettings = settings.sessionSettings;
    generatedAudioPath = settings.generatedAudioPath;
    url = settings.url;
    port = settings.port;
    apiKey = settings.api_key;
    DBG(settingsJ.dump(4));
    DBG(json{ settings }.dump(4));
};

void HTTPClient::savePluginSettings() {
    settings.textToSpeech = textToSpeech;
    settings.engineModules = engineModules;
    settings.sessionSettings = sessionSettings;
    settings.generatedAudioPath = generatedAudioPath;
    settings.url = url;
    settings.port = port;
    settings.api_key = apiKey;

    const juce::String settingsLocation{ juce::File::getSpecialLocation(juce::File::commonApplicationDataDirectory).getFullPathName() + juce::File::getSeparatorString() + "vivoac" + juce::File::getSeparatorString() + "settings.json" };
    const juce::File settingsFile{ settingsLocation };

    settingsFile.replaceWithText(json{ settings }[0] .dump());
};