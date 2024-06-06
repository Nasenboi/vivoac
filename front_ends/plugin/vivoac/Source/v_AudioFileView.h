/*
  ==============================================================================

    v_AudioFileView.h
    Created: 5 Jun 2024 2:00:55pm
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"
#include "v_Colors.h"
#include "v_HTTPClient.h"

//==============================================================================
/*
*/
class v_AudioFileView  : public juce::Component, public juce::Button::Listener
{
public:
    v_AudioFileView(VivoacAudioProcessor& p, HTTPClient& c);
    ~v_AudioFileView() override;

    void paint (juce::Graphics&) override;
    void resized() override;

    void buttonClicked(juce::Button* button) override;
    void buttonStateChanged(juce::Button* button) override {};

private:
    v_Colors colors;
    VivoacAudioProcessor& processor;
    HTTPClient& client;

    juce::TextButton loadButton{ "Load" }, playButton{ "Play" };

    const int margin = 3;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_AudioFileView)
};
