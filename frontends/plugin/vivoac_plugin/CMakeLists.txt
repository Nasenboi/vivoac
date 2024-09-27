cmake_minimum_required(VERSION 3.20)

juce_add_plugin(
    ${PROJECT_NAME}
    COMPANY_NAME "Christian_Boendgen"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    PLUGIN_MANUFACTURER_CODE RAIN
    PLUGIN_CODE AUPL
    FORMATS AU VST3 Standalone AAX
    PRODUCT_NAME "ViVoAc_Plugin"
    NEEDS_WEBVIEW2 TRUE
)

target_sources(${PROJECT_NAME}
    PRIVATE
        source/PluginProcessor.cpp
        source/PluginEditor.cpp
)

target_include_directories(${PROJECT_NAME}
    PRIVATE
        include
)

target_link_libraries(${PROJECT_NAME}
    PRIVATE
        juce::juce_audio_utils
    PUBLIC
        juce::juce_recommended_lto_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags
)

target_compile_definitions(${PROJECT_NAME}
    PUBLIC
        JUCE_WEB_BROWSER=1
        JUCE_USE_CURL=0
        JUCE_VST3_CAN_REPLACE_VST2=0
        JUCE_USE_WIN_WEBVIEW2_WITH_STATIC_LINKING=1
        JUCE_USE_WIN_WEBVIEW2=1
)

if (MSVC)
    target_compile_definitions(${PROJECT_NAME}
        PUBLIC
            JUCE_WINDOWS=1
            JUCE_USE_WIN_WEBVIEW2=1
        PRIVATE
            _SILENCE_CXX23_ALIGNED_STORAGE_DEPRECATION_WARNING
    )
endif()

# use this if the juce version should change from 8.0.1
# file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/../libs/juce/modules/juce_gui_extra/native/javascript/" DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}/../../reactapp/vivoac-web/juce/")

set(STATIC_WEBVIEW_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../../reactapp/vivoac-web/out")

if (MSVC)
    #set(COMMUN_APPLICATION_DIR "C:/Program Files/Common Files/${PROJECT_NAME}/")
    #set(VST3_DIR "C:/Program Files/Common Files/VST3/")
    #set(INSTALL_DIR "C:/Program Files/${PROJECT_NAME}/")
    #set(STANDALONE_DIR "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}_artefacts/${CMAKE_BUILD_TYPE}Debug/Standalone/ViVoAc_Plugin.exe")
    #set(VST3_BUILD "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}_artefacts/${CMAKE_BUILD_TYPE}VST3/Project.vst3")
elseif(APPLE)
    set(COMMUN_APPLICATION_DIR "Library/${PROJECT_NAME}")
    set(VST3_DIR "Library/Audio/Plug-Ins/VST3")
    set(INSTALL_DIR "Applications/${PROJECT_NAME}")
    set(STANDALONE_BUILD "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}_artefacts/${CMAKE_BUILD_TYPE}Standalone/${PROJECT_NAME}.app")
    set(VST3_BUILD "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}_artefacts/${CMAKE_BUILD_TYPE}VST3/${PROJECT_NAME}.vst3")
endif()

include("package.cmake")