"use client"

import { useContext, useEffect, useState } from "react";
import { SettingsContext } from "@/components/settings-context";

import { z } from "zod";
import { ViVoAc_User } from "@/types/user";
import { Backend_Response } from "@/types/backend-response";

import UserForm from "@/components/forms/user-form";
import { PasswordInput } from "@/components/extra/password-input";

import { getCookie } from "cookies-next";

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
    }, [url, api_version, user_access_token]);

    if (loading) {
        return <div>Loading...</div>; // You can customize this loading UI
    }
    return (<> 
        {user &&
            <div className="w-full h-full flex justify-center items-center">
                <UserForm {...user} />
            </div>
        }
        </>
    );
}