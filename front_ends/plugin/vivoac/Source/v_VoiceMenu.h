/*
  ==============================================================================

    v_VoiceMenu.h
    Created: 28 May 2024 9:24:46am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>

//==============================================================================
/*
*/
class v_VoiceMenu  : public juce::Component
{
public:
    v_VoiceMenu();
    ~v_VoiceMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_VoiceMenu)
};
