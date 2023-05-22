import { ReactNode } from "react";
import Navbar from "./Navbar";
import { AnimatePresence, motion } from "framer-motion";
type LayoutProps = {
    children: ReactNode;
    navigation: NavigationItem[]; // Add navigation prop to LayoutProps
};

interface NavigationItem {
    name: string;
    href: string;
    current: boolean;
}

const Layout = ({ navigation, children }: LayoutProps) => {
    return (
        <>
            <Navbar navigation={navigation}></Navbar>
            <div className="container-flex pl-16 pr-16 pt-4 pb-16 mx-auto">

                <AnimatePresence>
                    <motion.main
                        initial={{ opacity: 0.6, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        transition={{ duration: 0.3 }}
                    >
                        {children}
                    </motion.main>
                </AnimatePresence>
            </div>
        </>
    );
};

export default Layout;
