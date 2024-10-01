"use client"
import React, { useState, useEffect } from 'react';

import Header from "@/components/main_menu/header";
import Sidebar from "@/components/main_menu/sidebar";
import Footer from "@/components/main_menu/footer";

export default function Layout({children}: {children: React.ReactNode}) {
    const [isSidebarFixedLeft, setIsSidebarFixedLeft] = useState(true);
    const [showSideBar, setShowSideBar] = useState(false);

    // Update the state when the screen is resized
    useEffect(() => {
        const handleResize = () => {
        if (window.innerWidth < 1024) {
            setShowSideBar(false);
            setIsSidebarFixedLeft(false);
        } else {
            setShowSideBar(false);
            setIsSidebarFixedLeft(true);
        }
        };
        handleResize();
        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    return (
        <section className="flex items-start justify-between w-full h-screen">
            {(isSidebarFixedLeft || !isSidebarFixedLeft && showSideBar) && (
                <div className="min-w-[300px] min-h-screen">
                    <Sidebar isFixed={isSidebarFixedLeft}/>
                </div>
            )}
            <main className="w-full h-full overflow-y-hidden">
                <Header isFixed={!isSidebarFixedLeft} toggleSideBar={() => setShowSideBar(prevState => !prevState)} />
                <div className={`p-4 h-full ${isSidebarFixedLeft ? "" : "pt-16"}`}>
                    {children}
                </div>
                {!isSidebarFixedLeft  && !showSideBar && (
                    <Footer isFixed={true}/>
                )}
            </main>
        </section>
    );
}