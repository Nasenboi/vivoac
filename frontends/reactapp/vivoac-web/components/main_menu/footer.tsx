

export default function Footer({ isFixed = false }: { isFixed: boolean }) {
    return (
        <div className={`flex justify-evenly ${isFixed ? "fixed bottom-0 left-0 w-full z-10 h-15 bg-[hsl(var(--background))]" : ""}`}>
            <p>ViVoAc ©2024</p>
        </div>
    );
}