import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';

interface SearchResult {
    imdb_id: string;
    title: string;
    poster_path: string;
    adult: number;
    genre: string[];
    keywords: { id: number; name: string }[];
}

const Search: React.FC = () => {
    const [searchText, setSearchText] = useState('');
    const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [showDropdown, setShowDropdown] = useState(false);

    const dropdownRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        let timerId: NodeJS.Timeout;

        const fetchSearchResults = async () => {
            setLoading(true);
            try {
                const response = await axios.get('http://127.0.0.1:8000/Search', {
                    params: { search: searchText },
                });
                setSearchResults(response.data.data);
                setLoading(false);
                setShowDropdown(true); // Sonuçlar döndüğünde dropdown alanını göster
            } catch (error) {
                console.error('Error fetching search results:', error);
                setLoading(false);
                setShowDropdown(false); // Hata durumunda dropdown alanını gizle
            }
        };

        if (searchText && searchText.length >= 3) {
            timerId = setTimeout(() => {
                fetchSearchResults();
            }, 300);
        } else {
            setSearchResults([]); // Metin girilmediğinde sonuçları sıfırla
            setShowDropdown(false); // Metin girilmediğinde dropdown alanını gizle
        }

        return () => {
            clearTimeout(timerId);
        };
    }, [searchText]);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchText(event.target.value);
    };

    const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            // Arama yapma işlemi burada gerçekleştirilebilir
            // Örneğin: window.location.href = '/search?q=' + searchText;
        }
    };


    const handleOutsideClick = (event: MouseEvent) => {
        const target = event.target as HTMLElement;

        if (dropdownRef.current && !dropdownRef.current.contains(target)) {
            setShowDropdown(false);
        }
    };

    useEffect(() => {
        window.addEventListener('mousedown', handleOutsideClick);

        return () => {
            window.removeEventListener('mousedown', handleOutsideClick);
        };
    }, []);

    return (
        <div className="flex flex-col items-center">
            <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <MagnifyingGlassIcon className="h-6 w-6 text-gray-400" />
                </div>
                <input
                    type="text"
                    value={searchText}
                    onChange={handleInputChange}
                    onKeyPress={handleKeyPress}
                    className="pl-10 pr-4 py-2 w-64 md:w-80 border border-gray-300 rounded-md shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Search..."
                />
                {showDropdown && searchResults.length > 0 && (
                    <ul className="mt-1 w-64 md:w-80 bg-white rounded-md shadow-md absolute z-10">
                        {searchResults.map((result) => (
                            <Link key={result.imdb_id} href={"/Movie?movie_id=" + result.imdb_id} passHref
                                className={`flex items-center space-x-2 px-4 py-2 hover:bg-gray-100 cursor-pointer hover:rounded-md
                                    }`}
                            >
                                <img src={result.poster_path} alt={result.title} className="h-20" />
                                <span>{result.title}</span>

                            </Link>
                        ))}
                    </ul>
                )}
            </div>
        </div >
    );
};

export default Search;
