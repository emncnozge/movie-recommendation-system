import React, { useState, useEffect } from "react";
import axios from "axios";
import Layout from "@/components/Layout";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Search from "@/components/Search";
interface PosterData {
    imdb_id: string;
    poster_path: string;
    title: string;
    similarity: string;
}

interface ResponseData {
    status: boolean;
    data: PosterData[];
    movie_name: string;
}
const navigation = [
    { name: "Movies", href: "/", current: false },
    { name: "Text Search", href: "/TextSearch", current: true },
];
const TextSearch: React.FC = () => {
    const [responseData, setResponseData] = useState<ResponseData | null>(null);

    const [searchedText, setSearchedText] = useState("");
    const [textInfo, setTextInfo] = useState("");
    const handleSearch = async (e: {
        target: { value: React.SetStateAction<string> };
    }) => {
        setSearchedText(e.target.value);
    };
    const GetSimilarFromText = async () => {
        try {
            const response = await axios.post<ResponseData>(
                "http://127.0.0.1:8000/GetTextRecommendation",
                {
                    searched: searchedText,
                }
            );
            setResponseData(response.data);
            setTextInfo(searchedText);
            console.log(response.data);
        } catch (error) {
            console.log(error);
        }
    };
    const startSearch = async (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            GetSimilarFromText();
        }
    };
    const [dotCount, setDotCount] = useState(0);
    function updatePlaceholder() {
        setDotCount((prevCount) => {
            if (prevCount < 3) {
                return prevCount + 1;
            } else {
                return 0;
            }
        });
    }

    useEffect(() => {
        const intervalId = setInterval(() => {
            updatePlaceholder();
        }, 500);

        return () => {
            clearInterval(intervalId);
        };
    }, []);

    useEffect(() => {
        if (responseData && responseData.status) {
            if (typeof document !== 'undefined') {

                if (document.getElementsByName("search").length > 0) {
                    document.getElementsByName("search")[0].classList.remove("searchbar");
                }
            }
        }
    }, [responseData]);
    return (
        <>
            <Layout navigation={navigation}>
                <div className="items-center mb-8">
                    {!responseData && (
                        <div className="mx-auto">
                            <h1 className="font-bold mb-8 header">
                                Start Searching
                            </h1>
                        </div>
                    )}
                    <div className="relative">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="absolute top-0 bottom-0 w-6 h-6 my-auto text-gray-400 left-3"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                            />
                        </svg>
                        <input
                            type="text"
                            name="search"
                            placeholder={"Search a word" + ".".repeat(dotCount)}
                            className="w-full py-3 pl-12 pr-4 text-gray-500 border rounded-md outline-none bg-gray-50 focus:bg-white focus:border-indigo-600 searchbar"
                            onKeyDown={startSearch}
                            onChange={handleSearch}
                        />
                    </div>
                </div>
                {responseData && responseData.status && (
                    <div className="mx-auto">
                        <h1 className="font-bold mb-8 header">
                            Movie Recommendations Based On: &quot;{textInfo}&quot; Keyword
                        </h1>
                        <div className="grid grid-cols-1 gap-x-6 gap-y-16 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 xl:gap-x-10 pb-16">
                            {responseData.data.map((movie) => (
                                <Link
                                    key={movie.imdb_id}
                                    href={"/Movie?movie_id=" + movie.imdb_id}
                                    passHref
                                    className="group"
                                >
                                    <div className="aspect-h-1 aspect-w-1 h-full overflow-hidden rounded-lg bg-gray-100 xl:aspect-h-8 xl:aspect-w-7">
                                        <img
                                            src={movie.poster_path}
                                            alt={movie.imdb_id}
                                            className="h-full object-contain object-center group-hover:opacity-75"
                                        />
                                    </div>
                                    <div
                                        className="mx-auto mt-2 mb-4 text-sm font-bold text-gray-700"
                                        style={{ textAlign: "center" }}
                                    >
                                        {movie.title}
                                    </div>
                                </Link>
                            ))}
                        </div>
                    </div>
                )}
                {responseData && !responseData.status && (
                    <div className="mx-auto">
                        <h1 className="font-bold mb-8 header">Not Found</h1>
                    </div>
                )}
            </Layout>
        </>
    );
};
export default TextSearch;
