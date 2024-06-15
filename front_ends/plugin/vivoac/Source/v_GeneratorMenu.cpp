/*
  ==============================================================================

    v_GeneratorMenu.cpp
    Created: 28 May 2024 9:24:17am
    Author:  cboen
     
  ==============================================================================
*/

#include <JuceHeader.h>
#include "v_GeneratorMenu.h"

//==============================================================================
v_GeneratorMenu::v_GeneratorMenu(VivoacAudioProcessor& p, HTTPClient& c): v_BaseMenuComponent(p,c), audioFileView(p, c, false)
{
    // The table:
    generatorTable.setSelectedRowsChangedCallback([this](int lastRowSelected) {
        this->onSelectedRowsChanged();
        });
    generatorTable.getViewport()->setScrollBarsShown(false, false, true, false);
    addAndMakeVisible(generatorTable);
    generatorTable.getHeader().addColumn("Audio File Name", 1, defaultLength);

    // Audio File view:
    addAndMakeVisible(audioFileView);

    // Texteditors and labels:
    translationLabel.setText("Translation", juce::dontSendNotification);
    translationLabel.attachToComponent(&translation, true);
    addAndMakeVisible(translationLabel);
    translation.setMultiLine(true);
    translation.setReturnKeyStartsNewLine(true);
    translation.addListener(this);
    addAndMakeVisible(translation);

    // Buttons:
    generateButton.addListener(this);
    addAndMakeVisible(generateButton);
}

v_GeneratorMenu::~v_GeneratorMenu()
{
}

void v_GeneratorMenu::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);
}

void v_GeneratorMenu::resized()
{
    generatorTable.setBounds(margin, margin, getWidth() / 2 - 2 * margin, getHeight() - 2 * margin);
    generatorTable.getHeader().setColumnWidth(1, generatorTable.getWidth());
    audioFileView.setBounds(generatorTable.getRight() + margin, margin, getWidth() / 2 - 2 * margin, defaultHeight);

    generateButton.setBounds(getWidth() - margin - defaultLength, getHeight() - margin - defaultLength, defaultLength, defaultLength);
    translation.setBounds(generatorTable.getRight() + margin + defaultLength, generateButton.getBottom() - generateButton.getHeight() - margin - 3 * defaultHeight, getRight() - margin - (generatorTable.getRight() + margin + defaultLength), 3 * defaultHeight);
}

void v_GeneratorMenu::loadGeneratedAudioFiles() {
    juce::File generatedAudioFolder{ client.getGeneratedAudioPath() };
    juce::Array<juce::File> generatedAudioFiles = generatedAudioFolder.findChildFiles(juce::File::findFiles, true);
    std::vector<std::string> generatedAudioFileNames;

    for (auto& file : generatedAudioFiles) {
		generatedAudioFileNames.push_back(file.getFullPathName().toStdString());
	}
	generatorTableModel.updateTable(generatedAudioFileNames);
	generatorTable.updateContent();
}

void v_GeneratorMenu::onSelectedRowsChanged() {
    audioFileView.currentAudioFile = generatorTableModel.getAudioFile(generatorTable.getSelectedRow());
    processor.loadAudioFile(audioFileView.currentAudioFile);
    repaint();
}

void v_GeneratorMenu::textEditorReturnKeyPressed(juce::TextEditor& editor) {
    if (!editor.getReturnKeyStartsNewLine()) {
        editor.unfocusAllComponents();
    };
};
void v_GeneratorMenu::onTextEditorDone(juce::TextEditor& editor) {
    if (&editor == &translation) {
		client.updateCurrentScriptLine(ScriptLineKeys::translation, translation.getText().toStdString());
	}

};

void v_GeneratorMenu::buttonClicked(juce::Button* button) {
	if (button == &generateButton) {
		client.CURLtextToSpeech();
        loadGeneratedAudioFiles();
	}
};

void v_GeneratorMenu::onEnter() {
    loadGeneratedAudioFiles();

    if (audioFileView.currentAudioFile.exists()) {
        processor.loadAudioFile(audioFileView.currentAudioFile);
    }

    translation.setText(client.getCurrentScriptLine().translation, juce::dontSendNotification);
}
void v_GeneratorMenu::onLeave() {
    processor.clearAudio();
}
