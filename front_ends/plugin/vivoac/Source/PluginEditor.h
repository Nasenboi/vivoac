/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"
#include "v_Colors.h"
#include "v_LookAndFeel.h"
#include "v_MenuBar.h"

//==============================================================================
/**
*/
class VivoacAudioProcessorEditor : public juce::AudioProcessorEditor, public juce::Button::Listener
{
public:
    VivoacAudioProcessorEditor (VivoacAudioProcessor&);
    ~VivoacAudioProcessorEditor() override;

    //==============================================================================
    void paint (juce::Graphics&) override;
    void resized() override;

    void buttonClicked(juce::Button* button) override;
    void buttonStateChanged(juce::Button* button) override {};

private:
    // This reference is provided as a quick way for your editor to
    // access the processor object that created it.
    VivoacAudioProcessor& audioProcessor;
    CostumLookAndFeel newLookAndFeel;
    const v_Colors colors;

    // UI Components
    const int ui_width = 800, ui_height = 600;

    v_MenuBar menuBar;
    const int menuBarWidth = ui_width, menuBarHeight = 90;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (VivoacAudioProcessorEditor)
};
