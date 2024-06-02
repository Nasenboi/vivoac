/*
  ==============================================================================

    v_SettingsMenu.cpp
    Created: 28 May 2024 9:24:29am
    Author:  cboen

  ==============================================================================
*/

#include <JuceHeader.h>
#include "v_BaseMenuComponent.h"
#include "v_SettingsMenu.h"

//==============================================================================
v_SettingsMenu::v_SettingsMenu(VivoacAudioProcessor& p, HTTPClient& c) : v_BaseMenuComponent(p,c)
{
    // In your constructor, you should add any child components, and
    // initialise any special settings that your component needs.

}

v_SettingsMenu::~v_SettingsMenu()
{
}

void v_SettingsMenu::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);
}

void v_SettingsMenu::resized()
{
    // This method is where you should set the bounds of any child
    // components that your component contains..

}
