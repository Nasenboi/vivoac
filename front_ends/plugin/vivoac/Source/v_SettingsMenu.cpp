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
    apiUrl.setText("http://localhost");
    apiUrl.addListener(this);
    addAndMakeVisible(apiUrl);
    apiPortLabel.setText("Port:", juce::dontSendNotification);
    apiPortLabel.attachToComponent(&apiPort, true);
    addAndMakeVisible(apiPortLabel);
    apiPort.setText("8080");
    apiPort.addListener(this);
    addAndMakeVisible(apiPort);
    apiKeyLabel.setText("API Key:", juce::dontSendNotification);
    apiKeyLabel.attachToComponent(&apiKey, true);
    addAndMakeVisible(apiKeyLabel);
    apiKey.addListener(this);
    addAndMakeVisible(apiKey);
    sessionIdLabel.setText("Session:", juce::dontSendNotification);
    sessionIdLabel.attachToComponent(&sessionId, true);
    addAndMakeVisible(sessionIdLabel);
    sessionId.setReadOnly(true);
    addAndMakeVisible(sessionId);
    reconnectButton.addListener(this);
    addAndMakeVisible(reconnectButton);

    generatedAudioPathLabel.setText("AI Audio Path:", juce::dontSendNotification);
    generatedAudioPathLabel.attachToComponent(&generatedAudioPath, true);
    addAndMakeVisible(generatedAudioPathLabel);
    generatedAudioPath.addListener(this);
    addAndMakeVisible(generatedAudioPath);
    choosePathButton.addListener(this);
    addAndMakeVisible(choosePathButton);

    targetNumChannelsLabel.setText("Channels:", juce::dontSendNotification);
    targetNumChannelsLabel.attachToComponent(&targetNumChannels, true);
    addAndMakeVisible(targetNumChannelsLabel);
    targetNumChannels.setInputRestrictions(1, "123456789");
    targetNumChannels.addListener(this);
    addAndMakeVisible(targetNumChannels);
    targetSampleRateLabel.setText("Samplerate:", juce::dontSendNotification);
    targetSampleRateLabel.attachToComponent(&targetSampleRate, true);
    addAndMakeVisible(targetSampleRateLabel);
    targetSampleRate.setInputRestrictions(6, "0123456789");
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
    aiApiEngineSettings.setMultiLine(true, true);
    aiApiEngineSettings.setReturnKeyStartsNewLine(true);
    aiApiEngineSettings.setTabKeyUsedAsCharacter(true);
    aiApiEngineSettings.addListener(this);
    addAndMakeVisible(aiApiEngineSettings);
    aiApiEngine.addListener(this);
    addAndMakeVisible(aiApiEngine);
    audioFileEngineLabel.setText("Audio File Engine:", juce::dontSendNotification);
    audioFileEngineLabel.attachToComponent(&audioFileEngineSettings, true);
    audioFileEngineLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(audioFileEngineLabel);
    audioFileEngineSettings.setMultiLine(true, true);
    audioFileEngineSettings.addListener(this);
    audioFileEngineSettings.setReturnKeyStartsNewLine(true);
    audioFileEngineSettings.setTabKeyUsedAsCharacter(true);
    addAndMakeVisible(audioFileEngineSettings);
    audioFileEngine.addListener(this);
    addAndMakeVisible(audioFileEngine);
    scriptDbEngineLabel.setText("Script DB Engine:", juce::dontSendNotification);
    scriptDbEngineLabel.attachToComponent(&scriptDbEngineSettings, true);
    scriptDbEngineLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(scriptDbEngineLabel);
    scriptDbEngineSettings.setMultiLine(true, true);
    scriptDbEngineSettings.setReturnKeyStartsNewLine(true);
    scriptDbEngineSettings.setTabKeyUsedAsCharacter(true);
    scriptDbEngineSettings.addListener(this);
    addAndMakeVisible(scriptDbEngineSettings);
    scriptDbEngine.addListener(this);
    addAndMakeVisible(scriptDbEngine);
}

v_SettingsMenu::~v_SettingsMenu()
{
    fileChooser = nullptr;
}

void v_SettingsMenu::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);

    // some nice lines to keep settings visually seperated:
    juce::Path p;
    p.startNewSubPath(getWidth() / 2, 0);
    p.lineTo(getWidth() / 2, getHeight());
    p.startNewSubPath(0, getHeight()/2);
    p.lineTo(getWidth() / 2, getHeight() / 2);
    g.setColour(colors.verdigris);
    g.strokePath(p, juce::PathStrokeType{ 2.0f });
}

void v_SettingsMenu::resized()
{
    // general settings
    apiUrl.setBounds(getWidth() / 4 - textEditLength, margin, textEditLength, textEditHeight);
    apiPort.setBounds(getWidth() / 4 + textEditLength / 2, margin, textEditLength / 2, textEditHeight);
    apiKey.setBounds(getWidth() / 4 - textEditLength, 2 * margin + textEditHeight, textEditLength*2, textEditHeight);
    sessionId.setBounds(getWidth() / 4 - textEditLength, 3 * margin + 2 * textEditHeight, textEditLength*2, textEditHeight);
    reconnectButton.setBounds(getWidth() / 2 - margin - textEditLength/2, 3 * margin + 2 * textEditHeight, textEditLength / 2, textEditHeight);

    generatedAudioPath.setBounds(getWidth() / 4 - textEditLength, getHeight()/2+margin, textEditLength * 2, textEditHeight);
    choosePathButton.setBounds(getWidth() / 2 - margin - textEditLength / 2, getHeight() / 2 + margin, textEditLength / 2, textEditHeight);

    targetAudioFormat.setBounds(getWidth() / 4 - textEditLength, getHeight() / 2 + 2 * margin + textEditHeight, textEditLength, textEditHeight);
    targetSampleRate.setBounds(getWidth() / 4 - textEditLength, getHeight() / 2 + 3 * margin + 2 * textEditHeight, textEditLength, textEditHeight);
    targetNumChannels.setBounds(getWidth() / 4 + textEditLength / 3 * 2, getHeight() / 2 + 3 * margin +2 * textEditHeight, textEditLength / 3, textEditHeight);

    //  engine settings
    aiApiEngineSettings.setBounds(getWidth() - margin - 2 * textEditLength, margin, 2 * textEditLength, getHeight() / 3 - 2*margin);
    audioFileEngineSettings.setBounds(getWidth() - margin - 2 * textEditLength, margin+getHeight()/3, 2 * textEditLength, getHeight() / 3 - 2*margin);
    scriptDbEngineSettings.setBounds(getWidth() - margin - 2 * textEditLength, margin+getHeight()/3*2, 2 * textEditLength, getHeight() / 3 - 2*margin);
    aiApiEngine.setBounds(getWidth() / 2 + margin, getHeight() / 6 - textEditHeight / 2, textEditLength, textEditHeight);
    audioFileEngine.setBounds(getWidth() / 2 + margin, getHeight() / 6 * 3 - textEditHeight / 2, textEditLength, textEditHeight);
    scriptDbEngine.setBounds(getWidth() / 2 + margin, getHeight() / 6 * 5 - textEditHeight / 2, textEditLength, textEditHeight);
}
void v_SettingsMenu::buttonClicked(juce::Button* button) {
    if (button == &reconnectButton) {
        client.reload();
        sessionId.setText(client.getSessionID());
    }
    else if (button == &choosePathButton) {
        fileChooser = std::make_unique<juce::FileChooser>("Please select a good path!");
        auto folderChooserFlags = juce::FileBrowserComponent::openMode | juce::FileBrowserComponent::canSelectDirectories;
        fileChooser->launchAsync(folderChooserFlags, [this](const juce::FileChooser& chooser) {
            juce::File file = chooser.getResult();
            if (file.isDirectory()) {generatedAudioPath.setText(file.getFullPathName());}
        });
    }
};

void v_SettingsMenu::textEditorTextChanged(juce::TextEditor& editor) {
    if (&editor == &apiUrl) {
        client.setUrl(apiUrl.getText().toStdString());
    }
    else if (&editor == &apiPort) {
        client.setPort(apiPort.getText().toStdString());
    }
    else if (&editor == &apiKey) {
        client.setApiKey(apiKey.getText().toStdString());
    }
};

void v_SettingsMenu::comboBoxChanged(juce::ComboBox* comboBoxThatHasChanged) {

};