"use client"
import React, { useState, useEffect } from 'react';

import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';

import Header from "@/components/main_menu/header";
import Sidebar from "@/components/main_menu/sidebar";
import Footer from "@/components/main_menu/footer";

export default function Layout({children}: {children: React.ReactNode}) {
    const [isSidebarFixedLeft, setIsSidebarFixedLeft] = useState(true);
    const [showSideBar, setShowSideBar] = useState(false);
    const router = useRouter();
    const {data: session} = useSession();

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

    useEffect(() => {
        // Redirect to /home when the component mounts
        console.log(session);
        if (session) {
          router.push('/home');
        }
        else {
          router.push('/login');
        }
    }, [session]);

    return (
        <section className="flex items-start justify-between w-full">
            {(isSidebarFixedLeft || !isSidebarFixedLeft && showSideBar) && (
                <div className="min-w-[300px] border-r-2 min-h-screen">
                    <Sidebar isFixed={isSidebarFixedLeft}/>
                </div>
            )}
            <main className="w-full">
                <Header isFixed={!isSidebarFixedLeft} toggleSideBar={() => setShowSideBar(prevState => !prevState)} />
                <div className={`p-4 ${isSidebarFixedLeft ? "" : "pt-16"}`}>
                    {children}
                </div>
                {!isSidebarFixedLeft  && !showSideBar && (
                    <Footer isFixed={true}/>
                )}
            </main>
        </section>
    );
}