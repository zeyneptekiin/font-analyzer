import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function analyzeImage(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${API_URL}/api/analyze-image`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  } catch (error) {
    console.error("Failed to process image", error);
    throw new Error("Failed to process image");
  }
}
