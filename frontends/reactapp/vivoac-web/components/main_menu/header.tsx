import { Button } from "@/components/ui/button"
import {Menu} from "lucide-react"
import Image from 'next/image'

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
            <div className={`relative col-span-1 col-start-2 flex justify-evenly  ${isFixed ? "" : "h-9"}`}>
                <Image src={"/ViVoAc_Logo_1.0.png"}
                    alt="ViVoAc Logo"
                    layout="fill"
                    objectFit="contain"
                />
            </div>
        </div>
    );
}