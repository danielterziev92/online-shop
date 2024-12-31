const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const API_ROUTES = {
    HOME: '/',
    TERMS: '/terms',
    POLICY: '/policy',
    AUTH: {
        SIGN_IN: `${API_URL}/auth/sign-in/`,
        SIGN_UP: `${API_URL}/auth/sign-up/`,
        SIGN_OUT: `${API_URL}/auth/sign-out/`,
        VERIFY_CODE: `${API_URL}/auth/verify/`,
    }
} as const;