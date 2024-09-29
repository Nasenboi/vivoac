
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Home',
};

export default function Home() {

    return(
      <div className="flex flex-col">
        <h1 className="font-bold text-2xl flex justify-center">Virtual Voice Actors</h1>
        <p>Create and generate script lines via neural speech synthesis for your localization projects.</p>
      </div>
    );
}