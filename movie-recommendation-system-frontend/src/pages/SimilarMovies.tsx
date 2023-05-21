import React, { useState, useEffect } from "react";
import axios from "axios";
import Layout from "@/components/Layout";
import Link from "next/link";
import Navbar from "@/components/Navbar";
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
    { name: "Poster Search", href: "/", current: false },
    { name: "Text Search", href: "/TextSearch", current: false },
];
const GetSimilarPostersPage: React.FC = () => {
    const [responseData, setResponseData] = useState<ResponseData | null>(null);
    useEffect(() => {
        GetSimilarMovies();
    }, []);
    const GetSimilarMovies = async () => {
        try {
            const urlParams = new URLSearchParams(window.location.search);
            const movieId = urlParams.get("movie_id") as string;
            const response = await axios.post<ResponseData>(
                "http://127.0.0.1:8000/GetSimilarPosters",
                {
                    movie_id: movieId,
                    amount: 23,
                    adult: 0,
                }
            );
            setResponseData(response.data);
            console.log(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <>
            <Navbar navigation={navigation}></Navbar>
            <Layout>
                {responseData && responseData.status && (
                    <div className="mx-auto">
                        <h1 className="font-bold mb-8 header">
                            Similar Movies For: "{responseData.movie_name}"{" "}
                        </h1>
                        <div className="grid grid-cols-1 gap-x-6 gap-y-16 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 xl:gap-x-10 pb-16">
                            {responseData.data.map((movie) => (
                                <Link
                                    key={movie.imdb_id}
                                    href={movie.poster_path}
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
            </Layout>
        </>
    );
};

export default GetSimilarPostersPage;
