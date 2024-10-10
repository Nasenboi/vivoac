"use client"

import { useContext, useEffect, useState } from "react";
import { SettingsContext } from "@/components/settings-context";

import { z } from "zod";
import { ViVoAc_Voice_Talent } from "@/types/voice-talent";

import VoiceTalentForm, {VoiceTalentFormSkeleton} from "@/components/forms/voice-talent-form";

import { getCookie } from "cookies-next";

import { ArrowRight } from "lucide-react";

export default function UserInfo() {
    const {settings, updateSettings} = useContext(SettingsContext);
    const [loading, setLoading] = useState(true);
    const [voice_talent, setVoiceTalent] = useState<z.infer<typeof ViVoAc_Voice_Talent> | null>(null);
    const user_access_token = getCookie("user_access_token");
    const api_version = settings.API_VERSION;
    const url = settings.BACKEND_SERVER_URL;

    return (<> 
        <div className="w-full h-full max-h-full overflow-y-auto">
            <div className="w-full flex items-center justify-center gap-3">
                <VoiceTalentForm {...voice_talent} />
            </div>
        </div>
        </>
    );
}