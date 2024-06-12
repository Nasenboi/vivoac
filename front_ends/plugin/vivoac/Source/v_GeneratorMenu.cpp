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
}

void v_GeneratorMenu::loadGeneratedAudioFiles() {
    DBG("PATH: " << client.getGeneratedAudioPath());
    juce::File generatedAudioFolder{ client.getGeneratedAudioPath() };
    juce::Array<juce::File> generatedAudioFiles = generatedAudioFolder.findChildFiles(juce::File::findFiles, true);
    std::vector<std::string> generatedAudioFileNames;

    for (auto& file : generatedAudioFiles) {
		generatedAudioFileNames.push_back(file.getFullPathName().toStdString());
	}
    DBG("Generated audio files: " << generatedAudioFileNames.size());
	generatorTableModel.updateTable(generatedAudioFileNames);
	generatorTable.updateContent();
}

void v_GeneratorMenu::onSelectedRowsChanged() {
    audioFileView.currentAudioFile = generatorTableModel.getAudioFile(generatorTable.getSelectedRow());
    processor.loadAudioFile(audioFileView.currentAudioFile);
    repaint();
}

void v_GeneratorMenu::onEnter() {
    loadGeneratedAudioFiles();

    if (audioFileView.currentAudioFile.exists()) {
        processor.loadAudioFile(audioFileView.currentAudioFile);
    }
}
void v_GeneratorMenu::onLeave() {
    processor.clearAudio();
}
