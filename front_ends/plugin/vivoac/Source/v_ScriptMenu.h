/*
  ==============================================================================

    v_ScriptMenu.h
    Created: 28 May 2024 9:23:45am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
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
            id = juce::String(scriptLines[rowNumber][0]);
            g.drawText(id, juce::Rectangle(0, 0, width, height), juce::Justification::centred, true);
            break;
        case 2:
            text = juce::String(scriptLines[rowNumber][1]);
            if (scriptLines[rowNumber][1].length() > 35) { text.append("...", 3); }
            g.drawText(text, juce::Rectangle(margin, 0, width-2*margin, height), juce::Justification::left, true);
            break;
        default:
            break;
        };
    };

    void listWasScrolled() override {

    };

    int getScriptLength() {
        return scriptLines.size();
    };

private:
    const int numRows = 20;
    const v_Colors colors;

    const std::vector<std::array<juce::String, 2>> scriptLines = {
        {"0", "A cool script line that is also very long and detailed!"},
        {"1", "A cool script line that is also very long and detailed!"},
        {"2", "A cool script line that is also very long and detailed!"},
        {"3", "A cool script line that is also very long and detailed!"},
        {"4", "A cool script line that is also very long and detailed!"},
        {"5", "A cool script line that is also very long and detailed!"},
        {"6", "A cool script line that is also very long and detailed!"},
        {"7", "A cool script line that is also very long and detailed!"},
        {"8", "A cool script line that is also very long and detailed!"},
        {"9", "A cool script line that is also very long and detailed!"},
        {"10", "A cool script line that is also very long and detailed!"},
        {"11", "A cool script line that is also very long and detailed!"},
        {"12", "A cool script line that is also very long and detailed!"},
        {"13", "A cool script line that is also very long and detailed!"},
        {"14", "A cool script line that is also very long and detailed!"},
        {"15", "A cool script line that is also very long and detailed!"},
        {"16", "A cool script line that is also very long and detailed!"},
        {"17", "A cool script line that is also very long and detailed!"},
        {"18", "A cool script line that is also very long and detailed!"},
        {"19", "A cool script line that is also very long and detailed!"}
    };
};

//==============================================================================
/*
*/
class v_ScriptMenu  : public v_BaseMenuComponent, public juce::Button::Listener
{
public:
    v_ScriptMenu(VivoacAudioProcessor& p);
    ~v_ScriptMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;


    void buttonClicked(juce::Button* button) override;

    void buttonStateChanged(juce::Button* button) override {};

private:
    // UI Sizes
    int margin = 10;
    int defaultLength = 100, defaultHeight = 50;

    // UI components
    juce::TextButton prevButton{ "<" }, nextButton{ ">" };
    ScriptTableModel scriptTableModel;
    juce::TableListBox scriptTable {"Script", &scriptTableModel };

    juce::SparseSet<int> moveSelection(juce::SparseSet<int> selection, int direction);
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_ScriptMenu)
};
