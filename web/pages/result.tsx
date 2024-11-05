import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

interface ResultData {
    [key: string]: string;
}

export default function Result() {
    const router = useRouter();
    const { data } = router.query;
    const [result, setResult] = useState<ResultData | null>(null);

    useEffect(() => {
        if (data) {
            try {
                const parsedData: ResultData = JSON.parse(data as string);
                setResult(parsedData);
            } catch (error) {
                console.error("Failed to parse JSON data", error);
            }
        }
    }, [data]);

    return (
        <div className="flex flex-col justify-center text-center">
            <h1 className="text-center mt-40 text-4xl">Analysis Results</h1>
            <div className="text-left w-[500px] mt-10 py-20 border-2 rounded-2xl hover:border-gray-600 pl-20 mx-auto">
                {result ? (
                    <pre className="mt-4">{JSON.stringify(result, null, 2)}</pre>
                ) : (
                    <p className="mt-4">Loading results...</p>
                )}
            </div>
            <button className="text-xl mt-4 underline underline-offset-4" onClick={() => router.push('/')}>Back to Home</button>
        </div>
    )
        ;
}
