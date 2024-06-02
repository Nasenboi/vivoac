/*
  ==============================================================================

    v_GeneratorMenu.cpp
    Created: 28 May 2024 9:24:17am
    Author:  cboen

  ==============================================================================
*/

#include <JuceHeader.h>
#include "v_GeneratorMenu.h"

//==============================================================================
v_GeneratorMenu::v_GeneratorMenu(VivoacAudioProcessor& p, HTTPClient& c): v_BaseMenuComponent(p,c)
{
    // In your constructor, you should add any child components, and
    // initialise any special settings that your component needs.

}

v_GeneratorMenu::~v_GeneratorMenu()
{
}

void v_GeneratorMenu::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);
}

void v_GeneratorMenu::resized()
{
    // This method is where you should set the bounds of any child
    // components that your component contains..

}
