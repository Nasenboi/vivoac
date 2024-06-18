/*
  ==============================================================================

    v_ScriptMenu.h
    Created: 28 May 2024 9:23:45am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "v_HTTPClient.h"
#include "v_BaseMenuComponent.h"
#include "v_Colors.h"
#include "v_AudioFileView.h"
#include "v_ScriptTableModel.h"
#include "v_BetterTableListBox.h"

//==============================================================================
/*
*/
class v_ScriptMenu : public v_BaseMenuComponent, public juce::Button::Listener, public juce::TextEditor::Listener, public juce::FileDragAndDropTarget
{
public:
    v_ScriptMenu(VivoacAudioProcessor& p, HTTPClient& c);
    ~v_ScriptMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;


    void buttonClicked(juce::Button* button) override;
    void buttonStateChanged(juce::Button* button) override {};
    void textEditorReturnKeyPressed(juce::TextEditor& editor) override;
    void textEditorFocusLost(juce::TextEditor& editor) override { onTextEditorDone(editor); };
    void onTextEditorDone(juce::TextEditor& editor);
    void changeListenerCallback(juce::ChangeBroadcaster* source) override;

    bool isInterestedInFileDrag(const juce::StringArray& files) override;
    void filesDropped(const juce::StringArray& files, int x, int y) override;

    void onEnter() override;
    void onLeave() override;

private:
    // UI Sizes
    int margin = 20;
    int defaultLength = 100, defaultHeight = 50;

    // UI components
    juce::TextButton prevButton{ "<" }, nextButton{ ">" }, clearButton{ "x" }, loadButton{ "Load" };
    ScriptTableModel scriptTableModel;
    v_BetterTableListBox scriptTable {"Script", &scriptTableModel };
    juce::Label idLabel, sourceTextLabel, translationLabel, timeRestrictionLabel, voiceTalentLabel, characterNameLabel;
    juce::TextEditor id, sourceText, translation, timeRestriction, voiceTalent, characterName;
    // can be either for the reference audio or the source audio
    v_AudioFileView scriptAudioView;
    juce::TextButton sourceLoader{ ">" }, translationLoader{ ">" };
    juce::Label sourceLoaderLabel, translationLoaderLabel;

    void onSelectedRowsChanged();
    void updateComponents();

    juce::SparseSet<int> moveSelection(juce::SparseSet<int> selection, int direction);
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_ScriptMenu)
};
