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
#include "v_BaseMenuComponent.h"
#include "v_ScriptMenu.h"
#include "v_GeneratorMenu.h"
#include "v_VoiceMenu.h"
#include "v_SettingsMenu.h"

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
    // access the processor object that created it.
    VivoacAudioProcessor& audioProcessor;
    CostumLookAndFeel newLookAndFeel;
    const v_Colors colors;

    std::unique_ptr <v_BaseMenuComponent> menuComponents[4] = {
        std::make_unique<v_ScriptMenu>(audioProcessor),
        std::make_unique<v_GeneratorMenu>(audioProcessor),
        std::make_unique<v_VoiceMenu>(audioProcessor),
        std::make_unique<v_SettingsMenu>(audioProcessor)
    };

    // UI Components
    const int ui_width = 800, ui_height = 600;

    v_MenuBar menuBar;
    const int menuBarWidth = ui_width, menuBarHeight = 90;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (VivoacAudioProcessorEditor)
};
