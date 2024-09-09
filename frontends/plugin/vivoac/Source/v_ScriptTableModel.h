/*
  ==============================================================================

	v_ScriptTableModel.h
	Created: 5 Jun 2024 3:30:17pm
	Author:  cboen

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>
//==============================================================================
/*
*/
class ScriptTableModel : public juce::TableListBoxModel {
public:
	int getNumRows() override {
		return numRows;
	}

	void paintRowBackground(juce::Graphics& g, int rowNumber, int, int, bool rowIsSelected) override {
		if (rowIsSelected) {
			g.fillAll(colors.light_sky_blue);
		}
		else if (rowNumber % 2 == 0) {
			g.fillAll(colors.rich_black.brighter(0.15f));
		}
	};

	void paintCell(juce::Graphics& g, int rowNumber, int columnId, int width, int height, bool) override {
		g.setColour(juce::Colours::white);
		g.setFont(12.0f);
		juce::String text, id;

		text = scriptLines[rowNumber].source_text;
		id = scriptLines[rowNumber].id;

		switch (columnId) {
		case 1:
			g.drawText(id, juce::Rectangle(0, 0, width, height), juce::Justification::centred, true);
			break;
		case 2:
			if (text.length() > 35) { text.append("...", 3); }
			g.drawText(text, juce::Rectangle(margin, 0, width - 2 * margin, height), juce::Justification::left, true);
			break;
		default:
			break;
		};
	};

	void updateTable(std::vector<ScriptLine>& newScriptLines) {
		scriptLines.clear();
		scriptLines = newScriptLines;
		numRows = (int)scriptLines.size();
	};

	void listWasScrolled() override {

	};

	int getScriptLength() {
		return numRows;
	};

private:
	int numRows = 0;
	const v_Colors colors;

	std::vector<ScriptLine> scriptLines;
};
