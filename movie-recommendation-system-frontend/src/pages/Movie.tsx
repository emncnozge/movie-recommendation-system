import React, { useState, useEffect } from "react";
import axios from "axios";
import Layout from "@/components/Layout";
import Link from "next/link";
import { ArrowRightIcon, LinkIcon, PhotoIcon } from "@heroicons/react/24/outline";

interface MovieData {
    imdb_id: string;
    title: string;
    overview: string;
    poster_path: string;
    adult: number;
    genre: string[];
}

interface ResponseData {
    status: boolean;
    data: MovieData;
    max: number;
}

const navigation = [
    { name: "Movies", href: "/", current: false },
    { name: "Text Search", href: "/TextSearch", current: false },
];

const Movie: React.FC = () => {
    const [url, setUrl] = useState("/");
    const [responseData, setResponseData] = useState<ResponseData | null>(null);
    useEffect(() => {
        GetMovie();
        if (responseData?.data.title)
            document.title = responseData.data.title;
    }, [url]);
    const GetMovie = async () => {
        if (typeof window !== 'undefined') {
            setUrl(window.location.href);
        }
        try {
            const urlParams = new URLSearchParams(window.location.search);
            const movieId = urlParams.get("movie_id") as string;
            const response = await axios.post<ResponseData>(
                "http://127.0.0.1:8000/GetMovie",
                {
                    movie_id: movieId,
                }
            );
            setResponseData(response.data);
            document.title = response.data.data.title;
        } catch (error) {
            console.log(error);
        }
    };
    const renderGenre = () => {
        if (responseData) {
            if (responseData.data.genre.length === 0) return null;

            return responseData.data.genre.map((genreItem, index) => (

                <li key={index}>
                    <ArrowRightIcon className="inline-flex" width={20} color="#34455d" />
                    &ensp;
                    {genreItem}
                </li>


            ));
        }
        else {
            return null;
        }

    };
    return (
        <>
            <Layout navigation={navigation}>
                {responseData && responseData.status && (
                    <>
                        <div className="mx-auto">
                            <h1 className="font-bold mb-8 header">{responseData.data.title}</h1>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 lg:grid-cols-11 gap-4">
                            <div className="sm:col-span-1 md:col-span-2 lg:col-span-3 overflow-hidden bg-gray-100 max-w-full rounded-lg flex items-center">
                                <img src={responseData.data.poster_path} alt="Movie Poster" className="max-w-full h-auto p-2 pl-4 pr-4 mx-auto my-auto" />
                            </div>
                            <div className="sm:col-span-1 md:col-span-3 lg:col-span-8 p-8 pt-4 bg-gray-100 rounded-lg" style={{ textAlign: "justify" }}>
                                <p className="subheaders mb-2">Overview</p>
                                <p>
                                    <ArrowRightIcon className="inline-flex" width={20} color="#34455d" />
                                    &ensp;
                                    {responseData.data.overview}
                                </p>
                                <p className="subheaders mt-4 mb-2">Genres</p>
                                <ul>
                                    {renderGenre()}
                                </ul>
                                <p className="subheaders mt-4 mb-2">Age Restrictions</p>
                                <div className="mb-8">
                                    <ArrowRightIcon className="inline-flex" width={20} color="#34455d" />
                                    &ensp;
                                    {
                                        responseData.data.adult === 1
                                            ?
                                            <span style={{ color: "red", fontWeight: "bold" }}>Adult</span>
                                            :
                                            <span style={{ color: "darkgreen", fontWeight: "bold" }}>Not Adult</span>
                                    }
                                </div>
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                    <Link key={responseData.data.imdb_id} href={"/SimilarMovies?movie_id=" + responseData.data.imdb_id} passHref>
                                        <div className="text-white font-bold py-2 px-4 rounded findButton mx-auto my-auto">
                                            <PhotoIcon className="inline-flex pb-1 mr-1" width={24} color="#fff" />
                                            Find Similar Movies with Poster
                                        </div>
                                    </Link>
                                    <a target="_blank" rel="noopener noreferrer" key={responseData.data.imdb_id} href={"https://www.imdb.com/title/" + responseData.data.imdb_id} >
                                        <div className="text-white font-bold py-2 px-4 rounded imdbButton mx-auto my-auto">
                                            <LinkIcon className="inline-flex pb-1 mr-1" width={24} color="#000" />
                                            Go to IMDb page
                                        </div>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </>)}
            </Layout>
        </>
    );
}

export default Movie;