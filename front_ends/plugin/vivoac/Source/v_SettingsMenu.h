/*
  ==============================================================================

    v_SettingsMenu.h
    Created: 28 May 2024 9:24:29am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "v_Colors.h"

//==============================================================================
/*
*/
class v_SettingsMenu  : public juce::Component
{
public:
    v_SettingsMenu();
    ~v_SettingsMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    v_Colors colors;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_SettingsMenu)
};
