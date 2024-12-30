'use client';

import {useState, useEffect} from "react";

import {Search} from "lucide-react";

import {useDebounce} from "@/components/useDebounce";

export function SearchBar() {
    const [searchTerm, setSearchTerm] = useState("");
    const debouncedValue = useDebounce(searchTerm, 500);

    useEffect(() => {
        const searchProducts = async () => {
            if (debouncedValue) {
                try {
                    const response = await fetch(`/api/products/search?query=${debouncedValue}`);
                    const data = await response.json();
                    console.log(data); // тук ще обработвате резултатите
                } catch (error) {
                    console.error('Search error:', error);
                }
            }
        };

        searchProducts();
    }, [debouncedValue]);

    return (
        <div className="relative w-full max-w-2xl">
            <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full rounded-md border-2 border-[#3B82F6] bg-background px-3 py-2 text-sm
                         placeholder:text-muted-foreground pr-10
                         focus:outline-none focus:ring-0 focus:border-[#3B82F6]"
                placeholder="Search your favorite products"
            />
            <Search
                strokeWidth={3}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[#3B82F6]"
                size={20}
            />
        </div>
    );
}