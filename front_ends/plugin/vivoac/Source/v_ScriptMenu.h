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


//==============================================================================
/*
*/
class ScriptTableModel : public juce::TableListBoxModel {
public:
    int getNumRows() override {
        return numRows;
    }

    void paintRowBackground(juce::Graphics& g, int rowNumber, int width, int height, bool rowIsSelected) override {
    };

    void paintCell(juce::Graphics& g, int rowNumber, int columnId, int width, int height, bool rowIsSelected) override {

    };
private:
    const int numRows = 15;
};

//==============================================================================
/*
*/
class v_ScriptMenu  : public v_BaseMenuComponent
{
public:
    v_ScriptMenu(VivoacAudioProcessor& p);
    ~v_ScriptMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    // UI Sizes
    int margin = 10;
    int defaultLength = 100, defaultHeight = 50;

    // UI components
    juce::TextButton prevButton{ "<" }, nextButton{ ">" };
    ScriptTableModel scriptTableModel;
    juce::TableListBox scriptTable {"Script", &scriptTableModel };
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_ScriptMenu)
};
