/*
  ==============================================================================

    v_BetterTableListBox.h
    Created: 12 Jun 2024 2:32:28pm
    Author:  cboen

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>

class v_BetterTableListBox : public juce::TableListBox
{
public:

    v_BetterTableListBox(const juce::String& componentName = juce::String(), juce::TableListBoxModel* model = nullptr) : juce::TableListBox(componentName, model), callback(nullptr)
    {
    }

    void setSelectedRowsChangedCallback(std::function<void(int)> cb)
    {
        callback = std::move(cb);
    }

    void selectedRowsChanged(int lastRowSelected) override {
        if (callback)
        {
            callback(lastRowSelected);
        }
    }

private:
    std::function<void(int)> callback;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(v_BetterTableListBox)
};
