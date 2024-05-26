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
        Menu1, Menu2, Menu3, Menu4
    };

    juce::TextButton& getMenuButton(int num) { return buttons[num]; };

    MenuOptions& getCurrentMenu() { return currentMenu; }
    void setCurrentMenu(MenuOptions newMenu);

private:
    const v_Colors colors;
    juce::Image logo;

    // Menu Options
    v_MenuBar::MenuOptions currentMenu = v_MenuBar::MenuOptions::Menu1;

    juce::TextButton buttons[4] = { juce::TextButton("Menu1"), juce::TextButton("Menu2"),
        juce::TextButton("Menu3"), juce::TextButton("Menu4")};

    // Sizes
    const int button_length = 90;
    const int button_height = 30;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (v_MenuBar)
};