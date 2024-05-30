/*
  ==============================================================================

    v_HTTPClient.h
    Created: 29 May 2024 2:20:21pm
    Author:  cboen

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>
#include "nlohmann/json.hpp"
#include "v_DataModels.h"

typedef juce::AudioProcessorValueTreeState japvts;


//==============================================================================
/* The HTTPClient Class
*/
class HTTPClient : public japvts::Listener {
public:
    void parameterChanged(const juce::String& parameterID, float newValue) override;

private:
    // === The Data models as structures: ===
    // Script
    CharacterInfo characterInfo;
    std::vector<ScriptLine> scriptLines;

};