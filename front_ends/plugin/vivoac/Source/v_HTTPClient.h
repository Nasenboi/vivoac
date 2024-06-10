/*
  ==============================================================================

    v_HTTPClient.h
    Created: 29 May 2024 2:20:21pm
    Author:  cboen

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>
#include <curl/curl.h>
#include "nlohmann/json.hpp"
#include "v_DataModels.h"

typedef juce::AudioProcessorValueTreeState japvts;
typedef std::pair<std::string, std::string> HEADER_PARAM;
typedef std::vector<HEADER_PARAM> HEADER_PARAMS;

//==============================================================================
/* The HTTPClient Class
*/
class HTTPClient : public japvts::Listener {
public:
    HTTPClient();
    ~HTTPClient();

    void parameterChanged(const juce::String& parameterID, float newValue) override;

    // == ai api functions ==

    // == Audio functions ==

    // == Engine functions ==
    PossibleEngineModules possibleEngineModules;

    // == Script functions ==
    ScriptLine& getCurrentScriptLine() { return currentScriptLine; };
    void setCurrentScriptLine(const ScriptLine& newScriptLine) { currentScriptLine = newScriptLine; };
    std::vector<ScriptLine>& getAllScriptLines() { return scriptLines; };
    void getScriptLines();

    // == Session functions ==

    void initSession();
    void closeSession();
    void reload();
    std::string getSessionID() { return sessionID; }
    void setUrl(const std::string& u) { url = u; }
    std::string& getUrl() { return url; };
    void setPort(const std::string& p) { port = p; }
    std::string& getPort() { return port; };
    void setApiKey(const std::string& k) { apiKey = k; }
    std::string& getApiKey() { return apiKey; };

    // == Boring Update Functions ==
    // AI API:
    void updateVoiceSettings(const VoiceSettingsKeys& key, const std::string& value);
    void updateVoiceSettings(const VoiceSettingsKeys& key, const json& value);
    void updateVoiceSettings(const VoiceSettingsKeys& key, std::vector<std::string>& value);
    void updateTextToSpeech(const TextToSpeechKeys& key, const std::string& value);
    void updateTextToSpeech(const TextToSpeechKeys& key, const VoiceSettings& value);
    void updateTextToSpeech(const TextToSpeechKeys& key, const int& value);

    // Audio
    void updateAudioFormat(const AudioFormatKeys& key, const std::string& value);
    void updateAudioFormat(const AudioFormatKeys& key, const int& value);
    std::string generatedAudioPath;

    // Engine Modules
    void updateSessionEngines(const EngineModulesKeys& key, const std::string& value);
    void updateSessionEngineSettings(const EngineModulesKeys& key, const std::string& value);

    // Script
    void updateCharacterInfo(const CharacterInfoKeys& key, const std::string& value);
    void updateCharacterInfo(const CharacterInfoKeys& key, const int& value);
    void updateCurrentScriptLine(const ScriptLineKeys& key, const std::string& value);

    // Session
    void updateSessionSettings(const SessionSettingsKeys& key, const std::string& value);
    void updateSessionSettings(const SessionSettingsKeys& key, const AudioFormat& value);

private:
    // == Curl opts ===
    std::string readBuffer;
    std::string url = "http://localhost", port = "8080";
    std::string sessionID;
    std::string apiKey;

    enum HTTPMethod {
        Get, Post, Put, Delete
    };

    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* s);
    std::string constructURL(const std::string& path = "");
    CURLcode doCurl(const std::string& path = "", const HTTPMethod& method = HTTPMethod::Get,
        const HEADER_PARAMS header_params = {}, json body_params = json());

    // === The Data models as structures: ===
    // AI API:
    VoiceSettings voiceSettings;
    TextToSpeech textToSpeech;

    // Audio
    AudioFormat audioFormat;

    // Engine Modules:
    EngineModules engineModules;
    json aiApiSettings, audioFileEngineSettings, scriptDbEngineSettings;

    // Script
    CharacterInfo characterInfo;
    std::vector<ScriptLine> scriptLines;
    ScriptLine currentScriptLine;

    // Session
    SessionSettings sessionSettings;

    // Settings
    void loadPluginSettings();
    void savePluginSettings();
    PluginSettings settings;
};