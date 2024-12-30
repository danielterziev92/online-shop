'use client';

import {Provider, useSelector} from "react-redux";
import {RootState, store} from "@/lib/store/store";
import {useEffect} from "react";

function ThemeWrapper({children}: { children: React.ReactNode }) {
    const theme = useSelector((state: RootState) => state.account.theme);

    useEffect(() => {
        document.documentElement.classList.remove('light', 'dark');
        document.documentElement.classList.add(theme);
    }, [theme]);

    return <>{children}</>;
}

export function Providers({children}: { children: React.ReactNode }) {
    return (
        <Provider store={store}>
            <ThemeWrapper>{children}</ThemeWrapper>
        </Provider>
    );
}