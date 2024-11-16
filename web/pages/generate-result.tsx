import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Navbar from "@/pages/components/Navbar";

export default function GenerateResultPage() {
    const router = useRouter();
    const [fontSrc, setFontSrc] = useState<string | null>(null);

    useEffect(() => {
        // Router hazırsa font parametresini kontrol edin
        if (router.isReady && router.query.font) {
            setFontSrc(router.query.font as string);
        }
    }, [router.isReady, router.query.font]);

    if (!fontSrc) {
        return <div>Loading...</div>;
    }

    return (
        <>
            <Navbar />
            <div className="flex flex-col justify-center items-center min-h-screen">
                <h1 className="text-4xl mb-6">Generated Font Download</h1>

                {/* Yazı tipi dosyasını indirme bağlantısı */}
                <a
                    href={fontSrc}
                    download="generated_font.ttf"
                    className="mt-4 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                >
                    Download Font (.ttf)
                </a>

                {/* Geri dönme butonu */}
                <button
                    onClick={() => router.push('/generate')}
                    className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                    Go Back
                </button>
            </div>
        </>
    );
}
