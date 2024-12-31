import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";

import {SignUpForm} from "@/components/forms/SignUpForm";

export default function SignUpPage() {
    return (
        <main className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle className="text-2xl text-center">Регистрация</CardTitle>
                </CardHeader>
                <CardContent>
                    <SignUpForm/>
                </CardContent>
            </Card>
        </main>
    )
}