/*
  ==============================================================================

    v_HTTPClient.cpp
    Created: 29 May 2024 2:20:21pm
    Author:  cboen

  ==============================================================================
*/

#include <curl/curl.h>
#include <fstream>
#include "v_HTTPClient.h"
#include "nlohmann/json.hpp"

using json = nlohmann::json;

//==============================================================================
/* Simple Class functions
*/

HTTPClient::HTTPClient() {
    loadPluginSettings();
    CURLinitSession();
};

HTTPClient::~HTTPClient() {
    // wait for all other threads to finish
    const int closeTimeout = 1500;
    const int startTimeInMs = juce::Time::getMillisecondCounter();
    while (threadRunning && (juce::Time::getMillisecondCounter() - startTimeInMs) < closeTimeout) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
    savePluginSettings();
    CURLcloseSession();
};

void HTTPClient::reload() {
    CURLcloseSession();
    CURLinitSession();
}

//==============================================================================
/* Plugin Settings
*/
void HTTPClient::loadPluginSettings() {
    const juce::String settingsLocation{ juce::File::getSpecialLocation(juce::File::commonApplicationDataDirectory).getFullPathName() + juce::File::getSeparatorString() + "vivoac" + juce::File::getSeparatorString() + "settings.json" };
    const juce::File settingsFile{ settingsLocation };
    settingsFile.create();
    const json settingsJ = json::parse(settingsFile.loadFileAsString().toStdString());
    settings = settingsJ;
    textToSpeech = settings.textToSpeech;
    engineModules = settings.engineModules;
    sessionSettings = settings.sessionSettings;
    audioFormat = sessionSettings.audio_format;
    generatedAudioPath = settings.generatedAudioPath;
    aiApiEngineSettings = settings.aiApiEngineSettings;
    audioFileEngineSettings = settings.audioFileEngineSettings;
    scriptDbEngineSettings = settings.scriptDbEngineSettings;
    url = settings.url;
    port = settings.port;
    apiKey = settings.api_key;
};
void HTTPClient::savePluginSettings() {
    settings.textToSpeech = textToSpeech;
    settings.engineModules = engineModules;
    settings.sessionSettings = sessionSettings;
    settings.generatedAudioPath = generatedAudioPath;
    settings.aiApiEngineSettings = aiApiEngineSettings;
    settings.audioFileEngineSettings = audioFileEngineSettings;
    settings.scriptDbEngineSettings = scriptDbEngineSettings;
    settings.url = url;
    settings.port = port;
    settings.api_key = apiKey;
    const juce::String settingsLocation{ juce::File::getSpecialLocation(juce::File::commonApplicationDataDirectory).getFullPathName() + juce::File::getSeparatorString() + "vivoac" + juce::File::getSeparatorString() + "settings.json" };
    const juce::File settingsFile{ settingsLocation };
    settingsFile.replaceWithText(json{ settings } [0] .dump());
};

//==============================================================================
/* Actual API Functions
*/

// == Session functions ==
void HTTPClient::CURLinitSession() {
    std::function<void()> callback = [this]() {
        json j;
        try {
            j = json::parse(readBuffer);
            DBG(j.dump(4));
            sessionID = j.value("session_id", "");
        }
        catch (json::parse_error& e) {
            DBG("JSON parse error: " << e.what());
            DBG("readBuffer: " << readBuffer);
            sessionID = "";
        }
        CURLupdateSession();
        CURLupdateSessionEngines();
        updateSessionEngineSettings();
    };
    std::thread asyncThread([this, callback]() {
        this->doCurl(callback, "/session/create", HTTPMethod::Put, {}, {}, {}, false);
    });
    threadRunning = true;
    asyncThread.detach();
};

void HTTPClient::CURLcloseSession() {
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));

    std::function<void()> callback = [this]() {
        json j;
        try {
            j = json::parse(readBuffer);
            DBG(j.dump(4));
            sessionID = "";
            DBG("Session Closed!");
        }
        catch (json::parse_error& e) {
            DBG("JSON parse error: " << e.what());
            DBG("readBuffer: " << readBuffer);
            sessionID = "";
        }
    };
    std::thread asyncThread([this, callback, headers]() {
        this->doCurl(callback, "/session/close", HTTPMethod::Post, headers);
    });
    // Do not detach, this session needs to be closed before the program ends!
    asyncThread.join();    
}

void HTTPClient::CURLupdateSession() {
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    json body = {};
    body["new_session"]["session_id"] = sessionID.c_str();
    body["new_session"]["session_settings"] = sessionSettings;
    std::function<void()> callback = []() {};
    std::thread asyncThread([this, callback, headers, body]() {
        this->doCurl(callback, "/session/update", HTTPMethod::Post, headers, body);
        });
    threadRunning = true;
    asyncThread.detach();
}

// == Script functions ==
void HTTPClient::CURLgetScriptLines() {
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    json body = {};
    if (!isEmpty(currentScriptLine)) {
        body["script_line"] = currentScriptLine;
    }
    std::function<void()> callback = [this]() {
        json j;
        try {
            j = json::parse(readBuffer);
        }
        catch (json::parse_error& e) {
            DBG("JSON parse error: " << e.what());
            DBG("readBuffer: " << readBuffer);
        }
        std::vector<json> lines;
        lines = j;
        scriptLines.clear();
        for (int i = 0; i < lines.size(); ++i) {
            scriptLines.push_back(lines[i]);
        }
    };
    std::thread asyncThread([this, callback, headers, body]() {
        this->doCurl(callback, "/script/get", HTTPMethod::Get, headers, body);
    });
    threadRunning = true;
    asyncThread.detach();
};

void HTTPClient::setCurrentScriptLine(const int& index) {
    currentScriptLine = scriptLines[index];
};
// == Audio functions ==
std::variant<int, std::string> HTTPClient::getAudioFormatParameter(const AudioFormatKeys& key) {
    switch (key) {
    case AudioFormatKeys::codec:
        return audioFormat.codec;
        break;
    case AudioFormatKeys::bit_depth:
        return audioFormat.bit_depth;
        break;
    case AudioFormatKeys::bit_rate:
        return audioFormat.bit_rate;
        break;
    case AudioFormatKeys::normalization_type:
        return audioFormat.normalization_type;
        break;
    case AudioFormatKeys::sample_rate:
        return audioFormat.sample_rate;
        break;
    case AudioFormatKeys::channels:
        return audioFormat.channels;
        break;
    }
}

// == ai api functions ==

void HTTPClient::CURLgetUserData() {

}
void HTTPClient::CURLgetModels() {
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    headers.push_back(HEADER_PARAM("api-key", apiKey.c_str()));
}
void HTTPClient::CURLgetVoices() {
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    headers.push_back(HEADER_PARAM("api-key", apiKey.c_str()));
}
void HTTPClient::CURLgetVoiceSettings() {
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    headers.push_back(HEADER_PARAM("api-key", apiKey.c_str()));
}
void HTTPClient::CURLupdateVoiceSettings() {
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    headers.push_back(HEADER_PARAM("api-key", apiKey.c_str()));
}

void HTTPClient::CURLtextToSpeech() {
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    headers.push_back(HEADER_PARAM("api-key", apiKey.c_str()));
    json body;
    textToSpeech.text = currentScriptLine.translation;
    textToSpeech.voice = "de_DE-markus_haase-ep=2665";
    body["data"] = json{ textToSpeech }[0];
    std::string timedate = juce::Time::getCurrentTime().formatted("%Y%m%d_%H%M%S").toStdString();
    std::string target_path = generatedAudioPath + std::string(juce::File::getSeparatorString()) + timedate + "_" + currentScriptLine.character_name + "_" + currentScriptLine.id + ".wav";
    std::function<void()> callback = []() {};
    std::thread asyncThread([this, callback, headers, body, target_path]() {
        this->doCurl(callback, "/ai_api_handler/text_to_speech", HTTPMethod::Post, headers, body, {}, true, true, target_path);
    });
    threadRunning = true;
    asyncThread.detach();
}
// == Engine Functions == 

void HTTPClient::CURLupdateSessionEngines() {
    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    json body = {};
    body["engine_modules"] = engineModules;


    std::function<void()> callback = [](){};
    std::thread asyncThread([this, callback, headers, body]() {
         this->doCurl(callback, "/session/engine/update", HTTPMethod::Post, headers, body);
    });
    threadRunning = true;
    asyncThread.detach();
}

void HTTPClient::getAllEngineSettings() {
    CURLgetEngineSettings(EngineModulesKeys::ai_api_engine_module);
    CURLgetEngineSettings(EngineModulesKeys::script_db_engine_module);
}

void HTTPClient::CURLgetEngineSettings(EngineModulesKeys key) {
    std::string engine_name;
    switch (key) {
    case EngineModulesKeys::ai_api_engine_module:
        engine_name = "ai_api_engine";
        break;
    case EngineModulesKeys::script_db_engine_module:
        engine_name = "script_db_engine";
        break;
    }

    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    json query = {};
    query["engine_module_name"] = engine_name;

    std::function<void()> callback = [this, key]() {
        try {
            json j = json::parse(readBuffer);
            switch (key) {
            case EngineModulesKeys::ai_api_engine_module:
                aiApiEngineSettings = j;
                break;
            case EngineModulesKeys::script_db_engine_module:
                scriptDbEngineSettings = j;
                break;
            }
        }
		catch (json::parse_error& e) {
			DBG("JSON parse error: " << e.what());
			DBG("readBuffer: " << readBuffer);
		}
    };

    std::thread asyncThread([this, callback, headers, query]() {
        this->doCurl(callback, "/session/engine/settings/get", HTTPMethod::Get, headers, {}, query);;
    });
    threadRunning = true;
    asyncThread.detach();
}

void HTTPClient::updateSessionEngineSettings() {
    CURLupdateSingleSessionEngineSettings(EngineModulesKeys::ai_api_engine_module);
    CURLupdateSingleSessionEngineSettings(EngineModulesKeys::script_db_engine_module);
}

void HTTPClient::CURLupdateSingleSessionEngineSettings(EngineModulesKeys key) {
    std::string engine_name;
    json engine_settings;
    switch (key) {
    case EngineModulesKeys::ai_api_engine_module:
        engine_name = "ai_api_engine";
        engine_settings = aiApiEngineSettings;
        break;
    case EngineModulesKeys::script_db_engine_module:
        engine_name = "script_db_engine";
        engine_settings = scriptDbEngineSettings;
        break;
    }
    if (engine_settings.is_null()) {
        CURLgetEngineSettings(key);
        return;
    }

    HEADER_PARAMS headers = {};
    headers.push_back(HEADER_PARAM("session-id", sessionID.c_str()));
    json query = {};
    query["engine_module_name"] = engine_name;
    json body;
    body["engine_settings"] = engine_settings;

    DBG(body.dump(4));

    std::function<void()> callback = []() {};
    std::thread asyncThread([this, callback, headers, body, query]() { 
        this->doCurl(callback, std::string("/session/engine/settings/update"), HTTPMethod::Post,
            headers, body, query, true, false, std::string());
    });
    threadRunning = true;
    asyncThread.detach();
}

std::string HTTPClient::getSessionEngine(EngineModulesKeys key) {
    switch (key) {
    case EngineModulesKeys::ai_api_engine_module:
        return engineModules.ai_api_engine_module;
        break;
    case EngineModulesKeys::script_db_engine_module:
        return engineModules.script_db_engine_module;
        break;
    }
}

std::string  HTTPClient::getEngineSettingsString(EngineModulesKeys key, int dump) {
    switch (key) {
    case EngineModulesKeys::ai_api_engine_module:
        return aiApiEngineSettings.dump(dump);
        break;
    case EngineModulesKeys::script_db_engine_module:
        return scriptDbEngineSettings.dump(dump);
        break;
    }
}

//==============================================================================
/* Class functionality
*/
void HTTPClient::doCurl(const std::function<void()> callback, const std::string& path, const HTTPMethod& method,
    const HEADER_PARAMS header_params, json body_params, json query_params, bool checkSessionId, bool isBinary, std::string destinationPath) {
    std::lock_guard<std::mutex> lock(curlMutex);

    readBuffer.clear();
    auto curlURL = constructURL(path);
    if (curlURL.empty() || (checkSessionId && sessionID.empty())) {
        if (callback) {
			callback();
		}
		afterCurl();
		return; 
    }


    juce::URL curl(curlURL);

    juce::String headers;
    headers += juce::String("accept") + ": " + juce::String("application/ son") + "\r\n";
    for (const auto& h : header_params) {
        headers += juce::String(h.first) + ": " + juce::String(h.second) + "\r\n";
    }

    juce::StringPairArray parameters;
    for (const auto& [key, value] : query_params.items()) {
		parameters.set(key, value.get<std::string>());
	}
    curl = curl.withParameters(parameters);
    if (!body_params.empty()) {
        headers += juce::String("content-type") + ": " + juce::String("application/json") + "\r\n";
        std::string bodyStr = body_params.dump();
        curl = curl.withPOSTData(bodyStr.c_str());
    }

    juce::String cmd;
    switch (method) {
    case HTTPMethod::Put:
	    cmd = "PUT";
	    break;
    case HTTPMethod::Post:  
        cmd = "POST";
        break;
    case HTTPMethod::Delete:
        cmd = "DELETE";
        break;
    case HTTPMethod::Get:
        cmd = "GET";
	    break;
    }

    juce::URL::InputStreamOptions options = juce::URL::InputStreamOptions(juce::URL::ParameterHandling::inAddress)
        .withHttpRequestCmd(cmd)
        .withExtraHeaders(headers);

    std::unique_ptr<juce::InputStream> stream(curl.createInputStream(options));

    if (stream && !isBinary) {
        auto line = stream->readString();
        readBuffer += line.toStdString();
	}
    else if (stream) {
        auto file = juce::File(destinationPath);
        std::unique_ptr<juce::FileOutputStream> out(file.createOutputStream());
        if (out) {
            out->writeFromInputStream(*stream, -1);
        }
        else {
            DBG("Failed to open stream.");
        }
    }
	else {
		DBG("Failed to open stream.");
	}

    if (callback) {
        callback();
    }
    afterCurl();
};

void HTTPClient::afterCurl() {
	threadRunning = false;
	sendChangeMessage();
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

size_t HTTPClient::WriteToFileCallback(void* ptr, size_t size, size_t nmemb, void* stream) {
    size_t written = fwrite(ptr, size, nmemb, (FILE*)stream);
    return written;
}

std::string urlEncode(CURL* curl, const std::string& value) {
    char* output = curl_easy_escape(curl, value.c_str(), value.length());
    if (output) {
        std::string encoded(output);
        curl_free(output);
        return encoded;
    }
    return "";
}

std::string HTTPClient::constructURL(const std::string& path, json query_params) {
    DBG("Path: " << path);
    std::stringstream ss;
    ss << url;
    if (!port.empty()) {
        ss << ":" << port;
    }
    if (!path.empty()) {
        ss << path;
    }

    if (!query_params.empty()) {
        ss << "?";
        CURL* curl = curl_easy_init(); // Initialize a CURL instance for URL encoding
        bool first = true;
        for (const auto& [key, value] : query_params.items()) {
            if (!first) {
                ss << "&";
            }
            first = false;
            std::string encodedKey = urlEncode(curl, key);
            std::string encodedValue;
            if (value.is_string()) {
                encodedValue = urlEncode(curl, value.get<std::string>());
            }
            else {
                encodedValue = urlEncode(curl, value.dump());
            }
            ss << encodedKey << "=" << encodedValue;
        }
        curl_easy_cleanup(curl); // Clean up the CURL instance after encoding
    }

    DBG(ss.str());
    return ss.str();
}

// === Boring Update functions ===
 // AI API:
void HTTPClient::updateVoiceSettings(const VoiceSettingsKeys& key, const std::string& value ) {
    switch(key) {
    case VoiceSettingsKeys::voice_id :
        currentVoiceSettings.voice_id = value;
        break;
    case VoiceSettingsKeys::name:
        currentVoiceSettings.name = value;
        break;
    case VoiceSettingsKeys::description:
        currentVoiceSettings.description = value;
        break;
    }
    updateTextToSpeech(TextToSpeechKeys::voice_settings, currentVoiceSettings);
};
void HTTPClient::updateVoiceSettings(const VoiceSettingsKeys& key, const json& value) {
    switch (key) {
    case VoiceSettingsKeys::settings:
        currentVoiceSettings.settings = value;
        break;
    case VoiceSettingsKeys::labels:
        currentVoiceSettings.labels = value;
        break;
    }
    updateTextToSpeech(TextToSpeechKeys::voice_settings, currentVoiceSettings);
};
void HTTPClient::updateVoiceSettings(const VoiceSettingsKeys& key, std::vector<std::string>& value) {
    switch (key) {
    case VoiceSettingsKeys::files:
        currentVoiceSettings.files = value;
        break;
    }
    updateTextToSpeech(TextToSpeechKeys::voice_settings, currentVoiceSettings);
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
    case EngineModulesKeys::script_db_engine_module:
        engineModules.script_db_engine_module = value;
        break;
    }
    CURLupdateSessionEngines();
    updateSessionEngineSettings();
};

void HTTPClient::updateSessionEngineSettings(const EngineModulesKeys& key, const std::string& value) {
    json valueJ;
    try {
        valueJ = json::parse( value );
    }
    catch (json::parse_error& e) {
        DBG("JSON parse error: " << e.what());
        DBG("readBuffer: " << readBuffer);
    }
    switch (key) {
    case EngineModulesKeys::ai_api_engine_module:
        aiApiEngineSettings = valueJ;
        break;
    case EngineModulesKeys::script_db_engine_module:
        scriptDbEngineSettings = valueJ;
        break;
    }
    updateSessionEngineSettings();
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
        textToSpeech.text = value;
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
    CURLupdateSession();
};
