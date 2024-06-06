/*
  ==============================================================================

    v_SettingsMenu.cpp
    Created: 28 May 2024 9:24:29am
    Author:  cboen

  ==============================================================================
*/

#include <JuceHeader.h>
#include "v_BaseMenuComponent.h"
#include "v_SettingsMenu.h"

//==============================================================================
v_SettingsMenu::v_SettingsMenu(VivoacAudioProcessor& p, HTTPClient& c) : v_BaseMenuComponent(p,c)
{
    // general settings
    apiUrlLabel.setText("URL:", juce::dontSendNotification);
    apiUrlLabel.attachToComponent(&apiUrl, true);
    addAndMakeVisible(apiUrlLabel);
    apiUrl.addListener(this);
    addAndMakeVisible(apiUrl);
    apiPortLabel.setText("Port:", juce::dontSendNotification);
    apiPortLabel.attachToComponent(&apiPort, true);
    addAndMakeVisible(apiPortLabel);
    apiPort.addListener(this);
    addAndMakeVisible(apiPort);
    apiKeyLabel.setText("API Key:", juce::dontSendNotification);
    apiKeyLabel.attachToComponent(&apiKey, true);
    addAndMakeVisible(apiKeyLabel);
    apiKey.addListener(this);
    addAndMakeVisible(apiKey);

    generatedAudioPathLabel.setText("AI Audio Path:", juce::dontSendNotification);
    generatedAudioPathLabel.attachToComponent(&generatedAudioPath, true);
    addAndMakeVisible(generatedAudioPathLabel);
    generatedAudioPath.addListener(this);
    addAndMakeVisible(generatedAudioPath);

    targetNumChannelsLabel.setText("Channels:", juce::dontSendNotification);
    targetNumChannelsLabel.attachToComponent(&targetNumChannels, true);
    addAndMakeVisible(targetNumChannelsLabel);
    targetNumChannels.addListener(this);
    addAndMakeVisible(targetNumChannels);
    targetSampleRateLabel.setText("Samplerate:", juce::dontSendNotification);
    targetSampleRateLabel.attachToComponent(&targetSampleRate, true);
    addAndMakeVisible(targetSampleRateLabel);
    targetSampleRate.addListener(this);
    addAndMakeVisible(targetSampleRate);
    targetAudioFormatLabel.setText("Format:", juce::dontSendNotification);
    targetAudioFormatLabel.attachToComponent(&targetAudioFormat, true);
    addAndMakeVisible(targetAudioFormatLabel);
    targetAudioFormat.addItem("wav", 1);
    targetAudioFormat.addItem("mp3", 2);
    targetAudioFormat.addItem("ogg", 3);
    targetAudioFormat.addItem("aif", 4);
    targetAudioFormat.setSelectedId(1);
    addAndMakeVisible(targetAudioFormat);


    //  engine settings
    aiApiEngineLabel.setText("AI API Engine:", juce::dontSendNotification);
    aiApiEngineLabel.attachToComponent(&aiApiEngineSettings, true);
    aiApiEngineLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(aiApiEngineLabel);
    aiApiEngineSettings.addListener(this);
    addAndMakeVisible(aiApiEngineSettings);
    aiApiEngine.addListener(this);
    addAndMakeVisible(aiApiEngine);
    audioFileEngineLabel.setText("Audio File Engine:", juce::dontSendNotification);
    audioFileEngineLabel.attachToComponent(&audioFileEngineSettings, true);
    audioFileEngineLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(audioFileEngineLabel);
    audioFileEngine.addListener(this);
    addAndMakeVisible(audioFileEngine);
    aiApiEngine.addListener(this);
    addAndMakeVisible(aiApiEngine);
    scriptDbEngineLabel.setText("Script DB Engine:", juce::dontSendNotification);
    scriptDbEngineLabel.attachToComponent(&scriptDbEngineSettings, true);
    scriptDbEngineLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(scriptDbEngineLabel);
    scriptDbEngineSettings.addListener(this);
    addAndMakeVisible(scriptDbEngineSettings);
    scriptDbEngine.addListener(this);
    addAndMakeVisible(scriptDbEngine);
}

v_SettingsMenu::~v_SettingsMenu()
{
}

void v_SettingsMenu::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);
}

void v_SettingsMenu::resized()
{
    // general settings

    //  engine settings


}
void v_SettingsMenu::buttonClicked(juce::Button* button) {

};

void v_SettingsMenu::textEditorTextChanged(juce::TextEditor& editor) {

};

void v_SettingsMenu::comboBoxChanged(juce::ComboBox* comboBoxThatHasChanged) {

};