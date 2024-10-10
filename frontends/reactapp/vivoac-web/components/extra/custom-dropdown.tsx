
import { useState } from "react"

import { Input } from "@/components/ui/input"

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


export default function CustomPopover({ popoverOptions, field, placeholder, allowCustomOption = true }) {
    const [popoverBoxOpen, setPopoverBoxOpen] = useState(false)
    const [useCustomOption, setUseCustomOption] = useState(false)


    return (
        <Popover open={popoverBoxOpen} onOpenChange={setPopoverBoxOpen}>
            <PopoverTrigger asChild>
                <Input
                    className="text-left"
                    placeholder={placeholder || "Select"}
                    readOnly
                    {...field}
                    value={popoverOptions.find(o => o.value === field.value)?.label || field.value} />
            </PopoverTrigger>
            <PopoverContent className="w-[200px] p-0" align="start">
                <Command>
                    <CommandInput placeholder="Search options..." />
                    <CommandList>
                        <CommandEmpty>No options found.</CommandEmpty>
                        {allowCustomOption &&
                            <CommandItem key={"custom"} className="border-b">
                                <Check
                                    className={cn(
                                        "mr-2 h-4 w-4",
                                        useCustomOption ? "opacity-100" : "opacity-0"
                                    )}
                                />
                                <Input
                                    className="border-0 p-2"
                                    placeholder="Custom gender"
                                    {...field}
                                    onChange={(e) => {
                                        field.onChange(e)
                                        setUseCustomOption(true)
                                    }}
                                />
                            </CommandItem>
                        }
                        <CommandGroup>
                            {popoverOptions.map((o) => (
                                <CommandItem
                                    key={o.value}
                                    value={o.value}
                                    onSelect={(currentValue) => {
                                        field.onChange(currentValue)
                                        setPopoverBoxOpen(false)
                                        setUseCustomOption(false)
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
                        </CommandGroup>
                    </CommandList>
                </Command>
            </PopoverContent>
        </Popover>
    );
}

