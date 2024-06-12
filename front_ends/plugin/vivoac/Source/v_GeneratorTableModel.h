/*
  ==============================================================================

    v_GeneratorTableBodel.h
    Created: 12 Jun 2024 3:31:34pm
    Author:  cboen

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>
#include "v_Colors.h"

class ScriptTableModel : public juce::TableListBoxModel {
public:
    int getNumRows() override {
        return numRows;
    }

    void paintRowBackground(juce::Graphics& g, int rowNumber, int width, int height, bool rowIsSelected) override {
        if (rowIsSelected) {
            g.fillAll(colors.light_sky_blue);
        }
        else if (rowNumber % 2 == 0) {
            g.fillAll(colors.rich_black.brighter(0.15f));
        }
    };

    void paintCell(juce::Graphics& g, int rowNumber, int columnId, int width, int height, bool rowIsSelected) override {
        g.setColour(juce::Colours::white);
        g.setFont(12.0f);


        switch (columnId) {
        case 1:
            g.drawText(generatedAudioFiles[rowNumber], juce::Rectangle(0, 0, width, height), juce::Justification::centred, true);
            break;
        default:
            break;
        };
    };

    void updateTable(std::vector<std::string>& newGeneratedAudioFiles) {
        generatedAudioFiles.clear();
        generatedAudioFiles = newGeneratedAudioFiles;
        numRows = generatedAudioFiles.size();
    };

    int getScriptLength() {
        return numRows;
    };

private:
    int numRows = 0;
    const v_Colors colors;

    std::vector<std::string> generatedAudioFiles;
};
