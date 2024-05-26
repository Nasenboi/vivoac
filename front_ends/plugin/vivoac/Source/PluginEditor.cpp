/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"
#include "v_MenuBar.h"

//==============================================================================
VivoacAudioProcessorEditor::VivoacAudioProcessorEditor(VivoacAudioProcessor& p)
    : AudioProcessorEditor(&p), audioProcessor(p), menuBar(*this)
{
    addAndMakeVisible(menuBar);
    setLookAndFeel(&newLookAndFeel);
    setSize (ui_width, ui_height);
}

VivoacAudioProcessorEditor::~VivoacAudioProcessorEditor()
{
    setLookAndFeel(nullptr);
}

//==============================================================================
void VivoacAudioProcessorEditor::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);
}

void VivoacAudioProcessorEditor::resized()
{
    menuBar.setBounds(0, 0, menuBarWidth, menuBarHeight);
}

void VivoacAudioProcessorEditor::buttonClicked(juce::Button* button) {
    if (button == &menuBar.getMenuButton(0)) {
        menuBar.setCurrentMenu(v_MenuBar::MenuOptions::Menu1);
    }
    else if (button == &menuBar.getMenuButton(1)) {
        menuBar.setCurrentMenu(v_MenuBar::MenuOptions::Menu2);
    }
    else if (button == &menuBar.getMenuButton(2)) {
        menuBar.setCurrentMenu(v_MenuBar::MenuOptions::Menu3);
    }
    else if (button == &menuBar.getMenuButton(3)) {
        menuBar.setCurrentMenu(v_MenuBar::MenuOptions::Menu4);
    }
    resized();
};
