/*
  ==============================================================================

    v_ScriptMenu.cpp
    Created: 28 May 2024 9:23:45am
    Author:  cboen

  ==============================================================================
*/

#include <JuceHeader.h>
#include "v_ScriptMenu.h"

//==============================================================================
v_ScriptMenu::v_ScriptMenu(VivoacAudioProcessor& p) : v_BaseMenuComponent(p)
{
    prevButton.addListener(this);
    addAndMakeVisible(prevButton);
    nextButton.addListener(this);
    addAndMakeVisible(nextButton);
    scriptTable.getViewport()->setScrollBarsShown(false, false, true, false);
    addAndMakeVisible(scriptTable);

    scriptTable.getHeader().addColumn("ID", 1, defaultLength);
    scriptTable.getHeader().addColumn("Script Line", 2, 2 * (defaultLength+margin));

}

v_ScriptMenu::~v_ScriptMenu()
{
}

void v_ScriptMenu::paint (juce::Graphics& g)
{
    g.fillAll(colors.rich_black);
}

void v_ScriptMenu::resized()
{
    scriptTable.setBounds(margin, margin, 2 * margin + 3 * defaultLength, getHeight() - (3*margin + defaultHeight));

    prevButton.setBounds(margin, getHeight() - margin - defaultHeight, defaultLength, defaultHeight);
    nextButton.setBounds(3*margin + 2*defaultLength, getHeight() - margin - defaultHeight, defaultLength, defaultHeight);
}

void v_ScriptMenu::buttonClicked(juce::Button* button) {
    if (button == &prevButton) {
        const juce::SparseSet<int> selection = scriptTable.getSelectedRows();
        juce::SparseSet<int> newSelection = moveSelection(selection, -1);
        scriptTable.setSelectedRows(newSelection);
        scriptTable.scrollToEnsureRowIsOnscreen(newSelection.getRange(0).getStart());
    }
    if (button == &nextButton) {
        const juce::SparseSet<int> selection = scriptTable.getSelectedRows();
        juce::SparseSet<int> newSelection = moveSelection(selection, 1);
        scriptTable.setSelectedRows(newSelection);
        scriptTable.scrollToEnsureRowIsOnscreen(newSelection.getRange(newSelection.getNumRanges() - 1).getStart());
    }
}

juce::SparseSet<int> v_ScriptMenu::moveSelection(juce::SparseSet<int> selection, int direction) {
    juce::SparseSet<int> newSelection;
    const int numRanges = selection.getNumRanges();
    const int min = 0, max = scriptTableModel.getScriptLength();
    juce::Range<int> range;
    int start, end;
    for (int i = 0; i < numRanges; ++i) {
        range = selection.getRange(i);
        start = range.getStart() + direction;
        end = range.getEnd() + direction;
        if (start < min || end > max) { return selection; }
        range = juce::Range<int>(start, end);
        newSelection.addRange(range);
    }

    return newSelection;
};