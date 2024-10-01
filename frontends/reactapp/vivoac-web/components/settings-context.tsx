"use client";
import { createContext, ReactNode, useState } from "react";
import initialSettings from '@/settings.json'; // Import initial settings from JSON

// Define the context with settings and updateSettings
export const SettingsContext = createContext({
    settings: initialSettings,
    updateSettings: (newSettings: any) => {}
});

interface SettingsProviderProps {
    children: ReactNode;
}

export default function SettingsProvider({ children }: SettingsProviderProps) {
    const [settings, setSettings] = useState(initialSettings);

    // Function to update settings state
    const updateSettings = (newSettings: any) => {
        setSettings((prevSettings) => ({ ...prevSettings, ...newSettings }));
    };

    return (
        <SettingsContext.Provider value={{ settings, updateSettings }}>
            {children}
        </SettingsContext.Provider>
    );
}