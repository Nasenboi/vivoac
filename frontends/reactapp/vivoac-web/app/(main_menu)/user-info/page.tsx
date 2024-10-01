"use client"

import { useContext, useEffect, useState } from "react";
import { SettingsContext } from "@/components/settings-context";

import { z } from "zod";
import { ViVoAc_User } from "@/types/user";
import { Backend_Response } from "@/types/backend-response";

import UserForm, {UserFormSkeleton} from "@/components/forms/user-form";

import { getCookie } from "cookies-next";

import { ArrowRight } from "lucide-react";

async function fetchUserInfo(url, api_version): Promise<z.infer<typeof ViVoAc_User> | null> {
    const route = "/user/self";
    const access_token = getCookie("user_access_token");
    const headers = {
        "Authorization": `Bearer ${access_token}`,
        "api-version": api_version
    };

    try {
        const response = await fetch(`${url}${route}`, {
            method: 'GET',
            headers: headers
        });

        // Check if the response is OK (status code 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Backend_Response is a zod schema
        //const data = await response.json();
        const data = Backend_Response.parse(await response.json());
        
        return data.data;
    } catch (error) {
        // Handle errors gracefully
        console.error(error);
        return null;
    }

}

export default function UserInfo() {
    const {settings, updateSettings} = useContext(SettingsContext);
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState<z.infer<typeof ViVoAc_User> | null>(null);
    const user_access_token = getCookie("user_access_token");
    const api_version = settings.API_VERSION;
    const url = settings.BACKEND_SERVER_URL;

    useEffect(() => {
        fetchUserInfo(url, api_version).then((data) => {
            console.log(data);
            setUser(data);
            setLoading(false);
        });
    }, []);


    return (<> 
        {user &&
            <div className="w-full h-full max-h-full overflow-y-auto">
                <div className="w-full flex items-center justify-center gap-3">
                    <h1 className="font-bold text-3xl hidden md:block">
                        {"This is you"}
                    </h1>
                    <ArrowRight className="w-9 h-9 hidden md:block" />
                    <UserForm {...user} />
                </div>
            </div>
        }
        </>
    );
}