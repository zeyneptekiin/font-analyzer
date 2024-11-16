import { useState, ChangeEvent, FormEvent } from 'react';
import { useRouter } from 'next/router';
import { generateFontWithImage } from '@/pages/api/generateText';
import Navbar from "@/pages/components/Navbar";

export default function GenerateTextPage() {
    const [file, setFile] = useState<File | null>(null);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        const uploadedFile = e.target.files ? e.target.files[0] : null;
        setFile(uploadedFile);
        setError(null);
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        if (!file) {
            setError("Please upload an image file.");
            return;
        }

        try {
            const result = await generateFontWithImage(file);
            await router.push({
                pathname: "/generate-result",
                query: { image: result },
            });
        } catch (error) {
            console.error("Failed to generate font preview image", error);
            setError("Failed to generate font preview image. Please try again.");
        }
    };

    return (
        <>
            <Navbar />
            <div className="flex flex-col justify-center text-center">
                <h1 className="text-center mt-40 text-4xl">Generate Text with Custom Font</h1>
                <div className="text-left w-[500px] mt-10 py-20 border-2 rounded-2xl hover:border-gray-600 pl-20 mx-auto">
                    <h2>Upload an Image File</h2>
                    <form onSubmit={handleSubmit} className="mt-4">
                        <input
                            type="file"
                            onChange={handleFileChange}
                            accept="image/*"
                            placeholder="Upload an image"
                        />
                        <button type="submit" className="block mt-4">Generate Font Preview</button>
                    </form>
                    {error && <p className="mt-4 text-red-600">{error}</p>}
                </div>
            </div>
        </>
    );
}
