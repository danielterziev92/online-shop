import SignInForm from "@/components/forms/SignInForm";
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";

export default function SignInPage() {
    return (
        <main className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle className="text-2xl text-center">Sign In</CardTitle>
                </CardHeader>
                <CardContent>
                    <SignInForm/>
                </CardContent>
            </Card>
        </main>
    )
}