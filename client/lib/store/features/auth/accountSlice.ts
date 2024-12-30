import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {signIn} from "@/lib/store/features/auth/accountActions";


interface AuthState {
    data: Record<string, any>;
    settings: Record<string, any>;
    isAuthenticated: boolean;
    theme: string;
    error: string | null;
    loading: boolean;
}

const initialState: AuthState = {
    data: {},
    settings: {},
    isAuthenticated: false,
    theme: "light",
    error: null,
    loading: false,
}

export const accountSlice = createSlice({
    name: "account",
    initialState,
    reducers: {
        toggleTheme: (state) => {
            state.theme = state.theme === "light" ? "dark" : "light";
        },
        setTheme: (state, action: PayloadAction<string>) => {
            state.theme = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(signIn.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(signIn.fulfilled, (state, action) => {
                state.loading = false;
                state.isAuthenticated = true;
                state.data = {
                    accountId: action.payload.accountId,
                }
            })
            .addCase(signIn.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })
    }
});

export const {toggleTheme, setTheme} = accountSlice.actions;

export default accountSlice.reducer;