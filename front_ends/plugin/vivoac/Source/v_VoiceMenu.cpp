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
v_VoiceMenu::v_VoiceMenu(VivoacAudioProcessor& p, HTTPClient& c) : v_BaseMenuComponent(p,c)
{
    voiceTable.setSelectedRowsChangedCallback([this](int lastRowSelected) {
        this->onSelectedRowsChanged();
        });
    voiceTable.getViewport()->setScrollBarsShown(false, false, true, false);
    addAndMakeVisible(voiceTable);
    voiceTable.getHeader().addColumn("Voices", 1, defaultLength);
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
    voiceTable.setBounds(margin, margin, getWidth() / 2 - 2 * margin, getHeight() - 2 * margin);
    voiceTable.getHeader().setColumnWidth(1, voiceTable.getWidth());
}


void v_VoiceMenu::changeListenerCallback(juce::ChangeBroadcaster* source)
{
    refreshComponents();
}

void v_VoiceMenu::onSelectedRowsChanged()
{
	client.CURLgetVoiceSettings(voiceTableModel.getVoiceID(voiceTable.getSelectedRow()));
}

void v_VoiceMenu::refreshComponents() {
    voiceTableModel.updateTable(client.getVoices());
    voiceTable.updateContent();
}

void v_VoiceMenu::onEnter() {
    client.CURLgetVoices();
    refreshComponents();
}
void v_VoiceMenu::onLeave() {

}