"use client";
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { hasCookie, getCookie } from "cookies-next";

export default function Index() {
  const router = useRouter();

  useEffect(() => {
    if (hasCookie("user_access_token")) {
      router.push('/home');
    }
    else {
      router.push('/login');
    }
  }, []);

  return(
    <>
    </>
  );
}