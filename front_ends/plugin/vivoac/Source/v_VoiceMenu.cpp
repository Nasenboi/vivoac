/*
  ==============================================================================

    v_VoiceMenu.cpp
    Created: 28 May 2024 9:24:46am
    Author:  cboen

  ==============================================================================
*/

#include <JuceHeader.h>
#include "v_VoiceMenu.h"

//==============================================================================
v_VoiceMenu::v_VoiceMenu()
{
    // In your constructor, you should add any child components, and
    // initialise any special settings that your component needs.

}

v_VoiceMenu::~v_VoiceMenu()
{
}

void v_VoiceMenu::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);
}

void v_VoiceMenu::resized()
{
    // This method is where you should set the bounds of any child
    // components that your component contains..

}
