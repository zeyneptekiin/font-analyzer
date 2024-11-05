import { useState, ChangeEvent, FormEvent } from 'react';
import { useRouter } from 'next/router';
import { analyzeImage } from '@/pages/api/getFonts';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const router = useRouter();

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = e.target.files ? e.target.files[0] : null;
    setFile(uploadedFile);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!file) return;

    try {
      const result = await analyzeImage(file);
      await router.push({
        pathname: "/result",
        query: {data: JSON.stringify(result)},
      });
    } catch (error) {
      console.error("Failed to process image", error);
    }
  };

  return (
      <div className="flex flex-col justify-center text-center">
        <h1 className="text-center mt-40 text-4xl">Welcome to Font Analyzer!</h1>
        <div className="text-left w-[500px] mt-10 py-20 border-2 rounded-2xl hover:border-gray-600 pl-20 mx-auto">
          <h2>Upload an Image</h2>
          <form onSubmit={handleSubmit} className="mt-4">
            <input
                type="file"
                onChange={handleFileChange}
                accept="image/*"
            />
            <button type="submit" className="block mt-4" >Analyze Image</button>
          </form>
        </div>
      </div>
  );
}
