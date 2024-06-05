/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin processor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
VivoacAudioProcessor::VivoacAudioProcessor()
#ifndef JucePlugin_PreferredChannelConfigurations
     : AudioProcessor (BusesProperties()
                     #if ! JucePlugin_IsMidiEffect
                      #if ! JucePlugin_IsSynth
                       .withInput  ("Input",  juce::AudioChannelSet::stereo(), true)
                      #endif
                       .withOutput ("Output", juce::AudioChannelSet::stereo(), true)
                     #endif
                       ), apvts(*this, nullptr, "Parameters", createParameters())
#endif
{
    // Add voices to the sampler
    for (int i = 0; i < numVoices; ++i) {
        synth.addVoice(new juce::SamplerVoice());
    }
    formatManager.registerBasicFormats();
    midiRange.setRange(0, 128, true);
}

VivoacAudioProcessor::~VivoacAudioProcessor()
{
    formatReader = nullptr;
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

void VivoacAudioProcessor::setCurrentProgram (int index)
{
}

const juce::String VivoacAudioProcessor::getProgramName (int index)
{
    return {};
}

void VivoacAudioProcessor::changeProgramName (int index, const juce::String& newName)
{
}

//==============================================================================
void VivoacAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    synth.setCurrentPlaybackSampleRate(sampleRate);
}

void VivoacAudioProcessor::releaseResources()
{
    // When playback stops, you can use this as an opportunity to free up any
    // spare memory, etc.
}

#ifndef JucePlugin_PreferredChannelConfigurations
bool VivoacAudioProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
  #if JucePlugin_IsMidiEffect
    juce::ignoreUnused (layouts);
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

    synth.renderNextBlock(
        buffer, midiMessages, 0, buffer.getNumSamples()
    );
};

//==============================================================================
bool VivoacAudioProcessor::hasEditor() const
{
    return true; // (change this to false if you choose to not supply an editor)
}

juce::AudioProcessorEditor* VivoacAudioProcessor::createEditor()
{
    return new VivoacAudioProcessorEditor (*this);
}

//==============================================================================
void VivoacAudioProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    // You should use this method to store your parameters in the memory block.
    // You could do that either as raw data, or use the XML or ValueTree classes
    // as intermediaries to make it easy to save and load complex data.
}

void VivoacAudioProcessor::setStateInformation (const void* data, int sizeInBytes)
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
japvts::ParameterLayout VivoacAudioProcessor::createParameters() {
    std::vector<std::unique_ptr<juce::RangedAudioParameter>> p;

    // p.push_back(std::make_unique<juce::Type>("KEY", "Name", opts));

    return { p.begin(), p.end() };
}

//==============================================================================
void VivoacAudioProcessor::loadAudioFile() {
    juce::FileChooser fileChooser = { "Please choose an audio file!" };

    synth.clearSounds();
    if (fileChooser.browseForFileToOpen()) {
        juce::File file = fileChooser.getResult();
        formatReader.reset(formatManager.createReaderFor(file));
    }
    synth.addSound(new juce::SamplerSound(
        "sample", *formatReader, midiRange, 60, 0.1, 0.1, 30.0
    ));
}

void VivoacAudioProcessor::loadAudioFile(const juce::String& path) {
    synth.clearSounds();

    juce::File audioFile{ path };
    formatReader.reset(formatManager.createReaderFor(audioFile));
    
    synth.addSound(new juce::SamplerSound(
        "sample", *formatReader, midiRange, 60, 0.1, 0.1, 30.0
    ));
}