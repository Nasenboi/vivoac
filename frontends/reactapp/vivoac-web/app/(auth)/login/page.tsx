"use client"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { useRouter } from "next/navigation"
import { useContext } from "react";
import { SettingsContext } from "@/components/settings-context";

import { Button } from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

import Image from 'next/image'

import { setCookie } from "cookies-next";


import { LoginSchema } from "./models"
import { PasswordInput } from "@/components/extra/password-input"

async function login(values, url): Promise<{ access_token: string, token_type: string } | null> {
    const authentication_creds = new URLSearchParams({
        username: values.username,
        password: values.password,
    });


    try {
        // env var BACKEND_SERVER_URL
        const backend_url = url;
        const response = await fetch(`${backend_url}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: authentication_creds.toString(),  // URL-encoded form data
        });

        // Check if the response is OK (status code 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        setCookie("user_access_token", data.access_token);
        setCookie("user_token_type", data.token_type);
        setCookie("user_username", values.username);

        return data;
    } catch (error) {
        // Handle errors gracefully
        console.error('Error:', error);
    }
    return null;
}

export default function Login() {
    const router = useRouter()
    const { settings, updateSettings } = useContext(SettingsContext);
    const form = useForm<z.infer<typeof LoginSchema>>({
        resolver: zodResolver(LoginSchema),
        defaultValues: {
            username: "",
            password: "",
        },
    })

    async function onSubmit(values: z.infer<typeof LoginSchema>) {
        try {
            // add token to cookies
            const token = await login(values, settings.BACKEND_SERVER_URL);
            router.push("/home");
        } catch (error) {
            console.error("Login failed:", error);
        }
    }

    return (
        <div className="h-screen min-h-full w-full flex flex-col justify-center items-center">
            <div className="relative min-h-[100px] w-[300px]">
                <Image src="/ViVoAc_Logo.png"
                    alt="ViVoAc Logo"
                    fill
                    sizes="(min-height: 6rem)"
                    className="object-contain"
                    unoptimized
                />
            </div>
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                    <FormField
                        control={form.control}
                        name="username"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Username</FormLabel>
                                <FormControl>
                                    <Input placeholder="username" {...field} />
                                </FormControl>
                                <FormDescription>
                                    The username of your account.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="password"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Password</FormLabel>
                                <FormControl>
                                    <PasswordInput placeholder="password" {...field} />
                                </FormControl>
                                <FormDescription>
                                    Your password.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <Button type="submit">Submit</Button>
                </form>
            </Form>
        </div>
    );
}