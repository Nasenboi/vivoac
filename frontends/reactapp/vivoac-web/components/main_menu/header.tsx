import { Button } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
  } from "@/components/ui/dropdown-menu"
import {Menu, CircleUser} from "lucide-react"
import Image from 'next/image'
import Link from 'next/link'

interface HeaderProps {
    isFixed: boolean;         // Prop for fixed positioning
    toggleSideBar: () => void; // Prop to toggle sidebar visibility
}

export default function Header({ isFixed = false, toggleSideBar }: HeaderProps) {

    return (
        <div className={`border-b-2 grid grid-cols-3 p-2 ${isFixed ? "fixed top-0 left-0 w-full z-10 bg-[hsl(var(--background))]" : ""}`}>
            <div className="col-span-1">
            {isFixed && 
                <Button variant="outline" size="icon" onClick={toggleSideBar}>
                    <Menu />
                </Button>
            }
            </div>
            <div className={`relative col-span-1 col-start-2 flex justify-evenly  ${isFixed ? "" : "h-9 min-w-full"}`}>
                <Image src={"/ViVoAc_Logo_1.0.png"}
                    alt="ViVoAc Logo"
                    fill
                    sizes="(min-height: 6rem)"
                    className="object-contain"
                />
            </div>
            <div className="col-span-1 flex justify-end">
                <DropdownMenu>
                    <DropdownMenuTrigger>
                        <CircleUser className="bg-red-600 rounded-full"/>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                        <DropdownMenuLabel>My Account</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>
                            <Link href="/login">Login</Link>
                        </DropdownMenuItem>
                        <DropdownMenuItem>Info</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
        </div>
    );
}