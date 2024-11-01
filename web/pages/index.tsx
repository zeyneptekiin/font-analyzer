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
      <div>
        <h1>Upload an Image</h1>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} accept="image/*" />
          <button type="submit">Analyze Image</button>
        </form>
      </div>
  );
}
