"use client";
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Index() {

  const router = useRouter();

  useEffect(() => {
    // Redirect to /home when the component mounts
    router.push('/home');
  }, [router]);

  return(
    <>
    </>
  );
}