/*
  ==============================================================================

    v_VoiceMenu.cpp
    Created: 28 May 2024 9:24:46am
    Author:  cboen

  ==============================================================================
*/

#include <JuceHeader.h>
#include "v_VoiceMenu.h"

//==============================================================================
v_VoiceMenu::v_VoiceMenu(VivoacAudioProcessor& p, HTTPClient& c) : v_BaseMenuComponent(p,c)
{
    // Voice table
    voiceTable.setSelectedRowsChangedCallback([this](int lastRowSelected) {
        this->onSelectedRowsChanged();
        });
    voiceTable.getViewport()->setScrollBarsShown(false, false, true, false);
    addAndMakeVisible(voiceTable);
    voiceTable.getHeader().addColumn("Voices", 1, defaultLength);

    // TextEditors
    voiceIdLabel.setText("Voice ID:", juce::dontSendNotification);
    voiceIdLabel.attachToComponent(&voiceId, true);
    voiceIdLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(voiceIdLabel);
    voiceId.setReadOnly(true);
    addAndMakeVisible(voiceId);

    voiceNameLabel.setText("Name:", juce::dontSendNotification);
    voiceNameLabel.attachToComponent(&voiceName, true);
    voiceNameLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(voiceNameLabel);
    voiceName.setReadOnly(true);
    addAndMakeVisible(voiceName);

    voiceDescriptionLabel.setText("Description:", juce::dontSendNotification);
    voiceDescriptionLabel.attachToComponent(&voiceDescription, true);
    voiceDescriptionLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(voiceDescriptionLabel);
    voiceDescription.setMultiLine(true, true);
    voiceSettings.setReturnKeyStartsNewLine(true);
    voiceSettings.setTabKeyUsedAsCharacter(true);
    voiceDescription.addListener(this);
    addAndMakeVisible(voiceDescription);

    voiceLabelsLabel.setText("Labels:", juce::dontSendNotification);
    voiceLabelsLabel.attachToComponent(&voiceLabels, true);
    voiceLabelsLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(voiceLabelsLabel);
    voiceLabels.setMultiLine(true, true);
    voiceLabels.setReadOnly(true);
    addAndMakeVisible(voiceLabels);

    voiceFilesLabel.setText("Files:", juce::dontSendNotification);
    voiceFilesLabel.attachToComponent(&voiceFiles, true);
    voiceFilesLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(voiceFilesLabel);
    voiceFiles.setMultiLine(true, true);
    voiceFiles.setReadOnly(true);
    addAndMakeVisible(voiceFiles);

    voiceSettingsLabel.setText("Settings:", juce::dontSendNotification);
    voiceSettingsLabel.attachToComponent(&voiceSettings, true);
    voiceSettingsLabel.setJustificationType(juce::Justification::topLeft);
    addAndMakeVisible(voiceSettingsLabel);
    voiceSettings.setMultiLine(true, true);
    voiceSettings.setReturnKeyStartsNewLine(true);
    voiceSettings.setTabKeyUsedAsCharacter(true);
    voiceSettings.addListener(this);
    addAndMakeVisible(voiceSettings);
}

v_VoiceMenu::~v_VoiceMenu()
{
}

void v_VoiceMenu::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);
}

void v_VoiceMenu::resized()
{
    voiceTable.setBounds(margin, margin, getWidth() / 2 - 2 * margin, getHeight() - 2 * margin);
    voiceTable.getHeader().setColumnWidth(1, voiceTable.getWidth());

    voiceId.setBounds(voiceTable.getRight() + margin + 0.75 * defaultLength, margin, defaultLength, defaultHeight / 2);
    voiceName.setBounds(getWidth() - margin - 1.5 * defaultLength, margin, defaultLength * 1.5, defaultHeight / 2);

    voiceDescription.setBounds(voiceTable.getRight() + margin + 0.75 * defaultLength, voiceId.getBottom() + margin, getWidth() / 2 - margin - 0.75 * defaultLength, defaultHeight * 1.5);

    voiceLabels.setBounds(voiceTable.getRight() + margin + 0.75 * defaultLength, voiceDescription.getBottom() + margin, defaultLength, defaultHeight * 1.5);
    voiceFiles.setBounds(getWidth() - margin - 1.5 * defaultLength, voiceDescription.getBottom() + margin, defaultLength * 1.5, defaultHeight * 1.5);

    voiceSettings.setBounds(voiceTable.getRight() + margin + 0.75 * defaultLength, voiceLabels.getBottom() + margin, getWidth() / 2 - margin - 0.75 * defaultLength, getHeight() - voiceLabels.getBottom() - 2 * margin);
}

void v_VoiceMenu::textEditorReturnKeyPressed(juce::TextEditor& editor) {
    if (!editor.getReturnKeyStartsNewLine()) {
        editor.unfocusAllComponents();
    };
};

void v_VoiceMenu::onTextEditorDone(juce::TextEditor& editor) {
    if (&editor == &voiceSettings) {
		client.updateVoiceSettings(VoiceSettingsKeys::settings, editor.getText().toStdString());
    }
	else if (&editor == &voiceName) {
		client.updateVoiceSettings(VoiceSettingsKeys::name, editor.getText().toStdString());
	}
    else if (&editor == &voiceDescription) {
        client.updateVoiceSettings(VoiceSettingsKeys::description, editor.getText().toStdString());
    }
}

void v_VoiceMenu::changeListenerCallback(juce::ChangeBroadcaster* source)
{
    refreshComponents();
}

void v_VoiceMenu::onSelectedRowsChanged()
{
	client.CURLgetVoiceSettings(voiceTableModel.getVoiceID(voiceTable.getSelectedRow()));
}

void v_VoiceMenu::refreshComponents() {
    voiceTableModel.updateTable(client.getVoices());
    voiceTable.updateContent();

    VoiceSettings voiceSettingsJ = client.getCurrentVoiceSettings();

    voiceId.setText(voiceSettingsJ.voice_id, juce::dontSendNotification);
    voiceName.setText(voiceSettingsJ.name, juce::dontSendNotification);
    voiceDescription.setText(voiceSettingsJ.description, juce::dontSendNotification);
    voiceLabels.setText(std::string(voiceSettingsJ.labels.dump(4)), juce::dontSendNotification);
    juce::String files;
    for (std::string s : voiceSettingsJ.files) {
        files += juce::String(s) + "\n";
    }
    voiceFiles.setText(files, juce::dontSendNotification);
    voiceSettings.setText(std::string(voiceSettingsJ.settings.dump(4)), juce::dontSendNotification);
}

void v_VoiceMenu::onEnter() {
    client.CURLgetVoices();
    refreshComponents();
}
void v_VoiceMenu::onLeave() {

}