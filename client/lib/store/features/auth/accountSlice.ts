import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {signIn, signUpAction} from "@/lib/store/features/auth/accountActions";

interface AccountData {
    accountId: number;
}

interface AccountSettings {
    notifications?: boolean;
}

interface AuthState {
    data: AccountData | null;
    settings: AccountSettings | object;
    isAuthenticated: boolean;
    isVerified: boolean;
    theme: 'light' | 'dark';
    loading: boolean;
}

interface SignInResponse {
    accountId: number;
    isVerified: boolean;
}

const initialState: AuthState = {
    data: null,
    settings: {},
    isAuthenticated: false,
    isVerified: false,
    theme: "light",
    loading: false,
}

export const accountSlice = createSlice({
    name: "account",
    initialState,
    reducers: {
        toggleTheme: (state) => {
            state.theme = state.theme === 'light' ? 'dark' : 'light';
        },
        setTheme: (state, action: PayloadAction<AuthState['theme']>) => {
            state.theme = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            // Sign In
            .addCase(signIn.pending, (state) => {
                state.loading = true;
            })
            .addCase(signIn.fulfilled, (state, action: PayloadAction<SignInResponse>) => {
                state.loading = false;
                state.isAuthenticated = true;
                state.data = {
                    accountId: action.payload.accountId,
                };
                state.isVerified = action.payload.isVerified;
            })
            .addCase(signIn.rejected, (state) => {
                state.loading = false;
            })
            // Sign Up
            .addCase(signUpAction.pending, state => {
                state.loading = true;
            })
            .addCase(signUpAction.fulfilled, state => {
                state.loading = false;
            })
            .addCase(signUpAction.rejected, (state) => {
                state.loading = false;
            })
    }
});

export const {toggleTheme, setTheme} = accountSlice.actions;

export default accountSlice.reducer;