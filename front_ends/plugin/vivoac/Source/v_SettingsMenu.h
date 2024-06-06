/*
  ==============================================================================

    v_SettingsMenu.h
    Created: 28 May 2024 9:24:29am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "v_BaseMenuComponent.h"

//==============================================================================
/*
*/
class v_SettingsMenu : public v_BaseMenuComponent, public juce::Button::Listener, public juce::TextEditor::Listener, public juce::ComboBox::Listener
{
public:
    v_SettingsMenu(VivoacAudioProcessor& p, HTTPClient& c);
    ~v_SettingsMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;

    void onEnter() override {};
    void onLeave() override {};
    void buttonClicked(juce::Button* button) override;
    void buttonStateChanged(juce::Button* button) override {};
    void textEditorTextChanged(juce::TextEditor& editor) override;
    void comboBoxChanged(juce::ComboBox* comboBoxThatHasChanged) override;

private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(v_SettingsMenu)
    juce::TextEditor apiUrl, apiPort, apiKey, generatedAudioPath, targetNumChannels, targetSampleRate, aiApiEngineSettings, audioFileEngineSettings, scriptDbEngineSettings, sessionId;
    juce::Label apiUrlLabel, apiPortLabel, apiKeyLabel, generatedAudioPathLabel, targetNumChannelsLabel, targetSampleRateLabel, targetAudioFormatLabel, aiApiEngineLabel, audioFileEngineLabel, scriptDbEngineLabel, sessionIdLabel;
    juce::ComboBox targetAudioFormat, aiApiEngine, audioFileEngine, scriptDbEngine;

    // UI constants
    const int margin = 5;
};
