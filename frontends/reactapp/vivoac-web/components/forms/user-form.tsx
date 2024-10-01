"use client"


import * as z from 'zod';
import { zodResolver } from "@hookform/resolvers/zod"
import { useState, useContext } from "react"
import { useForm, FieldErrors } from "react-hook-form"

import { getCookie } from "cookies-next"

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
import { Skeleton } from "@/components/ui/skeleton"

import { PasswordInput } from '../extra/password-input';

import { AlertCircle } from "lucide-react"
import {
    Alert,
    AlertDescription,
    AlertTitle,
} from "@/components/ui/alert"

import { ViVoAc_User } from "@/types/user";
import { Backend_Response } from "@/types/backend-response";

import { SettingsContext } from "@/components/settings-context";

const ViVoAc_User_Schema = ViVoAc_User.extend({
    confirm_password: z.string().optional(),
}).refine((data) => data.password === data.confirm_password, {
    message: "Passwords must match",
    path: ["confirmPassword"], // Error will be shown on confirmPassword field
});

async function updateUser(url, api_version, user): Promise<z.infer<typeof ViVoAc_User> | string | null> {
    const route = "/user/crud/";
    const access_token = getCookie("user_access_token");
    const headers = {
        "Authorization": `Bearer ${access_token}`,
        "api-version": api_version,
        "Content-Type": "application/json",
    };

    try {
        const keys_to_remove = ['created_at', 'updated_at', '_id', 'confirm_password'];
        const user_to_send = JSON.stringify(user, (key, value) => {
            if (value !== null && value !== undefined && !keys_to_remove.includes(key)) {
                return value;
            }
        });
        console.log(user_to_send);
        const response = await fetch(`${url}${route}${user._id}`, {
            method: 'PUT',
            headers: headers,
            body: user_to_send,
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
        return error;
    }
}

export function UserFormSkeleton() {

    return (
        <div className="grid grid-cols-5 gap-4 justify-center items-center">
            <div className="space-y-8 col-span-3 col-start-2 border-2 rounded-lg p-4">
                <Skeleton className="h-5 w-full" />
                <div className="flex gap-4">
                    <Skeleton className="h-5 w-full" />
                    <Skeleton className="h-5 w-full" />
                </div>
                <div className="flex gap-4">
                    <Skeleton className="h-5 w-full" />
                    <Skeleton className="h-5 w-full" />
                </div>
                <Skeleton className="h-5 w-full" />
            </div>
        </div>
    );
}

export default function UserForm(user: z.infer<typeof ViVoAc_User>) {
    const { settings, updateSettings } = useContext(SettingsContext);
    const [error, setError] = useState<string | FieldErrors | null>(null);

    const form = useForm<z.infer<typeof ViVoAc_User_Schema>>({
        resolver: zodResolver(ViVoAc_User_Schema),
        defaultValues: {
            ...user,
        },
    })

    function onSubmit(values: z.infer<typeof ViVoAc_User_Schema>) {
        setError(null)

        updateUser(settings.BACKEND_SERVER_URL, settings.API_VERSION, values).then((data) => {
            console.log(data);
            if (typeof data === 'string') {
                setError(data);
            }
        });
    }

    return (<div className="flex flex-col gap-4 justify-center items-center">
        {error &&
            <Alert variant="destructive" className="bg-red-50 dark:bg-red-400">
                <AlertCircle />
                <AlertTitle className="font-bold text-2xl">
                    Error
                </AlertTitle>
                <AlertDescription>
                    {typeof error === "string" ? (
                        error
                    ) : (
                        // Map over the FieldErrors object to display error messages for each field
                        Object.entries(error).map(([fieldName, fieldError]) => (
                            <div key={fieldName}>
                                <h1 className="font-bold">{fieldName}</h1>
                                <p>{JSON.stringify(fieldError?.message)}</p>
                            </div>
                        ))
                    )}
                </AlertDescription>
            </Alert>
        }
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit, (e) => { setError(e) })} className="space-y-8 border-2 rounded-lg p-4">
                <FormField
                    control={form.control}
                    name="username"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                                <Input placeholder="username" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <div className="flex gap-4">
                    <FormField
                        control={form.control}
                        name="password"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Password</FormLabel>
                                <FormControl>
                                    <PasswordInput {...field} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="confirm_password"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Confirm Password</FormLabel>
                                <FormControl>
                                    <PasswordInput {...field} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                </div>
                <div className="flex gap-4">
                    <div className="w-full">
                        <FormField
                            control={form.control}
                            name="first_name"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>First Name</FormLabel>
                                    <FormControl>
                                        <Input placeholder="first name" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                    </div>
                    <div className="w-full">
                        <FormField
                            control={form.control}
                            name="last_name"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Last Name</FormLabel>
                                    <FormControl>
                                        <Input placeholder="last name" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                    </div>
                </div>
                <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>E-Mail</FormLabel>
                            <FormControl>
                                <Input placeholder="e-mail" {...field} />
                            </FormControl>
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