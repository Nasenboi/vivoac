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

    void onEnter() override {};
    void onLeave() override {};

private:

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_GeneratorMenu)
};
