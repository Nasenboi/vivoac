"use client"
import { useContext } from "react";
import { SettingsContext } from "@/components/settings-context";
import BackendSettings from "@/components/main_menu/settings/backend-settings";
import ApiSettings from "@/components/main_menu/settings/api-settings";

import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"


import ThemeButton from "@/components/main_menu/settings/theme-button"

export default function Settings() {
    const settings = useContext(SettingsContext);


    return (
        <div className="w-full h-full max-h-full overflow-y-auto flex">
            <div className="w-full flex flex-wrap justify-center gap-4">
                <div className="grow min-w-[250px]">
                    <BackendSettings />
                </div>
                <div className="grow min-w-[250px]">
                    <ApiSettings />
                </div>
                <div className="grid grid-rows-3">
                    <Card className="flex justify-center items-center p-2">
                        <ThemeButton />
                    </Card>
                </div>
            </div>
        </div>
    );
}