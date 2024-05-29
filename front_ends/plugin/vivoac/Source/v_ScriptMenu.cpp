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
    addAndMakeVisible(prevButton);
    addAndMakeVisible(nextButton);

    addAndMakeVisible(scriptTable);

    scriptTable.getHeader().addColumn("ID", 1, defaultLength);
    scriptTable.getHeader().addColumn("Script Line", 2, 2 * (defaultLength+margin));
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
    scriptTable.setBounds(margin, margin, 2 * margin + 3 * defaultLength, getHeight() - (2*margin + defaultHeight));

    prevButton.setBounds(margin, getHeight() - margin - defaultHeight, defaultLength, defaultHeight);
    nextButton.setBounds(3*margin + 2*defaultLength, getHeight() - margin - defaultHeight, defaultLength, defaultHeight);
}
