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

import { Check, ChevronsUpDown } from "lucide-react"
import { cn } from "@/lib/utils"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "@/components/ui/command"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"

import { AlertCircle } from "lucide-react"
import {
    Alert,
    AlertDescription,
    AlertTitle,
} from "@/components/ui/alert"

import { ViVoAc_Voice_Talent, ViVoAc_Voice_Talent_Gender_Options } from "@/types/voice-talent";
import { Backend_Response } from "@/types/backend-response";

import { SettingsContext } from "@/components/settings-context";


const ViVoAc_Voice_Talent_Schema = ViVoAc_Voice_Talent;

async function updateVoiceTalent(url, api_version, voice_talent): Promise<z.infer<typeof ViVoAc_Voice_Talent> | string | null> {
    const route = "/voice_talent/crud/";
    const access_token = getCookie("user_access_token");
    const headers = {
        "Authorization": `Bearer ${access_token}`,
        "api-version": api_version,
        "Content-Type": "application/json",
    };

    try {
        const keys_to_remove = ['created_at', 'updated_at', '_id'];
        const voice_talent_to_send = JSON.stringify(voice_talent, (key, value) => {
            if (value !== null && value !== undefined && !keys_to_remove.includes(key)) {
                return value;
            }
        });
        console.log(voice_talent_to_send);
        const response = await fetch(`${url}${route}${voice_talent._id}`, {
            method: 'PUT',
            headers: headers,
            body: voice_talent_to_send,
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

export function VoiceTalentFormSkeleton() {

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

export default function VoiceTalentForm(voice_talent: z.infer<typeof ViVoAc_Voice_Talent>) {
    const { settings, updateSettings } = useContext(SettingsContext);
    const [error, setError] = useState<string | FieldErrors | null>(null);
    const [useCustomGender, setUseCustomGender] = useState(false)
    const [genderBoxOpen, setGenderBoxOpen] = useState(false)

    const form = useForm<z.infer<typeof ViVoAc_Voice_Talent_Schema>>({
        resolver: zodResolver(ViVoAc_Voice_Talent_Schema),
        defaultValues: {
            ...voice_talent,
        },
    })

    function onSubmit(values: z.infer<typeof ViVoAc_Voice_Talent_Schema>) {
        setError(null)

        updateVoiceTalent(settings.BACKEND_SERVER_URL, settings.API_VERSION, values).then((data) => {
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
                <FormField
                    control={form.control}
                    name="gender"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Gender</FormLabel>
                            <FormControl>
                                <Popover open={genderBoxOpen} onOpenChange={setGenderBoxOpen}>
                                    <PopoverTrigger asChild>
                                        <Input
                                            placeholder="Select"
                                            readOnly
                                            {...field}
                                            value={ViVoAc_Voice_Talent_Gender_Options.find(o => o.value === field.value)?.label || field.value} />
                                    </PopoverTrigger>
                                    <PopoverContent className="w-[200px] p-0">
                                        <Command>
                                            <CommandInput placeholder="Search gender options..." />
                                            <CommandList>
                                                <CommandEmpty>No gender options found.</CommandEmpty>
                                                <CommandGroup>
                                                    {ViVoAc_Voice_Talent_Gender_Options.map((o) => (
                                                        <CommandItem
                                                            key={o.value}
                                                            value={o.value}
                                                            onSelect={(currentValue) => {
                                                                field.onChange(currentValue)
                                                                setGenderBoxOpen(false)
                                                                setUseCustomGender(false)
                                                            }}
                                                        >
                                                            <Check
                                                                className={cn(
                                                                    "mr-2 h-4 w-4",
                                                                    field.value === o.value ? "opacity-100" : "opacity-0"
                                                                )}
                                                            />
                                                            {o.label}
                                                        </CommandItem>
                                                    ))}
                                                    <CommandItem key={"custom"}>
                                                        <Check
                                                            className={cn(
                                                                "mr-2 h-4 w-4",
                                                                useCustomGender ? "opacity-100" : "opacity-0"
                                                            )}
                                                        />
                                                        <Input
                                                            className="border-0 p-2"
                                                            placeholder="Custom gender"
                                                            onSubmit={(value) => {
                                                                setUseCustomGender(true)
                                                                setGenderBoxOpen(false)
                                                            }}
                                                            {...field}
                                                        />
                                                    </CommandItem>
                                                </CommandGroup>
                                            </CommandList>
                                        </Command>
                                    </PopoverContent>
                                </Popover>
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