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

export default function ApiSettings() {

    const {settings, updateSettings} = useContext(SettingsContext);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        updateSettings({ API_KEY: e.target.value }); // Update settings with new backend URL
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>API Settings</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex flex-col gap-2">
                    <Label htmlFor="api_key">API Key</Label>
                    <Input
                        type="text"
                        id="api_key"
                        placeholder="API Key"
                        onChange={handleInputChange} // Update value on input change
                        value={settings.API_KEY} // Bind the input value to the settings state
                    />
                </div>
            </CardContent>
        </Card>
    );
}