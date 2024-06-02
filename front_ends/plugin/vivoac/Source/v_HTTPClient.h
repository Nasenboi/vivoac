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


//==============================================================================
/* The HTTPClient Class
*/
class HTTPClient : public japvts::Listener {
public:
    HTTPClient();
    ~HTTPClient();

    void parameterChanged(const juce::String& parameterID, float newValue) override;

    // == Session functions ==

    void initSession();

    // == Script functions ==
    ScriptLine& getCurrentScriptLine() { return currentScriptLine; };
    void setCurrentScriptLine(const ScriptLine& newScriptLine) { currentScriptLine = newScriptLine; };
    void updateCurrentScriptLine(const std::string& text, const ScriptLineKeys scriptLineKey);
    std::vector<ScriptLine>& getAllScriptLines() { return scriptLines; };
    void fetchScriptLines();

    // == Audio functions ==

    // == ai api functions ==

private:
    // == Curl opts ===
    CURL* curl;
    std::string readBuffer;
    std::string url = "http://localhost", port = "8080";
    std::string sessionID;

    enum HTTPMethod {
        Get, Post, Put, Delete
    };

    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* s);
    std::string constructURL(const std::string& path = "");
    bool initCurl(const std::string& path = "", const HTTPMethod& method = HTTPMethod::Get);

    // === The Data models as structures: ===
    // Script
    CharacterInfo characterInfo;
    std::vector<ScriptLine> scriptLines;
    ScriptLine currentScriptLine;


};