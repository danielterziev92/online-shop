import {createAsyncThunk} from "@reduxjs/toolkit";

import {jwtDecode} from "jwt-decode";

import {API_ROUTES} from "@/lib/routes";


interface SignInCredentials {
    email: string;
    password: string;
}

interface JWTPayload {
    account_id: string;
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
            console.log(data)

            if (!response.ok) {
                throw new Error(data.detail || 'Sign in failed');
            }

            const token = data.token;
            const decodedToken = jwtDecode<JWTPayload>(token);
            console.log(decodedToken.account_id)

            return {
                accountId: decodedToken.account_id,
            }
        } catch (error: any) {
            return rejectWithValue(error.message);
        }
    }
);


