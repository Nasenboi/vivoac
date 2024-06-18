/*
  ==============================================================================

    v_VoiceMenu.h
    Created: 28 May 2024 9:24:46am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "v_BaseMenuComponent.h"
#include "v_VoiceTableModel.h"
#include "v_BetterTableListBox.h"

//==============================================================================
/*
*/
class v_VoiceMenu  : public v_BaseMenuComponent, public juce::TextEditor::Listener
{
public:
    v_VoiceMenu(VivoacAudioProcessor& p, HTTPClient& c);
    ~v_VoiceMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;
    void textEditorReturnKeyPressed(juce::TextEditor& editor) override;
    void textEditorFocusLost(juce::TextEditor& editor) override { onTextEditorDone(editor); };
    void onTextEditorDone(juce::TextEditor& editor);
    void changeListenerCallback(juce::ChangeBroadcaster* source) override;

    void onEnter() override;
    void onLeave() override;

private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_VoiceMenu)
    // UI Sizes
    int margin = 20;
    int defaultLength = 100, defaultHeight = 50;

    // UI components
    v_VoiceTableModel voiceTableModel;
    v_BetterTableListBox voiceTable{ "Voices", &voiceTableModel };
    juce::TextEditor voiceId, voiceName, voiceDescription, voiceFiles, voiceLabels, voiceSettings;
    juce::Label voiceIdLabel, voiceNameLabel, voiceDescriptionLabel, voiceFilesLabel, voiceLabelsLabel, voiceSettingsLabel;

    // private functions
    void refreshComponents();
    void onSelectedRowsChanged();
};
