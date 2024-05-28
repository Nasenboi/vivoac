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

//==============================================================================
/*
*/
class v_VoiceMenu  : public v_BaseMenuComponent
{
public:
    v_VoiceMenu(VivoacAudioProcessor& p);
    ~v_VoiceMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;

private:

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_VoiceMenu)
};
