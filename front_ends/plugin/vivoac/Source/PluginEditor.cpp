/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"
#include "v_MenuBar.h"
#include "v_ScriptMenu.h"
#include "v_GeneratorMenu.h"
#include "v_VoiceMenu.h"
#include "v_SettingsMenu.h"

//==============================================================================
VivoacAudioProcessorEditor::VivoacAudioProcessorEditor(VivoacAudioProcessor& p)
    : AudioProcessorEditor(&p), audioProcessor(p), menuBar(*this)
{    
    setLookAndFeel(&newLookAndFeel);
    addAndMakeVisible(menuBar);
    for (int i = 0; i < menuBar.num_menu_buttons; ++i) {
        addAndMakeVisible(menuComponents[i].get());
    }
    setSize (ui_width, ui_height);

    client.initSession();
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

    menuComponents[menuBar.getCurrentMenu()]->setBounds(0, menuBarHeight, getWidth(), getHeight() - menuBarHeight);
}

void VivoacAudioProcessorEditor::buttonClicked(juce::Button* button) {
    for (int i = 0; i < menuBar.num_menu_buttons; ++i) {
        if (button == &menuBar.getMenuButton(i)) {
            menuBar.setCurrentMenu(v_MenuBar::MenuOptions(i));
            menuComponents[i]->setVisible(true);

            for (int j = 0; j < menuBar.num_menu_buttons; ++j) {
                if (j != i) {
                    menuComponents[j]->setVisible(false);
                }
            }
            break;
        }
    }
    resized();
};
