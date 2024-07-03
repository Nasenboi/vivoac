/*
  ==============================================================================

	v_BaseMenuComponent.cpp
	Created: 28 May 2024 10:20:07am
	Author:  cboen

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "v_BaseMenuComponent.h"
#include <JuceHeader.h>

//==============================================================================
v_BaseMenuComponent::v_BaseMenuComponent(VivoacAudioProcessor& p, HTTPClient& c) : processor(p), client(c)
{
	client.addChangeListener(this);
}

v_BaseMenuComponent::~v_BaseMenuComponent()
{
}

void v_BaseMenuComponent::paint(juce::Graphics& g)
{

}

void v_BaseMenuComponent::resized()
{

}
