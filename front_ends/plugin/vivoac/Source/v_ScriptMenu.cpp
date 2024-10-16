/*
  ==============================================================================

	v_ScriptMenu.cpp
	Created: 28 May 2024 9:23:45am
	Author:  cboen

  ==============================================================================
*/

#include "v_DataModels.h"
#include "v_ScriptMenu.h"
#include <JuceHeader.h>

//==============================================================================
v_ScriptMenu::v_ScriptMenu(VivoacAudioProcessor& p, HTTPClient& c) : v_BaseMenuComponent(p, c), scriptAudioView(p, c)
{
	// Buttons
	prevButton.addListener(this);
	prevButton.setConnectedEdges(juce::TextButton::ConnectedEdgeFlags::ConnectedOnRight);
	addAndMakeVisible(prevButton);
	loadButton.addListener(this);
	loadButton.setConnectedEdges(juce::TextButton::ConnectedEdgeFlags::ConnectedOnRight + juce::TextButton::ConnectedEdgeFlags::ConnectedOnLeft);
	addAndMakeVisible(loadButton);
	nextButton.addListener(this);
	nextButton.setConnectedEdges(juce::TextButton::ConnectedEdgeFlags::ConnectedOnLeft);
	addAndMakeVisible(nextButton);
	clearButton.addListener(this);
	addAndMakeVisible(clearButton);

	// ScriptTable
	scriptTable.setSelectedRowsChangedCallback([this](int) {
		this->onSelectedRowsChanged();
		});
	scriptTable.getViewport()->setScrollBarsShown(false, false, true, false);
	addAndMakeVisible(scriptTable);
	scriptTable.getHeader().addColumn("ID", 1, 0.75 * defaultLength);
	scriptTable.getHeader().addColumn("Script Line", 2, 2.25 * (defaultLength + margin));

	// Labels
	addAndMakeVisible(idLabel);
	idLabel.setText("ID:", juce::dontSendNotification);
	idLabel.attachToComponent(&id, true);
	addAndMakeVisible(sourceTextLabel);
	sourceTextLabel.setText("Source:", juce::dontSendNotification);
	sourceTextLabel.attachToComponent(&sourceText, true);
	addAndMakeVisible(translationLabel);
	translationLabel.setText("Translation:", juce::dontSendNotification);
	translationLabel.attachToComponent(&translation, true);
	addAndMakeVisible(timeRestrictionLabel);
	timeRestrictionLabel.setText("TR:", juce::dontSendNotification);
	timeRestrictionLabel.attachToComponent(&timeRestriction, true);
	addAndMakeVisible(voiceTalentLabel);
	voiceTalentLabel.setText("Voice Talent:", juce::dontSendNotification);
	voiceTalentLabel.attachToComponent(&voiceTalent, true);
	addAndMakeVisible(characterNameLabel);
	characterNameLabel.setText("Character:", juce::dontSendNotification);
	characterNameLabel.attachToComponent(&characterName, true);

	// Text Boxes
	addAndMakeVisible(id);
	id.addListener(this);
	addAndMakeVisible(sourceText);
	sourceText.setMultiLine(true, true);
	sourceText.setReturnKeyStartsNewLine(true);
	sourceText.addListener(this);
	addAndMakeVisible(translation);
	translation.setMultiLine(true, true);
	translation.setReturnKeyStartsNewLine(true);
	translation.addListener(this);
	addAndMakeVisible(timeRestriction);
	timeRestriction.addListener(this);
	addAndMakeVisible(voiceTalent);
	voiceTalent.addListener(this);
	addAndMakeVisible(characterName);
	characterName.addListener(this);

	// Audio File View
	addAndMakeVisible(scriptAudioView);
	sourceLoaderLabel.setText("Source", juce::dontSendNotification);
	sourceLoaderLabel.attachToComponent(&sourceLoader, true);
	addAndMakeVisible(sourceLoaderLabel);
	sourceLoader.addListener(this);
	addAndMakeVisible(sourceLoader);
	translationLoaderLabel.setText("Translation", juce::dontSendNotification);
	translationLoaderLabel.attachToComponent(&translationLoader, true);
	addAndMakeVisible(translationLoaderLabel);
	translationLoader.addListener(this);
	addAndMakeVisible(translationLoader);
}

v_ScriptMenu::~v_ScriptMenu()
{
}

void v_ScriptMenu::paint(juce::Graphics& g)
{
	g.fillAll(colors.rich_black);
}

void v_ScriptMenu::resized()
{
	// Buttons
	prevButton.setBounds(margin, getHeight() - margin - defaultHeight, defaultLength, defaultHeight);
	loadButton.setBounds(margin + defaultLength, getHeight() - margin - defaultHeight, defaultLength, defaultHeight);
	nextButton.setBounds(margin + 2 * defaultLength, getHeight() - margin - defaultHeight, defaultLength, defaultHeight);

	// Script Table
	scriptTable.setBounds(margin, margin, 2.f * margin + 3.f * defaultLength, getHeight() - (2.f * margin + defaultHeight));

	// Text Boxes
	timeRestriction.setBounds(scriptTable.getRight() + margin + 0.75f * defaultLength, margin, defaultLength, defaultHeight / 2.f);
	id.setBounds(getWidth() - margin - 1.5f * defaultLength, margin, 1.5f * defaultLength, defaultHeight / 2.f);

	voiceTalent.setBounds(scriptTable.getRight() + margin + 0.75f * defaultLength, timeRestriction.getBottom() + margin, defaultLength, defaultHeight / 2.f);
	characterName.setBounds(getWidth() - margin - 1.5f * defaultLength, id.getBottom() + margin, 1.5 * defaultLength, defaultHeight / 2.f);

	sourceText.setBounds(scriptTable.getRight() + margin + 0.75f * defaultLength, voiceTalent.getBottom() + margin, getWidth() - scriptTable.getWidth() - 3.f * margin - 0.75f * defaultLength, defaultHeight * 1.5f);
	translation.setBounds(scriptTable.getRight() + margin + 0.75f * defaultLength, sourceText.getBottom() + margin, getWidth() - scriptTable.getWidth() - 3.f * margin - 0.75f * defaultLength, defaultHeight * 1.5f);

	clearButton.setBounds(getWidth() - margin - defaultHeight, getHeight() - margin - defaultHeight, defaultHeight, defaultHeight);

	const int loadButtonSize = (defaultHeight) / 2.f - 0.25f * margin;
	sourceLoader.setBounds(scriptTable.getRight() + defaultHeight + 0.5f * margin, getHeight() - defaultHeight - margin, loadButtonSize, loadButtonSize);
	translationLoader.setBounds(scriptTable.getRight() + defaultHeight + 0.5f * margin, getHeight() - loadButtonSize - margin, loadButtonSize, loadButtonSize);
	scriptAudioView.setBounds(sourceLoader.getRight() + 0.5f * margin, getHeight() - defaultHeight - margin, getWidth() - scriptTable.getWidth() - 3.f * margin - 3.f * defaultHeight, defaultHeight);
}

void v_ScriptMenu::onSelectedRowsChanged() {
	const juce::SparseSet<int> selection = scriptTable.getSelectedRows();
	scriptTable.scrollToEnsureRowIsOnscreen(selection.getRange(selection.getNumRanges() - 1).getStart());
	client.setCurrentScriptLine(selection.getRange(0).getStart());
	updateComponents();
}

void v_ScriptMenu::buttonClicked(juce::Button* button) {
	if (button == &prevButton) {
		const juce::SparseSet<int> selection = scriptTable.getSelectedRows();
		juce::SparseSet<int> newSelection = moveSelection(selection, -1);
		scriptTable.setSelectedRows(newSelection);
	}
	else if (button == &nextButton) {
		const juce::SparseSet<int> selection = scriptTable.getSelectedRows();
		juce::SparseSet<int> newSelection = moveSelection(selection, 1);
		scriptTable.setSelectedRows(newSelection);
	}
	else if (button == &clearButton) {
		scriptTable.deselectAllRows();
		client.setCurrentScriptLine(ScriptLine());
		updateComponents();
		processor.clearAudio();
		scriptAudioView.repaint();
	}
	else if (button == &loadButton) {
		client.CURLgetScriptLines();
	}
	else if (button == &sourceLoader) {
		scriptAudioView.currentAudioFile = juce::File{ client.getCurrentScriptLine().reference_audio_path };
		processor.loadAudioFile(scriptAudioView.currentAudioFile);
	}
	else if (button == &translationLoader) {
		scriptAudioView.currentAudioFile = juce::File{ client.getCurrentScriptLine().delivery_audio_path };
		processor.loadAudioFile(scriptAudioView.currentAudioFile);
	}
}

void v_ScriptMenu::textEditorReturnKeyPressed(juce::TextEditor& editor) {
	if (!editor.getReturnKeyStartsNewLine()) {
		editor.unfocusAllComponents();
	};
};
void v_ScriptMenu::onTextEditorDone(juce::TextEditor& editor) {
	if (&editor == &id) {
		client.updateCurrentScriptLine(ScriptLineKeys::id, editor.getText().toStdString());
	}
	else if (&editor == &sourceText) {
		client.updateCurrentScriptLine(ScriptLineKeys::source_text, editor.getText().toStdString());
	}
	else if (&editor == &translation) {
		client.updateCurrentScriptLine(ScriptLineKeys::translation, editor.getText().toStdString());
	}
	else if (&editor == &voiceTalent) {
		client.updateCurrentScriptLine(ScriptLineKeys::voice_talent, editor.getText().toStdString());
	}
	else if (&editor == &characterName) {
		client.updateCurrentScriptLine(ScriptLineKeys::character_name, editor.getText().toStdString());
	}
	else if (&editor == &timeRestriction) {
		client.updateCurrentScriptLine(ScriptLineKeys::time_restriction, editor.getText().toStdString());
	}
};

void v_ScriptMenu::changeListenerCallback(juce::ChangeBroadcaster*) {
	scriptTableModel.updateTable(client.getAllScriptLines());
	scriptTable.updateContent();
	updateComponents();
};

juce::SparseSet<int> v_ScriptMenu::moveSelection(juce::SparseSet<int> selection, int direction) {
	juce::SparseSet<int> newSelection;
	const int numRanges = selection.getNumRanges();
	const int min = 0, max = scriptTableModel.getScriptLength();
	juce::Range<int> range;
	int start, end;
	for (int i = 0; i < numRanges; ++i) {
		range = selection.getRange(i);
		start = range.getStart() + direction;
		end = range.getEnd() + direction;
		if (start < min || end > max) { return selection; }
		range = juce::Range<int>(start, end);
		newSelection.addRange(range);
	}

	return newSelection;
};

bool v_ScriptMenu::isInterestedInFileDrag(const juce::StringArray& files) {
	if (files[0].contains(".wav") ||
		files[0].contains(".mp3") ||
		files[0].contains(".aif") ||
		files[0].contains(".ogg")) {
		return true;
	}

	return false;
};

void  v_ScriptMenu::updateComponents() {
	// Update text fields accordung to the current script line
	const ScriptLine currentScriptLine = client.getCurrentScriptLine();
	id.setText(currentScriptLine.id, juce::dontSendNotification);
	sourceText.setText(currentScriptLine.source_text, juce::dontSendNotification);
	translation.setText(currentScriptLine.translation, juce::dontSendNotification);
	timeRestriction.setText(currentScriptLine.time_restriction, juce::dontSendNotification);
	voiceTalent.setText(currentScriptLine.voice_talent, juce::dontSendNotification);
	characterName.setText(currentScriptLine.character_name, juce::dontSendNotification);

	sourceLoader.setVisible(!currentScriptLine.reference_audio_path.empty() && juce::File{ currentScriptLine.reference_audio_path }.exists());
	translationLoader.setVisible(!currentScriptLine.delivery_audio_path.empty() && juce::File{ currentScriptLine.delivery_audio_path }.exists());
	if (sourceLoader.isVisible()) {
		scriptAudioView.currentAudioFile = juce::File{ currentScriptLine.reference_audio_path };
		processor.loadAudioFile(scriptAudioView.currentAudioFile);
	}
	else if (translationLoader.isVisible()) {
		scriptAudioView.currentAudioFile = juce::File{ currentScriptLine.delivery_audio_path };
		processor.loadAudioFile(scriptAudioView.currentAudioFile);
	}
	else {
		processor.clearAudio();
	}
	scriptAudioView.repaint();
}

void v_ScriptMenu::filesDropped(const juce::StringArray& files, int, int) {
	if (!isInterestedInFileDrag(files[0])) return;
	processor.loadAudioFile(files[0]);
	scriptAudioView.currentAudioFile = processor.getCurrentAudioFile();
	DBG("Current Audio File: " << scriptAudioView.currentAudioFile.getFullPathName());
	scriptAudioView.repaint();
};

void v_ScriptMenu::onEnter() {
	if (scriptAudioView.currentAudioFile.exists()) {
		processor.loadAudioFile(scriptAudioView.currentAudioFile);
	}
	updateComponents();
}

void v_ScriptMenu::onLeave() {
	processor.clearAudio();
}