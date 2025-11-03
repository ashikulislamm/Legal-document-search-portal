import React from "react";

export default function Loader() {
  return (
    <div className="flex items-center justify-center py-10">
      <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      <span className="ml-3 text-gray-300">Fetching results...</span>
    </div>
  );
}
