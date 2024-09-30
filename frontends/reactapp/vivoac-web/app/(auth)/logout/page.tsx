"use client"
import { Button } from '@/components/ui/button';
import { Power } from 'lucide-react';
import Image from 'next/image'
import { useRouter } from 'next/navigation';

import { deleteCookie } from "cookies-next";

export default function Logout() {
    const router = useRouter();

    const handleLogout = async () => {
        // remove token from cookies
        deleteCookie("user_access_token");
        deleteCookie("user_token_type");
        deleteCookie("user_username");
        router.push('/');
    }

    return (
        <div className="h-screen min-h-full w-full flex flex-col justify-center items-center">
            <div className="relative min-h-[100px] w-[300px]">
                <Image src={"/ViVoAc_Logo_1.0.png"}
                    alt="ViVoAc Logo"
                    fill
                    sizes="(min-height: 6rem)"
                    className="object-contain"
                />
            </div>

            <div className="flex flex-col p-4 justify-between items-center">
                <h1 className="font-bold text-2xl p-4 gap-4">Are you sure you want to logout?</h1>
                <div>
                    <Button onClick={handleLogout}  className="w-[150px]" variant="destructive">
                        <Power />
                        <h1 className="pl-4">Logout</h1>
                    </Button>
                </div>
            </div>
        </div>
    );
}