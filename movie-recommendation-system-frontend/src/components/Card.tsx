import React from "react";
import Link from "next/link";

interface CardProps {
  imageUrl: string;
  text: string;
  linkUrl: string;
}

const Card: React.FC<CardProps> = ({ imageUrl, text, linkUrl }) => {
  return (
    <Link href={linkUrl} className="bg-white rounded-lg shadow-md hover:shadow-lg transition duration-300 ease-in-out transform hover:-translate-y-1 cursor-pointer sm:w-1/3 md:w-1/4 lg:w-1/4 xl:w-1/4 flex flex-col justify-center">
      <div >
        <img className="mx-auto w-full h-48 object-contain rounded-t-lg" src={imageUrl} alt="card image" />
        <div className="px-4 py-2">
          <p className="text-gray-800 font-semibold">{text}</p>
        </div>
      </div>
    </Link>
  );
};

export default Card;
