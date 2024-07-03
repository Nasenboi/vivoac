/*
  ==============================================================================

	v_GeneratorMenu.cpp
	Created: 28 May 2024 9:24:17am
	Author:  cboen

  ==============================================================================
*/

#include "v_GeneratorMenu.h"
#include <JuceHeader.h>

//==============================================================================
v_GeneratorMenu::v_GeneratorMenu(VivoacAudioProcessor& p, HTTPClient& c) : v_BaseMenuComponent(p, c), audioFileView(p, c, false)
{
	// The table:
	generatorTable.setSelectedRowsChangedCallback([this](int) {
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
	deleteButton.addListener(this);
	addAndMakeVisible(deleteButton);
	openButton.addListener(this);
	addAndMakeVisible(openButton);
}

v_GeneratorMenu::~v_GeneratorMenu()
{
}

void v_GeneratorMenu::paint(juce::Graphics& g)
{
	g.fillAll(colors.rich_black);
}

void v_GeneratorMenu::resized()
{
	generatorTable.setBounds(margin, margin, getWidth() / 2 - 2 * margin, getHeight() - 2 * margin);
	generatorTable.getHeader().setColumnWidth(1, generatorTable.getWidth());
	audioFileView.setBounds(generatorTable.getRight() + margin, margin, getWidth() / 2 - margin, defaultHeight);
	openButton.setBounds(generatorTable.getRight() + margin, audioFileView.getBottom() + margin, defaultHeight, defaultHeight);
	deleteButton.setBounds(generatorTable.getRight() + margin, openButton.getBottom() + 0.5 * margin, defaultHeight, defaultHeight);

	generateButton.setBounds(getWidth() - margin - defaultLength, audioFileView.getBottom() + margin, defaultLength, defaultLength);



	translation.setBounds(generatorTable.getRight() + margin + 0.75f * defaultLength, generateButton.getBottom() + margin, getWidth() / 2 - margin - 0.75f * defaultLength, getHeight() - generateButton.getBottom() - 2.f * margin);
}

void v_GeneratorMenu::loadGeneratedAudioFiles() {
	juce::File generatedAudioFolder{ client.generatedAudioPath };
	juce::Array<juce::File> generatedAudioFiles = generatedAudioFolder.findChildFiles(juce::File::findFiles, true);
	std::vector<std::string> generatedAudioFileNames;

	// Sort the files by date:
	std::sort(generatedAudioFiles.begin(), generatedAudioFiles.end(), [](const juce::File& a, const juce::File& b) {
		return a.getLastModificationTime() > b.getLastModificationTime();
		});

	for (auto& file : generatedAudioFiles) {
		generatedAudioFileNames.push_back(file.getFullPathName().toStdString());
	}
	generatorTableModel.updateTable(generatedAudioFileNames);
	generatorTable.updateContent();
}

void v_GeneratorMenu::onSelectedRowsChanged() {
	if (generatorTable.getSelectedRow() < 0) {
		return;
	}
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
	}
	else if (button == &deleteButton) {
		const int row = generatorTable.getSelectedRow();
		if (row < 0) {
			return;
		}
		juce::File generatedFile = juce::File{ generatorTableModel.getAudioFile(row) };
		if (!generatedFile.exists()) {
			return;
		}
		processor.clearAudio();
		audioFileView.currentAudioFile = juce::File{};
		generatedFile.deleteFile();
		generatorTableModel.removeAudioFileFromTable(row);
		refreshComponents();
	}
	else if (button == &openButton) {
		const int row = generatorTable.getSelectedRow();
		if (row < 0) {
			return;
		}
		juce::File generatedFile = juce::File{ generatorTableModel.getAudioFile(row) };
		if (!generatedFile.exists()) {
			return;
		}
		generatedFile.revealToUser();
	}
};

void v_GeneratorMenu::changeListenerCallback(juce::ChangeBroadcaster*) {
	loadGeneratedAudioFiles();
	if (generatorTable.getNumRows() > 0) {
		generatorTable.selectRow(0);
	}
};

void v_GeneratorMenu::refreshComponents() {
	loadGeneratedAudioFiles();

	if (audioFileView.currentAudioFile.exists()) {
		processor.loadAudioFile(audioFileView.currentAudioFile);
	}
	audioFileView.repaint();

	translation.setText(client.getCurrentScriptLine().translation, juce::dontSendNotification);
}

void v_GeneratorMenu::onEnter() {
	refreshComponents();
}
void v_GeneratorMenu::onLeave() {
	processor.clearAudio();
}


