"use client"
import { useContext } from "react";
import { SettingsContext } from "@/components/settings-context";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function BackendSettings() {

    const {settings, updateSettings} = useContext(SettingsContext);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        updateSettings({ BACKEND_SERVER_URL: e.target.value }); // Update settings with new backend URL
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>Backend Settings</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex flex-col gap-2">
                    <Label htmlFor="backend_url">Backend URL</Label>
                    <Input
                        type="text"
                        id="backend_url"
                        placeholder="Backend URL"
                        onChange={handleInputChange} // Update value on input change
                        value={settings.BACKEND_SERVER_URL} // Bind the input value to the settings state
                    />
                </div>
            </CardContent>
        </Card>
    );
}