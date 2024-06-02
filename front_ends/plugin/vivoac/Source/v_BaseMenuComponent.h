/*
  ==============================================================================

    v_BaseMenuComponent.h
    Created: 28 May 2024 10:20:07am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "v_HTTPClient.h"
#include "PluginProcessor.h"
#include "v_Colors.h"

//==============================================================================
/*
*/
class v_BaseMenuComponent  : public juce::Component
{
public:
    v_BaseMenuComponent(VivoacAudioProcessor& p, HTTPClient& c);
    ~v_BaseMenuComponent() override;

    virtual void paint (juce::Graphics&) override;
    virtual void resized() override;

protected:
    VivoacAudioProcessor &processor;
    HTTPClient& client;
    v_Colors colors;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_BaseMenuComponent)
};
