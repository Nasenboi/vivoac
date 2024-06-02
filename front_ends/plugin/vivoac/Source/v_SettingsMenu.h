/*
  ==============================================================================

    v_SettingsMenu.h
    Created: 28 May 2024 9:24:29am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "v_BaseMenuComponent.h"

//==============================================================================
/*
*/
class v_SettingsMenu  : public v_BaseMenuComponent
{
public:
    v_SettingsMenu(VivoacAudioProcessor& p, HTTPClient& c);
    ~v_SettingsMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;

private:

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_SettingsMenu)
};
