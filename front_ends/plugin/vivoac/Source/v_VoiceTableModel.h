/*
  ==============================================================================

    v_VoiceTableModel.h
    Created: 12 Jun 2024 3:31:21pm
    Author:  cboen

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>

class v_VoiceTableModel : public juce::TableListBoxModel {
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

        // trim text from the begining until it fits in the cell:
        juce::String text = voices[rowNumber];
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
        voices.clear();
        voices = newGeneratedAudioFiles;
        numRows = voices.size();
    };

    int getScriptLength() {
        return numRows;
    };

    std::string getVoiceID(int row) {
        return voices[row];
    };

    void removeAudioFileFromTable(int row) {
        voices.erase(voices.begin() + row);
        numRows = voices.size();
    };

private:
    int numRows = 0;
    const v_Colors colors;

    std::vector<std::string> voices;
};
