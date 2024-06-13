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
#include "v_BetterCombobox.h"

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
    void textEditorReturnKeyPressed(juce::TextEditor& editor) override;
    void textEditorFocusLost(juce::TextEditor& editor) override { onTextEditorDone(editor); };
    void onTextEditorDone(juce::TextEditor& editor);
    void comboBoxChanged(juce::ComboBox* comboBoxThatHasChanged) override;

    void updateSessionComponents();
    void updateEngineComponents();

private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(v_SettingsMenu)
    juce::TextEditor apiUrl, apiPort, apiKey, generatedAudioPath, targetNumChannels, targetSampleRate, aiApiEngineSettings, scriptDbEngineSettings, sessionId;
    juce::Label apiUrlLabel, apiPortLabel, apiKeyLabel, generatedAudioPathLabel, targetNumChannelsLabel, targetSampleRateLabel, targetAudioFormatLabel, aiApiEngineLabel, scriptDbEngineLabel, sessionIdLabel;
    v_BetterCombobox targetAudioFormat, aiApiEngine, scriptDbEngine;
    juce::TextButton reconnectButton{ "reload" }, choosePathButton{ "choose" };

    std::unique_ptr<juce::FileChooser> fileChooser;

    // UI constants
    const int margin = 10, textEditLength = 125, textEditHeight = 25;
};
