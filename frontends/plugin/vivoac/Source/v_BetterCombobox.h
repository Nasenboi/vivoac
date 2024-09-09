/*
  ==============================================================================

	v_BetterCombobox.h
	Created: 11 Jun 2024 2:53:32pm
	Author:  cboen

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>

class v_BetterCombobox : public juce::ComboBox {
public:
	int getItemIdByText(const juce::String& szText) const {
		for (int i = 0; i < getNumItems(); ++i) {
			if (szText == getItemText(i)) return getItemId(i);
		}
		return -1;
	}
	void setSelectetItemByText(const juce::String& szText) {
		setSelectedId(getItemIdByText(szText), juce::dontSendNotification);
	}
};