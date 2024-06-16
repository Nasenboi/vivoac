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
#include <fstream>
#include "nlohmann/json.hpp"
#include "v_DataModels.h"


typedef juce::AudioProcessorValueTreeState japvts;
typedef std::pair<std::string, std::string> HEADER_PARAM;
typedef std::vector<HEADER_PARAM> HEADER_PARAMS;


//==============================================================================
/* The HTTPClient Class
*/
class HTTPClient : public japvts::Listener, public juce::ChangeBroadcaster {
public:
    HTTPClient();
    ~HTTPClient();

    void parameterChanged(const juce::String& parameterID, float newValue) override;

    // == ai api functions ==
    void CURLtextToSpeech();

    // == Audio functions ==
    std::variant<int, std::string> getAudioFormatParameter(const AudioFormatKeys& key);

    // == Engine functions ==
    PossibleEngineModules possibleEngineModules;
    std::string getSessionEngine(EngineModulesKeys key);
    std::string getEngineSettingsString(EngineModulesKeys key, int dump = 4);


    // == Script functions ==
    ScriptLine& getCurrentScriptLine() { return currentScriptLine; };
    void setCurrentScriptLine(const ScriptLine& newScriptLine) { currentScriptLine = newScriptLine; };
    std::vector<ScriptLine>& getAllScriptLines() { return scriptLines; };
    void CURLgetScriptLines();

    // == Session functions ==

    void CURLinitSession();
    void CURLcloseSession();
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
    void setGeneratedAudioPath(const std::string& k) { generatedAudioPath = k; }
    std::string& getGeneratedAudioPath() { return generatedAudioPath; };

    // Engine Modules
    void updateSessionEngines(const EngineModulesKeys& key, const std::string& value);
    void updateSessionEngineSettings(const EngineModulesKeys& key, const std::string& value);

    // Script
    void updateCharacterInfo(const CharacterInfoKeys& key, const std::string& value);
    void updateCharacterInfo(const CharacterInfoKeys& key, const int& value);
    void updateCurrentScriptLine(const ScriptLineKeys& key, const std::string& value);
    void setCurrentScriptLine(const int& index);

    // Session
    void updateSessionSettings(const SessionSettingsKeys& key, const std::string& value);
    void updateSessionSettings(const SessionSettingsKeys& key, const AudioFormat& value);

private:
    // == Curl opts ===
    std::string readBuffer;
    std::string url = "http://localhost", port = "8080";
    std::string sessionID;
    std::string apiKey;
    std::string generatedAudioPath;

    enum HTTPMethod {
        Get, Post, Put, Delete
    };

    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* s);
    static size_t WriteToFileCallback(void* ptr, size_t size, size_t nmemb, void* stream);
    std::string constructURL(const std::string& path = "", json query = json());
    void doCurl(const std::function<void()> callback = std::function<void()>(), const std::string& path = "", const HTTPMethod& method = HTTPMethod::Get,
        const HEADER_PARAMS header_params = {}, json body_params = json(), json query_params = json(), bool checkSessionId = true, bool isBinary = false, std::string destinationPath = "");

    // Listeners:
    std::mutex curlMutex;

    // === The Data models as structures: ===
    // AI API:
    VoiceSettings voiceSettings;
    TextToSpeech textToSpeech;

    // Audio
    AudioFormat audioFormat;

    // Engine Modules:
    EngineModules engineModules;
    json aiApiEngineSettings, audioFileEngineSettings, scriptDbEngineSettings;
    void getAllEngineSettings();
    void CURLgetEngineSettings(EngineModulesKeys key);
    void CURLupdateSessionEngines();
    void updateSessionEngineSettings();
    void CURLupdateSingleSessionEngineSettings(EngineModulesKeys key);

    // Script
    CharacterInfo characterInfo;
    std::vector<ScriptLine> scriptLines;
    ScriptLine currentScriptLine;

    // Session
    SessionSettings sessionSettings;
    void CURLupdateSession();

    // Settings
    void loadPluginSettings();
    void savePluginSettings();
    PluginSettings settings;
};