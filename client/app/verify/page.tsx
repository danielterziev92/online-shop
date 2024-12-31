import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";

import {VerificationForm} from "@/components/forms/VerificationForm";

export default function VerifyPage() {
    return (
        <main className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle className="text-2xl text-center">Потвърди кода</CardTitle>
                </CardHeader>
                <CardContent>
                    <VerificationForm/>
                </CardContent>
            </Card>
        </main>
    )
}