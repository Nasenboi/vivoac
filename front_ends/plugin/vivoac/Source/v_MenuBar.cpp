/*
  ==============================================================================

	v_MenuBar.cpp
	Created: 26 May 2024 2:32:04pm
	Author:  cboen

  ==============================================================================
*/

#include "v_Colors.h"
#include "v_MenuBar.h"
#include <JuceHeader.h>

//==============================================================================
v_MenuBar::v_MenuBar(juce::Button::Listener& buttonListener)
{
	for (int i = 0; i < num_menu_buttons; ++i) {
		if (i == 0) buttons[i].setConnectedEdges(juce::TextButton::ConnectedEdgeFlags::ConnectedOnRight);
		else if (i == num_menu_buttons - 1) buttons[i].setConnectedEdges(juce::TextButton::ConnectedEdgeFlags::ConnectedOnLeft);
		else buttons[i].setConnectedEdges(juce::TextButton::ConnectedEdgeFlags::ConnectedOnRight + juce::TextButton::ConnectedEdgeFlags::ConnectedOnLeft);

		buttons[i].addListener(&buttonListener);
		addAndMakeVisible(buttons[i]);
	}

	logo = juce::ImageCache::getFromMemory(BinaryData::ViVoAc_Logo_1_0_png, BinaryData::ViVoAc_Logo_1_0_pngSize);
}

v_MenuBar::~v_MenuBar()
{

}

void v_MenuBar::paint(juce::Graphics& g)
{
	g.fillAll(colors.rich_black);
	g.drawImageWithin(logo, getWidth() - 200, getHeight() - 100, 200, 100, juce::RectanglePlacement::centred);

	juce::ColourGradient gradient = juce::ColourGradient(colors.midnight_green, getWidth() / 2, getHeight(), colors.rich_black, getWidth() / 4 * 3, 0, false);

	int x1 = 0.0f;
	int y1 = (float)getHeight() - button_height;
	int x2 = (float)getWidth();
	int y2 = (float)getHeight();

	juce::Path p;
	p.startNewSubPath(x1, y1);
	p.lineTo(x1, y2);
	p.lineTo(x2, y2);
	p.lineTo(x2, y1);
	p.closeSubPath();
	g.setGradientFill(gradient);
	g.fillPath(p);
}

void v_MenuBar::resized()
{
	for (int i = 0; i < num_menu_buttons; ++i) {
		if (MenuOptions(i) == currentMenu) {
			buttons[i].setToggleState(true, false);
		}
		else {
			buttons[i].setToggleState(false, false);
		}
		buttons[i].setBounds(i * button_length, getHeight() - button_height,
			button_length, button_height + 5);
	}
}

void v_MenuBar::setCurrentMenu(MenuOptions newMenu) {
	currentMenu = newMenu;
	resized();
}