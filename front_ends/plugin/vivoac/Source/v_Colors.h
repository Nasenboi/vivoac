#pragma once
#include <JuceHeader.h>

// https://coolors.co/001011-093a3e-3aafb9-64e9ee-97c8eb

struct v_Colors {
	juce::Colour true_black = juce::Colour(0xFF000000);
	juce::Colour rich_black = juce::Colour(0xFF001011);
	juce::Colour midnight_green = juce::Colour(0xFF093A3E);
	juce::Colour verdigris = juce::Colour(0xFF3AAFB9);
	juce::Colour electric_blue = juce::Colour(0xFF64E9EE);
	juce::Colour light_sky_blue = juce::Colour(0xFF97C8EB);
	juce::Colour true_white = juce::Colour(0xFFFFFFFF);
};

const int margin = 10;
const int twoMargin = 20;
const int halfMargin = 5;