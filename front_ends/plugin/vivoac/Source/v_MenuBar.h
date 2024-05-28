/*
  ==============================================================================

    v_MenuBar.h
    Created: 26 May 2024 2:32:04pm
    Author:  cboen

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "v_Colors.h"

//==============================================================================
/*
*/
class v_MenuBar  : public juce::Component
{
public:
    v_MenuBar(juce::Button::Listener& buttonListener);
    ~v_MenuBar() override;

    void paint (juce::Graphics&) override;
    void resized() override;

    enum MenuOptions {
        Script, Generator, Voice, Settings
    };

    juce::TextButton& getMenuButton(int num) { return buttons[num]; };

    MenuOptions& getCurrentMenu() { return currentMenu; }
    void setCurrentMenu(MenuOptions newMenu);

    const int num_menu_buttons = 4;

private:
    const v_Colors colors;
    juce::Image logo;

    // Menu Options
    v_MenuBar::MenuOptions currentMenu = v_MenuBar::MenuOptions::Script;
    juce::TextButton buttons[4] = {juce::TextButton("Script"), juce::TextButton("Generator"),
        juce::TextButton("Voice"), juce::TextButton("Settings")};

    // Sizes
    const int button_length = 90;
    const int button_height = 30;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_MenuBar)
};