#pragma once
#include <JuceHeader.h>
#include <math.h>
#include "v_Colors.h"

class CostumLookAndFeel : public juce::LookAndFeel_V4 {
public:
    CostumLookAndFeel() { mainColor = colors.midnight_green; accentColor = colors.light_sky_blue; }
    CostumLookAndFeel(juce::Colour mc, juce::Colour ac) { mainColor = mc; accentColor = ac; }
    ~CostumLookAndFeel() {}

    void drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height, float sliderPos,
        float rotaryStartAngle, float rotaryEndAngle, juce::Slider& slider) override {
        float diameter;
        if (width < height) {
            diameter = width;
        }
        else {
            diameter = height;
        }
        diameter *= 0.9;
        float radius = diameter / 2;
        float centreX = x + width / 2, centreY = y + height / 2;
        float sX = centreX - radius, sY = centreY - radius;
        juce::Rectangle<float> sliderArea = { sX, sY, diameter, diameter };

        float angle = rotaryStartAngle + sliderPos * (rotaryEndAngle - rotaryStartAngle) - 1.70796f;
        float dX, dY, r = 10.f, dR = 0.75f * radius;
        dX = centreX + dR * cos(angle) - 5.f;
        dY = centreY + dR * sin(angle) - 5.f;
        juce::Rectangle<float> dialPointer = { dX, dY, r, r };

        g.setColour(mainColor.withSaturation(0.5 + 0.5 * sliderPos));
        g.fillEllipse(sliderArea);
        g.setColour(accentColor.withSaturation(1 - sliderPos));
        g.fillEllipse(dialPointer);
    }


private:
    v_Colors colors;
    juce::Colour mainColor, accentColor;
};