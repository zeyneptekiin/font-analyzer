import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function generateFontWithImage(imageFile: File): Promise<string> {
    const formData = new FormData();
    formData.append("file", imageFile);

    try {
        const response = await axios.post(`${API_URL}/api/generate-font-with-image`, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
            responseType: "blob",
        });
        return URL.createObjectURL(response.data);
    } catch (error) {
        console.error("Failed to generate font preview image", error);
        throw new Error("Failed to generate font preview image. Please try again.");
    }
}
