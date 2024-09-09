#pragma once
#include "v_Colors.h"
#include <JuceHeader.h>
#include <math.h>

class CostumLookAndFeel : public juce::LookAndFeel_V4 {
public:
	CostumLookAndFeel() {
		setColour(juce::ComboBox::ColourIds::outlineColourId, colors.verdigris);

		setColour(juce::TextButton::ColourIds::buttonColourId, colors.midnight_green);
		setColour(juce::TextButton::ColourIds::buttonOnColourId, colors.rich_black);
		setColour(juce::TextButton::ColourIds::textColourOffId, colors.true_white);
		setColour(juce::TextButton::ColourIds::textColourOnId, colors.true_white);

		setColour(juce::TableListBox::ColourIds::backgroundColourId, colors.rich_black);
		setColour(juce::TableListBox::ColourIds::outlineColourId, colors.verdigris);
		setColour(juce::TableListBox::ColourIds::textColourId, colors.true_white);
		setColour(juce::TableHeaderComponent::ColourIds::backgroundColourId, colors.midnight_green);
		setColour(juce::TableHeaderComponent::ColourIds::highlightColourId, colors.electric_blue);
		setColour(juce::TableHeaderComponent::ColourIds::outlineColourId, colors.verdigris);
		setColour(juce::TableHeaderComponent::ColourIds::textColourId, colors.true_white);

		setColour(juce::TextEditor::ColourIds::backgroundColourId, colors.midnight_green);
		setColour(juce::TextEditor::ColourIds::focusedOutlineColourId, colors.electric_blue);
		setColour(juce::TextEditor::ColourIds::highlightColourId, colors.verdigris);
		setColour(juce::TextEditor::ColourIds::highlightedTextColourId, colors.true_white);
		setColour(juce::TextEditor::ColourIds::outlineColourId, colors.verdigris);
		setColour(juce::TextEditor::ColourIds::shadowColourId, colors.true_black);
		setColour(juce::TextEditor::ColourIds::textColourId, colors.true_white);

		setColour(juce::ComboBox::ColourIds::arrowColourId, colors.verdigris);
		setColour(juce::ComboBox::ColourIds::backgroundColourId, colors.midnight_green);
		setColour(juce::ComboBox::ColourIds::buttonColourId, colors.verdigris);
		setColour(juce::ComboBox::ColourIds::focusedOutlineColourId, colors.electric_blue);
		setColour(juce::ComboBox::ColourIds::outlineColourId, colors.verdigris);
		setColour(juce::ComboBox::ColourIds::textColourId, colors.true_white);

		setColour(juce::PopupMenu::ColourIds::backgroundColourId, colors.verdigris);
		setColour(juce::PopupMenu::ColourIds::headerTextColourId, colors.electric_blue);
		setColour(juce::PopupMenu::ColourIds::highlightedBackgroundColourId, colors.light_sky_blue);
		setColour(juce::PopupMenu::ColourIds::highlightedTextColourId, colors.rich_black);
		setColour(juce::PopupMenu::ColourIds::textColourId, colors.true_white);
	}
	CostumLookAndFeel(juce::Colour mc, juce::Colour ac) { mainColor = mc; accentColor = ac; }
	~CostumLookAndFeel() {}

	void drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height, float sliderPos,
		float rotaryStartAngle, float rotaryEndAngle, juce::Slider&) override {
		float diameter;
		if (width < height) {
			diameter = (float)width;
		}
		else {
			diameter = (float)height;
		}
		diameter *= 0.9f;
		float radius = diameter / 2.f;
		float centreX = x + width / 2.f, centreY = y + height / 2.f;
		float sX = centreX - radius, sY = centreY - radius;
		juce::Rectangle<float> sliderArea = { sX, sY, diameter, diameter };

		float angle = rotaryStartAngle + sliderPos * (rotaryEndAngle - rotaryStartAngle) - 1.70796f;
		float dX, dY, r = 10.f, dR = 0.75f * radius;
		dX = centreX + dR * cos(angle) - 5.f;
		dY = centreY + dR * sin(angle) - 5.f;
		juce::Rectangle<float> dialPointer = { dX, dY, r, r };

		g.setColour(mainColor.withSaturation(0.5f + 0.5f * sliderPos));
		g.fillEllipse(sliderArea);
		g.setColour(accentColor.withSaturation(1 - sliderPos));
		g.fillEllipse(dialPointer);
	}

private:

	v_Colors colors;
	juce::Colour mainColor = colors.midnight_green, accentColor = colors.light_sky_blue;;
};