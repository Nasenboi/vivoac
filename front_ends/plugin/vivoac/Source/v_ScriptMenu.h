/*
  ==============================================================================

    v_ScriptMenu.h
    Created: 28 May 2024 9:23:45am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "v_Colors.h"

//==============================================================================
/*
*/
class v_ScriptMenu  : public juce::Component
{
public:
    v_ScriptMenu();
    ~v_ScriptMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    v_Colors colors;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_ScriptMenu)
};
