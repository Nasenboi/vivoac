/*
  ==============================================================================

    v_ScriptMenu.cpp
    Created: 28 May 2024 9:23:45am
    Author:  cboen

  ==============================================================================
*/

#include <JuceHeader.h>
#include "v_ScriptMenu.h"

//==============================================================================
v_ScriptMenu::v_ScriptMenu()
{
    // In your constructor, you should add any child components, and
    // initialise any special settings that your component needs.

}

v_ScriptMenu::~v_ScriptMenu()
{
}

void v_ScriptMenu::paint (juce::Graphics& g)
{
    /* This demo code just fills the component's background and
       draws some placeholder text to get you started.

       You should replace everything in this method with your own
       drawing code..
    */

    g.fillAll (getLookAndFeel().findColour (juce::ResizableWindow::backgroundColourId));   // clear the background

    g.setColour (juce::Colours::grey);
    g.drawRect (getLocalBounds(), 1);   // draw an outline around the component

    g.setColour (juce::Colours::white);
    g.setFont (14.0f);
    g.drawText ("v_ScriptMenu", getLocalBounds(),
                juce::Justification::centred, true);   // draw some placeholder text
}

void v_ScriptMenu::resized()
{
    // This method is where you should set the bounds of any child
    // components that your component contains..

}
