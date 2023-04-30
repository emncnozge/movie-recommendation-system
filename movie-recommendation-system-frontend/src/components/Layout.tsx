import { ReactNode } from "react";
import Navbar from "./Navbar";
type LayoutProps = {
    children: ReactNode;
};

const Layout = ({ children }: LayoutProps) => {
    console.log(children);
    return (
        <>


            <div className="container-flex pl-16 pr-16 pt-8 pb-16 mx-auto">
                <main>{children}</main>
            </div>
        </>
    );
};

export default Layout;
