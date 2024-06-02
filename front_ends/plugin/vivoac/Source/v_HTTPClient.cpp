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
    curl = curl_easy_init();
    if (!curl) {
        throw std::runtime_error("Failed to initialize CURL");
    }

};

HTTPClient::~HTTPClient() {
    if (curl) {
        curl_easy_cleanup(curl);
    }
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
    if (!initCurl("/session/create", HTTPMethod::Put)) return;

    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

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

    sessionID = j.value("session_id", "");
};

// == Script functions ==

void HTTPClient::updateCurrentScriptLine(const std::string& text, const ScriptLineKeys scriptLineKey) {
    switch (scriptLineKey) {
    case id:
        currentScriptLine.id = text;
        break;
    case source_text:
        currentScriptLine.source_text = text;
        break;
    case translation:
        currentScriptLine.translation = text;
        break;
    case time_restriction:
        currentScriptLine.time_restriction = text;
        break;
    case voice_talent:
        currentScriptLine.voice_talent = text;
        break;
    case character_name:
        currentScriptLine.character_name = text;
        break;
    case reference_audio_path:
        currentScriptLine.reference_audio_path = text;
        break;
    case delivery_audio_path:
        currentScriptLine.delivery_audio_path = text;
        break;
    case generated_audio_path:
        currentScriptLine.generated_audio_path = text;
        break;
    };
};

void HTTPClient::fetchScriptLines() {

};

// == Audio functions ==

// == ai api functions ==


//==============================================================================
/* Class functionality
*/
bool HTTPClient::initCurl(const std::string& path, const HTTPMethod& method) {
    if (!curl) return false;
    readBuffer.clear();
    curl_easy_reset(curl);

    auto curlURL = constructURL(path);
    if (curlURL.empty()) return false;
    curl_easy_setopt(curl, CURLOPT_URL, curlURL.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

    switch (method) {
    case HTTPMethod::Put:
        curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);
        break;
    case HTTPMethod::Post:
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        break;
    case HTTPMethod::Delete:
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "DELETE");
        break;
    default:
        curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
    };

    return true;
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