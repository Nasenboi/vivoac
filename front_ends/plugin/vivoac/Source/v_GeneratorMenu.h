/*
  ==============================================================================

    v_GeneratorMenu.h
    Created: 28 May 2024 9:24:17am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "v_BaseMenuComponent.h"
#include "v_GeneratorTableModel.h"
#include "v_AudioFileView.h"
#include "v_BetterTableListBox.h"

//==============================================================================
/*
*/
class v_GeneratorMenu  : public v_BaseMenuComponent
{
public:
    v_GeneratorMenu(VivoacAudioProcessor& p, HTTPClient& c);
    ~v_GeneratorMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;

    void onEnter() override;
    void onLeave() override;

    void onSelectedRowsChanged();

    void loadGeneratedAudioFiles();

private:
    // UI Sizes
    int margin = 10;
    int defaultLength = 100, defaultHeight = 50;

    // UI components
    v_GeneratorTableModel generatorTableModel;
    v_BetterTableListBox generatorTable{ "Generated Audio", &generatorTableModel };
    v_AudioFileView audioFileView;


    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_GeneratorMenu)
};
