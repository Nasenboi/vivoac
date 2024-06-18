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
class HTTPClient : public juce::ChangeBroadcaster {
public:
    // ==== public variables ====
    PossibleEngineModules possibleEngineModules;
    std::string url = "http://localhost";
    std::string port = "8080";
    std::string sessionID;
    std::string apiKey = "none";
    std::string generatedAudioPath;

    // ==== public functions ====
    HTTPClient();
    ~HTTPClient();

    // == ai api functions ==
    void CURLtextToSpeech();
    void CURLgetUserData();
    void CURLgetModels();
    void CURLgetVoices();
    void CURLgetVoiceSettings(const std::string& voice_id);
    void CURLupdateVoiceSettings();
    std::vector<std::string> getVoices() { return voices; };

    // == Audio functions ==
    std::variant<int, std::string> getAudioFormatParameter(const AudioFormatKeys& key);

    // == Engine functions ==
    void CURLgetEngineSettings(EngineModulesKeys key);
    void CURLupdateSingleSessionEngineSettings(EngineModulesKeys key);
    void CURLupdateSessionEngines();
    std::string getSessionEngine(EngineModulesKeys key);
    std::string getEngineSettingsString(EngineModulesKeys key, int dump = 4);


    // == Script functions ==
    void CURLgetScriptLines();
    ScriptLine& getCurrentScriptLine() { return currentScriptLine; };
    void setCurrentScriptLine(const ScriptLine& newScriptLine) { currentScriptLine = newScriptLine; };
    std::vector<ScriptLine>& getAllScriptLines() { return scriptLines; };
    void setCurrentScriptLine(const int& index);

    // == Session functions ==
    void CURLinitSession();
    void CURLcloseSession();
    void CURLupdateSession();
    void reload();

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
    // ==== private variables ====
    // Plugin Settings
    PluginSettings settings;
    // AI API:
    VoiceSettings currentVoiceSettings;
    TextToSpeech textToSpeech;
    json userData;
    json models;
    std::vector<std::string> voices;

    // Audio
    AudioFormat audioFormat;

    // Engine Modules:
    EngineModules engineModules;
    json aiApiEngineSettings, audioFileEngineSettings, scriptDbEngineSettings;

    // Script
    CharacterInfo characterInfo;
    std::vector<ScriptLine> scriptLines;
    ScriptLine currentScriptLine;

    // Session
    SessionSettings sessionSettings;

    enum HTTPMethod {
        Get, Post, Put, Delete
    };

    std::string readBuffer;

    // Listeners:
    std::mutex curlMutex;
    bool threadRunning = false;

    // ==== private functions ====
    // curl
    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* s);
    static size_t WriteToFileCallback(void* ptr, size_t size, size_t nmemb, void* stream);
    std::string constructURL(const std::string& path = "", json query = json());
    void doCurl(const std::function<void()> callback = std::function<void()>(), const std::string& path = "", const HTTPMethod& method = HTTPMethod::Get,
        const HEADER_PARAMS header_params = {}, json body_params = json(), json query_params = json(), bool checkSessionId = true, bool isBinary = false, std::string destinationPath = "");
    void afterCurl();

    // plugin settings
    void loadPluginSettings();
    void savePluginSettings();

    // Ai API

    // Audio

    // Engine Modules
    void getAllEngineSettings();
    void updateSessionEngineSettings();

    // Script

    // Session


};