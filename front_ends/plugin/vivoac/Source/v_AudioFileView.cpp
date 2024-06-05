/*
  ==============================================================================

    v_AudioFileView.cpp
    Created: 5 Jun 2024 2:00:55pm
    Author:  cboen

  ==============================================================================
*/

#include <JuceHeader.h>
#include "v_AudioFileView.h"

//==============================================================================
v_AudioFileView::v_AudioFileView(VivoacAudioProcessor& p, HTTPClient& c): processor(p), client(c)
{
    setSize(300, 50);

    loadButton.addListener(this);
    addAndMakeVisible(loadButton);
}

v_AudioFileView::~v_AudioFileView()
{
}

void v_AudioFileView::paint (juce::Graphics& g)
{
    g.fillAll (colors.rich_black.brighter(0.15f));
}

void v_AudioFileView::resized()
{
    loadButton.setBounds(margin, margin, 50, 20);
}


void v_AudioFileView::buttonClicked(juce::Button* button) {
    if (button == &loadButton) {
        processor.loadAudioFile();
    }
}