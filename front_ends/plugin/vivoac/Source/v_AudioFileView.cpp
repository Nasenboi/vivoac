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
v_AudioFileView::v_AudioFileView(VivoacAudioProcessor& p, HTTPClient& c, const bool hasLoadButton): processor(p), client(c), hasLoadButton(hasLoadButton)
{
    if (hasLoadButton) {
        loadButton.addListener(this);
        addAndMakeVisible(loadButton);
    }

    playButton.addListener(this);
    addAndMakeVisible(playButton);
}

v_AudioFileView::~v_AudioFileView()
{
}

void v_AudioFileView::paint(juce::Graphics& g)
{
    const int buttonWidth = getHeight(), buttonHeight = getHeight() / 2 - 2*margin;
    g.fillAll(colors.midnight_green);

    // fill border of waveform:
    juce::Rectangle<int> border{ juce::Point<int>{3 * margin + buttonWidth, 0}, juce::Point<int>{getWidth() - margin, getHeight()} };
    juce::Rectangle<float> borderF{ juce::Point<float>{3.0f * margin + buttonWidth, 0.0f}, juce::Point<float>{getWidth() - (float)margin, (float)getHeight()} };
    g.setColour(colors.rich_black);
    g.fillRect(border);

    juce::AudioBuffer<float> waveForm = processor.getWaveForm();
    if (waveForm.getNumSamples() > 0) {
        juce::Path p;
        g.setColour(colors.electric_blue);
        const float widthRatio = (float)waveForm.getNumSamples() / (float)borderF.getWidth();
        const float heightRatio = ((float)getHeight() - (float)margin) / 2.0f;
        auto readBuffer = waveForm.getReadPointer(0);
        float x = 3.0f * margin + buttonWidth;
        float startY = getHeight() / 2.0f;
        float y = startY;
        p.startNewSubPath(x, y);
        int starti;
        for (int s = 0; s < waveForm.getNumSamples(); s += widthRatio) {
            // simple low pass filter:
            y = 0.0f;
            if (s < 4) {starti = 0;}
            else {starti = -4;}
            for (int i = starti; i < starti + 5; ++i) {y += (readBuffer[(int)s + i] * heightRatio);}
            y = y / 3 + startY;
            //y = (readBuffer[(int)s] * heightRatio) + startY;
            p.lineTo(x, y);
            ++x;
        }
        p.lineTo(getWidth(), startY);
        g.strokePath(p, juce::PathStrokeType(1.0f));
    }

    g.setColour(colors.midnight_green);
    g.drawRoundedRectangle(borderF, 9.0f, 7.0f);
}

void v_AudioFileView::resized()
{
    const int buttonWidth = getHeight(), buttonHeight = getHeight() / 2 - 2*margin;

    if (hasLoadButton) {
        loadButton.setBounds(margin, margin, buttonWidth, buttonHeight);
        playButton.setBounds(margin, getHeight() - margin - buttonHeight, buttonWidth, buttonHeight);
	}
	else {
        playButton.setBounds(margin, margin, buttonWidth, getHeight() - 2 * margin);
	}

}

void v_AudioFileView::buttonClicked(juce::Button* button) {
    if (button == &loadButton) {
        processor.loadAudioFile([this]() {
            this->repaint();
            this->currentAudioFile = processor.getCurrentAudioFile();
        });
    }
    else if (button == &playButton) {
        if (!processor.isPlayingAudio()) {
            processor.playAudio();
        }
        else {
            processor.pauseAudio();
        }
    }
}