const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const API_ROUTES = {
    HOME: '/',
    AUTH: {
        SIGN_IN: `${API_URL}/auth/sign-in/`,
        SIGN_UP: `${API_URL}/auth/sign-up/`,
        SIGN_OUT: `${API_URL}/auth/sign-out/`,
    }
} as const;