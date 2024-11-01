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
        <div>
            <h1>Analysis Results</h1>
            {result ? (
                <pre>{JSON.stringify(result, null, 2)}</pre>
            ) : (
                <p>Loading results...</p>
            )}
            <button onClick={() => router.push('/')}>Back to Home</button>
        </div>
    );
}
