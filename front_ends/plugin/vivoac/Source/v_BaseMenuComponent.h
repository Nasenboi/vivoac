/*
  ==============================================================================

	v_BaseMenuComponent.h
	Created: 28 May 2024 10:20:07am
	Author:  cboen

  ==============================================================================
*/

#pragma once

#include "PluginProcessor.h"
#include "v_Colors.h"
#include "v_HTTPClient.h"
#include <JuceHeader.h>

//==============================================================================
/*
*/
class v_BaseMenuComponent : public juce::Component, public juce::ChangeListener
{
public:
	v_BaseMenuComponent(VivoacAudioProcessor& p, HTTPClient& c);
	~v_BaseMenuComponent() override;

	virtual void paint(juce::Graphics&) override;
	virtual void resized() override;
	virtual void onEnter() {};
	virtual void onLeave() {};

	virtual void changeListenerCallback(juce::ChangeBroadcaster* source) override = 0;

protected:
	VivoacAudioProcessor& processor;
	HTTPClient& client;
	v_Colors colors;

	JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(v_BaseMenuComponent)
};
