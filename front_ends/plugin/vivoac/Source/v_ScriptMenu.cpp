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
v_ScriptMenu::v_ScriptMenu(VivoacAudioProcessor& p) : v_BaseMenuComponent(p)
{
    // In your constructor, you should add any child components, and
    // initialise any special settings that your component needs.

}

v_ScriptMenu::~v_ScriptMenu()
{
}

void v_ScriptMenu::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);
}

void v_ScriptMenu::resized()
{
    // This method is where you should set the bounds of any child
    // components that your component contains..

}
