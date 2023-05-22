import React, { createContext, useState, useEffect, useContext } from 'react';

interface AppContextProps {
    isAdult: boolean;
    setIsAdult: (value: boolean) => void;
}

const AppContext = createContext<AppContextProps | undefined>(undefined);

const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [isAdult, setIsAdult] = useState<boolean>(false);

    useEffect(() => {
        window.onload = () => {
            const storedAdultValue = localStorage.getItem('adult');
            const parsedValue = storedAdultValue !== null ? JSON.parse(storedAdultValue) : false;
            setIsAdult(parsedValue);
        };
    }, []);

    useEffect(() => {
        localStorage.setItem('adult', JSON.stringify(isAdult));
    }, [isAdult]);

    return (
        <AppContext.Provider value={{ isAdult, setIsAdult }}>
            {children}
        </AppContext.Provider>
    );
};

const useAppContext = (): AppContextProps => {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error('useAppContext must be used within an AppProvider');
    }
    return context;
};

export { AppProvider, useAppContext };
