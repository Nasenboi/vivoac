"use client"
import { Button } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Menu, CircleUser } from "lucide-react"
import Image from "next/image"
import Link from 'next/link'

import { hasCookie, getCookie } from "cookies-next";

import { useState, useEffect } from "react"

interface HeaderProps {
    isFixed: boolean;         // Prop for fixed positioning
    toggleSideBar: () => void; // Prop to toggle sidebar visibility
}

export default function Header({ isFixed = false, toggleSideBar }: HeaderProps) {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const cookie = hasCookie("user_access_token") ? getCookie("user_access_token") : null;

    useEffect(() => {
        setIsLoggedIn(cookie ? true : false);
    }, []);

    return (
        <div className={`shadow-lg dark:shadow-dark grid grid-cols-3 p-2 ${isFixed ? "fixed top-0 left-0 w-full z-10 bg-[hsl(var(--background))]" : ""}`}>
            <div className="col-span-1">
                {isFixed &&
                    <Button variant="outline" size="icon" onClick={toggleSideBar}>
                        <Menu />
                    </Button>
                }
            </div>
            <div className={`relative col-span-1 col-start-2 flex justify-evenly  ${isFixed ? "" : "h-9 min-w-full"}`}>
                <Link href="/home">
                    <Image src="/ViVoAc_Logo.png"
                        alt="ViVoAc Logo"
                        fill
                        sizes="(min-height: 6rem)"
                        className="object-contain"
                        unoptimized
                    />
                </Link>
            </div>
            <div className="col-span-1 flex justify-end">
                <DropdownMenu>
                    <DropdownMenuTrigger>
                        <div className={`rounded-full h-full w-full flex justify-evenly items-center ${isLoggedIn ? "bg-green-600" : "bg-red-600"}`} >
                            {isLoggedIn && hasCookie("user_username") &&
                                <h1 className="p-1 pl-2">
                                    {getCookie("user_username")}
                                </h1>
                            }
                            <CircleUser className="h-full w-full p-1" />
                        </div>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                        <DropdownMenuLabel>My Account</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <Link href={isLoggedIn ? "/logout" : "/login"}>
                            <DropdownMenuItem>
                                {isLoggedIn ? "Logout" : "Login"}
                            </DropdownMenuItem>
                        </Link>
                        <Link href="/user-info">
                            <DropdownMenuItem>
                                Info
                            </DropdownMenuItem>
                        </Link>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
        </div>
    );
}