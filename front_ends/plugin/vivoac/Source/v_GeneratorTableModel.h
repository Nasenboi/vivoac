/*
  ==============================================================================

	v_GeneratorTableBodel.h
	Created: 12 Jun 2024 3:31:34pm
	Author:  cboen

  ==============================================================================
*/

#pragma once
#include "v_Colors.h"
#include <JuceHeader.h>

class v_GeneratorTableModel : public juce::TableListBoxModel {
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

		// trim text from the begining until it fits in the cell:
		juce::String text = generatedAudioFiles[rowNumber];
		int begin = text.length() - 60;
		if (begin < 0) { begin = 0; }
		switch (columnId) {
		case 1:
			g.drawText(text.substring(begin), juce::Rectangle(0, 0, width, height), juce::Justification::centred, true);
			break;
		default:
			break;
		};
	};

	void updateTable(std::vector<std::string>& newGeneratedAudioFiles) {
		generatedAudioFiles.clear();
		generatedAudioFiles = newGeneratedAudioFiles;
		numRows = (int)generatedAudioFiles.size();
	};

	int getScriptLength() {
		return numRows;
	};

	std::string getAudioFile(int row) {
		return generatedAudioFiles[row];
	};

	void removeAudioFileFromTable(int row) {
		generatedAudioFiles.erase(generatedAudioFiles.begin() + row);
		numRows = (int)generatedAudioFiles.size();
	};

private:
	int numRows = 0;
	const v_Colors colors;

	std::vector<std::string> generatedAudioFiles;
};
