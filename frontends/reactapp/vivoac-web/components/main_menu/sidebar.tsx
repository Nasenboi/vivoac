import { Map } from "lucide-react";

import Footer from "./footer";


export default function Sidebar({ isFixed = false }: { isFixed: boolean }) {
    return (
        <div className={`fixed flex flex-col min-w-[300px] p-4 min-h-full ${isFixed ? "" : "pt-16"}`}>
            <div className="w-full p-4 gap-4 flex">
                <Map size={32} />
                <h1 className="font-bold text-4xl">Navigation</h1>
            </div>
            <div className="grow">
                Menu
            </div>
            <Footer isFixed={false}/>
        </div>
    );
}