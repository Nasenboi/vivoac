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
    juce::TableListBox scriptTable {"Script", nullptr};

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_ScriptMenu)
};
