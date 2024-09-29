import { Map } from "lucide-react";

import {UserCog, UserPlus, Settings, Car, List, Speech} from "lucide-react"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
    CommandSeparator,
  } from "@/components/ui/command"

import Footer from "./footer";


export default function Sidebar({ isFixed = false }: { isFixed: boolean }) {
    return (
        <div className={`fixed flex flex-col min-w-[300px] p-4 min-h-full ${isFixed ? "" : "pt-16"}`}>
            <div className="w-full p-4 gap-4 flex">
                <Map size={32} />
                <h1 className="font-bold text-4xl">Navigation</h1>
            </div>
            <div className="grow">
                <Command>
                    <CommandInput placeholder="Type a command or search..." />
                    <CommandList className="max-h-full">
                        <CommandEmpty>No results found.</CommandEmpty>
                        <CommandGroup heading="Voice-Talents">
                            <CommandItem>
                                <List className="mr-2 h-4 w-4" />
                                <span>Voice-Talent List</span>
                            </CommandItem>
                            <CommandItem>
                                <UserPlus className="mr-2 h-4 w-4" />
                                <span>Add Voice-Talent</span>
                            </CommandItem>
                        </CommandGroup>
                        <CommandGroup heading="Voices">
                            <CommandItem>
                                <List className="mr-2 h-4 w-4" />
                                <span>Voice List</span>
                            </CommandItem>
                            <CommandItem>
                                <Speech className="mr-2 h-4 w-4" />
                                <span>Add Voice</span>
                            </CommandItem>
                        </CommandGroup>
                        <CommandGroup heading="Settings">
                            <CommandItem>
                                <Settings className="mr-2 h-4 w-4" />
                                <span>General</span>
                            </CommandItem>
                            <CommandItem>
                                <UserCog className="mr-2 h-4 w-4" />
                                <span>Users</span>
                            </CommandItem>
                            <CommandItem>
                                <Car className="mr-2 h-4 w-4" />
                                <span>Engines</span>
                            </CommandItem>
                        </CommandGroup>
                    </CommandList>
                </Command>
            </div>
            <Footer isFixed={false}/>
        </div>
    );
}