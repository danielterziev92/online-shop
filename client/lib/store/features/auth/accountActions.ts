import {createAsyncThunk} from "@reduxjs/toolkit";

import {jwtDecode} from "jwt-decode";

import {API_ROUTES} from "@/lib/routes";


interface SignInCredentials {
    email: string;
    password: string;
}

interface JWTPayload {
    account_id: number;
    is_verified: boolean;
}

export const signIn = createAsyncThunk(
    'account/signIn',
    async (credentials: SignInCredentials, {rejectWithValue}) => {
        try {
            const response = await fetch(API_ROUTES.AUTH.SIGN_IN, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(credentials),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Sign in failed');
            }

            const token = data.token;
            const decodedToken = jwtDecode<JWTPayload>(token);

            return {accountId: decodedToken.account_id, isVerified: decodedToken.is_verified}
        } catch (error: any) {
            return rejectWithValue(error.message);
        }
    }
);


export const signUpAction = createAsyncThunk(
    'account/signUp',
    async (credentials: SignInCredentials, {rejectWithValue}) => {
        console.log(credentials)
        try {
            const response = await fetch(API_ROUTES.AUTH.SIGN_UP, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(credentials),
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Sign up failed');
            }

            return data.message;
        } catch (error: any) {
            return rejectWithValue(error.message);
        }
    }
);

