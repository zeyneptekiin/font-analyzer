import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function analyzeImage(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${API_URL}/api/analyze-image`, formData);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error("Axios error:", error.response?.data || error.message);
      throw new Error(error.response?.data?.detail || "Failed to process image");
    } else {
      console.error("Unexpected error:", error);
      throw new Error("Unexpected error occurred while processing the image");
    }
  }
}
