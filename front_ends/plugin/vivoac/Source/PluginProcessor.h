/*
  ==============================================================================

	This file contains the basic framework code for a JUCE plugin processor.

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>


//==============================================================================
/**
*/
class VivoacAudioProcessor : public juce::AudioProcessor
{
public:
	//==============================================================================
	VivoacAudioProcessor();
	~VivoacAudioProcessor() override;

	//==============================================================================
	void prepareToPlay(double sampleRate, int samplesPerBlock) override;
	void releaseResources() override;

#ifndef JucePlugin_PreferredChannelConfigurations
	bool isBusesLayoutSupported(const BusesLayout& layouts) const override;
#endif

	void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

	//==============================================================================
	juce::AudioProcessorEditor* createEditor() override;
	bool hasEditor() const override;

	//==============================================================================
	const juce::String getName() const override;

	bool acceptsMidi() const override;
	bool producesMidi() const override;
	bool isMidiEffect() const override;
	double getTailLengthSeconds() const override;

	//==============================================================================
	int getNumPrograms() override;
	int getCurrentProgram() override;
	void setCurrentProgram(int index) override;
	const juce::String getProgramName(int index) override;
	void changeProgramName(int index, const juce::String& newName) override;

	//==============================================================================
	void getStateInformation(juce::MemoryBlock& destData) override;
	void setStateInformation(const void* data, int sizeInBytes) override;


	//==============================================================================
	void loadAudioFile(std::function<void()> callback = []() {});
	void loadAudioFile(const juce::String& path);
	void loadAudioFile(const juce::File& file);
	juce::AudioBuffer<float>& getWaveForm() { return waveForm; };

	juce::String getFileName() { return currentAudioFile.getFileNameWithoutExtension(); }
	juce::String getFilePath() { return currentAudioFile.getFullPathName(); }
	juce::File getCurrentAudioFile() { return currentAudioFile; }
	void playAudio();
	void pauseAudio();
	bool isPlayingAudio();
	void clearAudio();

private:
	JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(VivoacAudioProcessor)
		//==============================================================================

		//==============================================================================
		juce::Synthesiser synth;
	const int numVoices = 1;
	juce::AudioFormatManager formatManager;
	std::unique_ptr<juce::AudioFormatReader> formatReader;
	juce::BigInteger midiRange;
	juce::AudioBuffer<float> waveForm;
	std::unique_ptr<juce::FileChooser> fileChooser;
	juce::File currentAudioFile;

};
