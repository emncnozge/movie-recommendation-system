import React, { useState, useEffect } from "react";
import axios from "axios";
import Layout from "@/Components/Layout";
import Link from "next/link";
import { ArrowLeftIcon, ArrowRightIcon } from '@heroicons/react/24/outline'

interface PosterData {
    imdb_id: string;
    poster_path: string;
    title: string;
    similarity: string;
}

interface ResponseData {
    status: boolean;
    data: PosterData[];
    max: number;
}

const GetSimilarPostersPage: React.FC = () => {
    const [responseData, setResponseData] = useState<ResponseData | null>(null);
    const [moviePerPage, setMoviePerPage] = useState(18);
    const [currentPage, setCurrentPage] = useState(1);
    const [start, setStart] = useState(0);
    const [end, setEnd] = useState(moviePerPage);
    const [max, setMax] = useState(end);
    useEffect(() => {
        getMovies(start, end);
    }, [start, end]);

    const getMovies = async (start: number, end: number) => {
        try {
            const response = await axios.get<ResponseData>(
                "http://127.0.0.1:8000/GetAllMovies",
                {
                    params: {
                        start: start, // Replace with your desired start value
                        end: end, // Replace with your desired end value
                    },
                }
            );
            setResponseData(response.data);
            setMax(response.data.max);
            console.log(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    const handleNext = async () => {
        if (start + moviePerPage > max || end + moviePerPage > max) {
            setStart(max - moviePerPage);
            setEnd(max);
            setCurrentPage(Math.ceil(max / moviePerPage));
        } else {
            setStart(start + moviePerPage);
            setEnd(end + moviePerPage);
            setCurrentPage(currentPage + 1);
        }
    };
    const handlePrev = async () => {
        if (start - moviePerPage < 0 || end - moviePerPage < 0) {
            setStart(0);
            setEnd(moviePerPage);
            setCurrentPage(1);
        } else {
            setStart(start - moviePerPage);
            setEnd(end - moviePerPage);
            setCurrentPage(currentPage - 1);
        }
    };


    const changePage = (e: React.KeyboardEvent<HTMLInputElement>) => {

        let val: number = parseInt(e.currentTarget.value) - 1
        let maxPage: number = Math.ceil(max / moviePerPage);
        console.log(maxPage)
        if (e.key === "Enter") {
            if (isNaN(val) || val === null) {

            }
            else if (val >= maxPage) {
                setStart(max - moviePerPage);
                setEnd(max);
                setCurrentPage(Math.ceil(max / moviePerPage));
            }
            else if (val < 1) {
                setStart(0);
                setEnd(moviePerPage);
                setCurrentPage(1);
            }
            else {
                setStart(val * moviePerPage);
                setEnd(val * moviePerPage + moviePerPage)
            }
        }
        else {
            setCurrentPage(parseInt(e.currentTarget.value));
        }
    };
    const handlePageNumber = async (e: { target: { value: any; }; }) => {
        setCurrentPage(parseInt(e.target.value));
    }
    return (
        <Layout>
            {responseData && responseData.status && (
                <div className="mx-auto">
                    <h1 className="font-bold mb-8">All Movies</h1>
                    <div className="mb-4" style={{ textAlign: "center" }}>
                        <button
                            onClick={handlePrev}
                            className="bg-blue-400 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-l"
                            disabled={currentPage == 1 ? true : false}
                        >
                            Prev
                        </button>
                        <button
                            onClick={handleNext}
                            className="bg-blue-400 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-r"
                            disabled={currentPage == Math.ceil(max / moviePerPage) ? true : false}
                        >
                            Next
                        </button>


                        <div className="inline-flex w-24 my-auto relative mt-2 mb-1.5 rounded-md shadow-sm ml-4">

                            <input
                                type="text"
                                name="pagenum"
                                id="pagenum"
                                value={currentPage}
                                onChange={handlePageNumber}
                                onKeyDown={changePage}
                                className="w-24 my-auto block rounded-md border-0 py-1.5 pl-2 pr-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-300 sm:text-sm sm:leading-6"
                                placeholder="Page"
                            />

                        </div>

                    </div>
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
                                <div className="object-center mx-auto mt-2 mb-4 text-sm font-bold text-gray-700">
                                    {movie.title}
                                </div>
                            </Link>
                        ))}
                    </div>
                    <div className="mb-4" style={{ textAlign: "center" }}>
                        <button
                            onClick={handlePrev}
                            className="bg-blue-400 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-l"
                            disabled={currentPage == 1 ? true : false}
                        >
                            Prev
                        </button>
                        <button
                            onClick={handleNext}
                            className="bg-blue-400 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-r"
                            disabled={currentPage == Math.ceil(max / moviePerPage) ? true : false}
                        >
                            Next
                        </button>


                        <div className="inline-flex w-24 my-auto relative mt-2 mb-1.5 rounded-md shadow-sm ml-4">

                            <input
                                type="text"
                                name="pagenum"
                                id="pagenum"
                                value={currentPage}
                                onChange={handlePageNumber}
                                onKeyDown={changePage}
                                className="w-24 my-auto block rounded-md border-0 py-1.5 pl-2 pr-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-300 sm:text-sm sm:leading-6"
                                placeholder="Page"
                            />

                        </div>

                    </div>
                </div>
            )}
        </Layout>
    );
};

export default GetSimilarPostersPage;
