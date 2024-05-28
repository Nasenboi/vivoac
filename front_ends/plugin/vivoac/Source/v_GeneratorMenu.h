/*
  ==============================================================================

    v_GeneratorMenu.h
    Created: 28 May 2024 9:24:17am
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>

//==============================================================================
/*
*/
class v_GeneratorMenu  : public juce::Component
{
public:
    v_GeneratorMenu();
    ~v_GeneratorMenu() override;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_GeneratorMenu)
};
