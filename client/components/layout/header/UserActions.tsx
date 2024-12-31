'use client';

import {Suspense, lazy} from 'react';

import {useDispatch, useSelector} from "react-redux";

import {Heart, LoaderCircle, Moon, RefreshCcw, ShoppingBag, Sun} from "lucide-react";

import {AppDispatch, RootState} from "@/lib/store/store";
import {toggleTheme} from "@/lib/store/features/auth/accountSlice";

interface CountBadgeProps {
    count: number;
}

const CountBadge: React.FC<CountBadgeProps> = ({count}) => (
    <span
        className="absolute -top-2 -right-2 bg-blue-600 text-white rounded-full w-5 h-5 text-xs flex items-center justify-center">
        {count}
    </span>
);

export function UserActions() {
    const dispatch = useDispatch<AppDispatch>();
    const theme = useSelector((state: RootState) => state.account.theme);

    const AuthPopoverLazy = lazy(() =>
        import('@/components/auth/AuthPopover').then(mod => ({
            default: mod.AuthPopover
        }))
    );

    const toggleThemeHandler = () => {
        dispatch(toggleTheme());
    };

    return (
        <div className="flex items-center gap-4">
            <button
                className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800"
                onClick={toggleThemeHandler}
                aria-label={theme === 'light' ? 'Switch to dark theme' : 'Switch to light theme'}
            >
                {theme === 'light' ? <Moon className="w-5 h-5"/> : <Sun className="w-5 h-5"/>}
            </button>
            <button className="relative">
                <Heart/>
                <CountBadge count={0}/>
            </button>
            <button className="relative">
                <RefreshCcw/>
                <CountBadge count={0}/>
            </button>
            <button className="relative">
                <ShoppingBag/>
                <CountBadge count={0}/>
            </button>
            <button>
                <Suspense fallback={<LoaderCircle className="animate-spin"/>}>
                    <AuthPopoverLazy/>
                </Suspense>
            </button>
        </div>
    );
}