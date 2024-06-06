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
};

HTTPClient::~HTTPClient() {
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

void HTTPClient::updateCurrentScriptLine(const std::string& text, const ScriptLineKeys scriptLineKey) {
    switch (scriptLineKey) {
    case ScriptLineKeys::id:
        currentScriptLine.id = text;
        break;
    case ScriptLineKeys::source_text:
        currentScriptLine.source_text = text;
        break;
    case ScriptLineKeys::translation:
        currentScriptLine.translation = text;
        break;
    case ScriptLineKeys::time_restriction:
        currentScriptLine.time_restriction = text;
        break;
    case ScriptLineKeys::voice_talent:
        currentScriptLine.voice_talent = text;
        break;
    case ScriptLineKeys::character_name:
        currentScriptLine.character_name = text;
        break;
    case ScriptLineKeys::reference_audio_path:
        currentScriptLine.reference_audio_path = text;
        break;
    case ScriptLineKeys::delivery_audio_path:
        currentScriptLine.delivery_audio_path = text;
        break;
    case ScriptLineKeys::generated_audio_path:
        currentScriptLine.generated_audio_path = text;
        break;
    };
};

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