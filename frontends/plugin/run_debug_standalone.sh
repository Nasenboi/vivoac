#!/bin/bash

# Detect the operating system
OS="$(uname -s)"

case "$OS" in
    Linux*) 
        echo "Running on Linux"
        # Add Linux-specific executable if needed
        ;;
    Darwin*) 
        echo "Running on macOS"
        ./build/vivoac_plugin/ViVoAc_Plugin_artefacts/Standalone/ViVoAc_Plugin.app/Contents/MacOS/ViVoAc_Plugin
        ;;
    CYGWIN*|MINGW32*|MSYS*|MINGW*)
        echo "Running on Windows"
        start ./build/vivoac_plugin/ViVoAc_Plugin_artefacts/Debug/Standalone/ViVoAc_Plugin.exe
        ;;
    *)
        echo "Unknown OS"
        exit 1
        ;;
esac