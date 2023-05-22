import { useAppContext } from '@/pages/AppContext';
import React, { useEffect } from 'react';

const OptionSlider = () => {
    const { isAdult, setIsAdult } = useAppContext();

    const handleToggle = () => {
        setIsAdult(!isAdult);
    };

    useEffect(() => {
        setIsAdult(isAdult);
    }, [isAdult]);

    return (
        <div className={`flex items-center md:mr-2 rounded-md p-2 md:border-2 duration-300 ease-in-out ${isAdult ? 'border-red-500' : 'border-gray-600 '}`}>
            <div className={`text-sm font-medium mr-1 duration-300 ease-in-out hidden md:block ${isAdult ? 'text-red-500' : 'text-gray-300 '}`}>Adult Content&nbsp;</div>
            <label htmlFor="adult-toggle" className="flex items-center cursor-pointer">
                <div className={`w-10 h-6 bg-gray-400 rounded-full p-1 duration-300 ease-in-out ${isAdult ? 'bg-red-500' : 'bg-gray-400'}`}>
                    <div className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300 ease-in-out ${isAdult ? 'translate-x-4' : 'translate-x-0'}`}></div>
                </div>
            </label>
            <input
                type="checkbox"
                id="adult-toggle"
                className="hidden"
                checked={isAdult}
                onChange={handleToggle}
            />
        </div>
    );
};

export default OptionSlider;
