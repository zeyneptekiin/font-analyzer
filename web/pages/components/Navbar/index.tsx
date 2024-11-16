"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
    const pathname = usePathname();

    return (
        <nav className="bg-slate-400 p-4 text-white h-[60px] absolute w-screen">
            <div className="max-w-7xl mx-auto flex gap-4">
                <Link
                    href="/"
                    className={`hover:underline font-semibold ${
                        pathname === "/" ? "text-black" : "text-white"
                    }`}
                >
                    Font Finder
                </Link>
                <Link
                    href="/generate"
                    className={`hover:underline font-semibold ${
                        pathname === "/generate" ? "text-black" : "text-white"
                    }`}
                >
                    Generate Text
                </Link>
            </div>
        </nav>
    );
}
