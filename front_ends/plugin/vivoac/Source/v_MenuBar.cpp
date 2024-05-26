/*
  ==============================================================================

    v_MenuBar.cpp
    Created: 26 May 2024 2:32:04pm
    Author:  cboen

  ==============================================================================
*/

#include <JuceHeader.h>
#include "v_Colors.h"
#include "v_MenuBar.h"

//==============================================================================
v_MenuBar::v_MenuBar(juce::Button::Listener& buttonListener)
{
    buttons[0].setConnectedEdges(juce::TextButton::ConnectedEdgeFlags::ConnectedOnRight);
    buttons[1].setConnectedEdges(juce::TextButton::ConnectedEdgeFlags::ConnectedOnRight+juce::TextButton::ConnectedEdgeFlags::ConnectedOnLeft);
    buttons[2].setConnectedEdges(juce::TextButton::ConnectedEdgeFlags::ConnectedOnRight+juce::TextButton::ConnectedEdgeFlags::ConnectedOnLeft);
    buttons[3].setConnectedEdges(juce::TextButton::ConnectedEdgeFlags::ConnectedOnLeft);

    for (int i = 0; i < 4; ++i) {
        buttons[i].setColour(juce::TextButton::ColourIds::buttonColourId, colors.midnight_green);
        buttons[i].setColour(juce::TextButton::ColourIds::buttonOnColourId, colors.rich_black);
        buttons[i].setColour(juce::ComboBox::ColourIds::outlineColourId, colors.verdigris);
        buttons[i].setColour(juce::TextButton::ColourIds::textColourOffId, colors.true_white);
        buttons[i].setColour(juce::TextButton::ColourIds::textColourOnId, colors.true_white);
        buttons[i].addListener(&buttonListener);
        addAndMakeVisible(buttons[i]);
    }

    logo = juce::ImageCache::getFromMemory(BinaryData::ViVoAc_Logo_1_0_png, BinaryData::ViVoAc_Logo_1_0_pngSize);
}

v_MenuBar::~v_MenuBar()
{

}

void v_MenuBar::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);
    g.drawImageWithin(logo, getWidth()-200, getHeight()-100, 200, 100, juce::RectanglePlacement::centred);

    juce::ColourGradient gradient = juce::ColourGradient(colors.rich_black, 0, getHeight()-10, colors.midnight_green, 0, getHeight(), false);

    juce::Path p;
    p.startNewSubPath(0.0f, (float)getHeight() - 10);
    p.lineTo((float)getWidth(), (float)getHeight() - 10);
    p.lineTo((float)getWidth(), (float)getHeight());
    p.lineTo(0.0f, (float)getHeight());
    p.closeSubPath();
    g.setGradientFill(gradient);
    g.fillPath(p);
}

void v_MenuBar::resized()
{
    for (int i = 0; i <  4; ++i) {
        if (MenuOptions(i) == currentMenu) {
            buttons[i].setToggleState(true, false);
        }
        else {
            buttons[i].setToggleState(false, false);
        }
        buttons[i].setBounds(i*button_length, getHeight() - button_height,
            button_length, button_height+5);
    }
}

void v_MenuBar::setCurrentMenu(MenuOptions newMenu) {
    currentMenu = newMenu;
    resized();
}