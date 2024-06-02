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


//==============================================================================
/*
*/
class ScriptTableModel : public juce::TableListBoxModel {
public:
    int getNumRows() override {
        return numRows;
    }

    void paintRowBackground(juce::Graphics& g, int rowNumber, int width, int height, bool rowIsSelected) override {
        if (rowIsSelected) {
            g.fillAll(colors.light_sky_blue);
        }
        else if (rowNumber % 2 == 0) {
            g.fillAll(colors.rich_black.brighter(0.15f));
        }
    };

    void paintCell(juce::Graphics& g, int rowNumber, int columnId, int width, int height, bool rowIsSelected) override {
        g.setColour(juce::Colours::white);
        g.setFont(12.0f);
        juce::String text, id;

        switch (columnId) {
        case 1:
            id = juce::String("");
            g.drawText(id, juce::Rectangle(0, 0, width, height), juce::Justification::centred, true);
            break;
        case 2:
            text = juce::String("");
            if (text.length() > 35) { text.append("...", 3); }
            g.drawText(text, juce::Rectangle(margin, 0, width-2*margin, height), juce::Justification::left, true);
            break;
        default:
            break;
        };
    };

    void listWasScrolled() override {

    };

    int getScriptLength() {
        return 0;
    };

private:
    int numRows = 0;
    const v_Colors colors;
};

//==============================================================================
/*
*/
class v_ScriptMenu  : public v_BaseMenuComponent, public juce::Button::Listener, public juce::TextEditor::Listener
{
public:
    v_ScriptMenu(VivoacAudioProcessor& p, HTTPClient& c);
    ~v_ScriptMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;


    void buttonClicked(juce::Button* button) override;
    void buttonStateChanged(juce::Button* button) override {};
    void textEditorTextChanged(juce::TextEditor& editor) override;

private:
    // UI Sizes
    int margin = 10;
    int defaultLength = 100, defaultHeight = 50;

    // UI components
    juce::TextButton prevButton{ "<" }, nextButton{ ">" }, clearButton{ "x" }, loadButton{ "load" };
    ScriptTableModel scriptTableModel;
    juce::TableListBox scriptTable {"Script", &scriptTableModel };
    juce::Label idLabel, sourceTextLabel, translationLabel, timeRestrictionLabel, voiceTalentLabel, characterNameLabel;
    juce::TextEditor id, sourceText, translation, timeRestriction, voiceTalent, characterName;

    juce::SparseSet<int> moveSelection(juce::SparseSet<int> selection, int direction);
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_ScriptMenu)
};
