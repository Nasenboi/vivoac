/*
  ==============================================================================

	This file contains the basic framework code for a JUCE plugin processor.

  ==============================================================================
*/

#include "PluginEditor.h"
#include "PluginProcessor.h"

//==============================================================================
VivoacAudioProcessor::VivoacAudioProcessor()
#ifndef JucePlugin_PreferredChannelConfigurations
	: AudioProcessor(BusesProperties()
#if ! JucePlugin_IsMidiEffect
#if ! JucePlugin_IsSynth
		.withInput("Input", juce::AudioChannelSet::stereo(), true)
#endif
		.withOutput("Output", juce::AudioChannelSet::stereo(), true)
#endif
	)
#endif
{
	// Add voices to the sampler
	for (int i = 0; i < numVoices; ++i) {
		synth.addVoice(new juce::SamplerVoice());
	}
	formatManager.registerBasicFormats();
	midiRange.setRange(0, 128, true);
	clearAudio();
}

VivoacAudioProcessor::~VivoacAudioProcessor()
{
	formatReader = nullptr;
	fileChooser = nullptr;
}

//==============================================================================
const juce::String VivoacAudioProcessor::getName() const
{
	return JucePlugin_Name;
}

bool VivoacAudioProcessor::acceptsMidi() const
{
#if JucePlugin_WantsMidiInput
	return true;
#else
	return false;
#endif
}

bool VivoacAudioProcessor::producesMidi() const
{
#if JucePlugin_ProducesMidiOutput
	return true;
#else
	return false;
#endif
}

bool VivoacAudioProcessor::isMidiEffect() const
{
#if JucePlugin_IsMidiEffect
	return true;
#else
	return false;
#endif
}

double VivoacAudioProcessor::getTailLengthSeconds() const
{
	return 0.0;
}

int VivoacAudioProcessor::getNumPrograms()
{
	return 1;   // NB: some hosts don't cope very well if you tell them there are 0 programs,
	// so this should be at least 1, even if you're not really implementing programs.
}

int VivoacAudioProcessor::getCurrentProgram()
{
	return 0;
}

void VivoacAudioProcessor::setCurrentProgram(int index)
{
}

const juce::String VivoacAudioProcessor::getProgramName(int index)
{
	return {};
}

void VivoacAudioProcessor::changeProgramName(int index, const juce::String& newName)
{
}

//==============================================================================
void VivoacAudioProcessor::prepareToPlay(double sampleRate, int samplesPerBlock)
{
	synth.setCurrentPlaybackSampleRate(sampleRate);
}

void VivoacAudioProcessor::releaseResources()
{
	// When playback stops, you can use this as an opportunity to free up any
	// spare memory, etc.
}

#ifndef JucePlugin_PreferredChannelConfigurations
bool VivoacAudioProcessor::isBusesLayoutSupported(const BusesLayout& layouts) const
{
#if JucePlugin_IsMidiEffect
	juce::ignoreUnused(layouts);
	return true;
#else
	// This is the place where you check if the layout is supported.
	// In this template code we only support mono or stereo.
	// Some plugin hosts, such as certain GarageBand versions, will only
	// load plugins that support stereo bus layouts.
	if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::mono()
		&& layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
		return false;

	// This checks if the input layout matches the output layout
#if ! JucePlugin_IsSynth
	if (layouts.getMainOutputChannelSet() != layouts.getMainInputChannelSet())
		return false;
#endif

	return true;
#endif
}
#endif

void VivoacAudioProcessor::processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
	juce::ScopedNoDenormals noDenormals;
	auto totalNumInputChannels = getTotalNumInputChannels();
	auto totalNumOutputChannels = getTotalNumOutputChannels();

	for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
		buffer.clear(i, 0, buffer.getNumSamples());

	try {
		synth.renderNextBlock(
			buffer, midiMessages, 0, buffer.getNumSamples()
		);
	}
	catch (const std::exception& e) {
		// no sound it is!
		DBG(e.what());
	}

};

//==============================================================================
bool VivoacAudioProcessor::hasEditor() const
{
	return true; // (change this to false if you choose to not supply an editor)
}

juce::AudioProcessorEditor* VivoacAudioProcessor::createEditor()
{
	return new VivoacAudioProcessorEditor(*this);
}

//==============================================================================
void VivoacAudioProcessor::getStateInformation(juce::MemoryBlock& destData)
{
	// You should use this method to store your parameters in the memory block.
	// You could do that either as raw data, or use the XML or ValueTree classes
	// as intermediaries to make it easy to save and load complex data.
}

void VivoacAudioProcessor::setStateInformation(const void* data, int sizeInBytes)
{
	// You should use this method to restore your parameters from this memory block,
	// whose contents will have been created by the getStateInformation() call.
}

//==============================================================================
// This creates new instances of the plugin..
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
	return new VivoacAudioProcessor();
}


//==============================================================================
bool VivoacAudioProcessor::isPlayingAudio() {
	juce::SynthesiserVoice* v = synth.getVoice(0);

	return v->isVoiceActive();
}

void VivoacAudioProcessor::playAudio() {
	synth.noteOn(0, 60, 1.0f);
}

void VivoacAudioProcessor::pauseAudio() {
	synth.allNotesOff(0, false);
}

void VivoacAudioProcessor::clearAudio() {
	try {
		synth.clearSounds();
		currentAudioFile = juce::File{};
		waveForm.setSize(1, 0);
		pauseAudio();
	}
	catch (const std::exception& e) {
		// Something really bad happened! oopsie
		DBG(e.what());
	}
}

void VivoacAudioProcessor::loadAudioFile(std::function<void()> callback) {
	fileChooser = std::make_unique<juce::FileChooser>("Please select an audio file");

	synth.clearSounds();
	auto folderChooserFlags = juce::FileBrowserComponent::openMode | juce::FileBrowserComponent::canSelectFiles;

	fileChooser->launchAsync(folderChooserFlags, [this, callback](const juce::FileChooser& chooser) {
		juce::File file = chooser.getResult();

		if (file != juce::File{}) {
			loadAudioFile(file);

			if (callback) {
				callback();
			}
		}
		});
}

void VivoacAudioProcessor::loadAudioFile(const juce::String& path) {
	loadAudioFile(juce::File{ path });
}

void VivoacAudioProcessor::loadAudioFile(const juce::File& file) {
	if (!file.existsAsFile()) {
		return;
	}
	juce::WildcardFileFilter filter{ formatManager.getWildcardForAllFormats(), {}, {} };
	if (!filter.isFileSuitable(file)) {
		return;
	}
	try {
		synth.clearSounds();
		currentAudioFile = juce::File{ file };
		formatReader.reset(formatManager.createReaderFor(currentAudioFile));

		if (!formatReader) {
			clearAudio();
			return;
		}

		synth.addSound(new juce::SamplerSound(
			"sample", *formatReader, midiRange, 60, 0.1, 0.1, 30.0
		));

		const int numSamples = static_cast<int>(formatReader->lengthInSamples);
		waveForm.setSize(1, numSamples);
		formatReader->read(
			&waveForm, 0, numSamples, 0, true, false
		);
		//normalize:
		const float maxValue = waveForm.findMinMax(0, 0, waveForm.getNumSamples()).getEnd();
		auto writeBuffer = waveForm.getWritePointer(0);
		for (int s = 0; s < waveForm.getNumSamples(); ++s) {
			writeBuffer[s] = writeBuffer[s] / maxValue;
		}
	}
	catch (const std::exception& e) {
		DBG(e.what());
		clearAudio();
	}
}