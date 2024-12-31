'use client';

import {useRouter} from "next/navigation";
import {useDispatch, useSelector} from "react-redux";

import {zodResolver} from "@hookform/resolvers/zod";
import {useForm} from "react-hook-form";
import {useToast} from "@/hooks/use-toast";

import * as z from "zod";

import {Form} from "@/components/ui/form";
import {Alert, AlertDescription} from "@/components/ui/alert";
import {Button} from "@/components/ui/button";

import {LoaderCircle} from "lucide-react";

import {EmailInput} from "@/components/forms/EmailInput";
import {PasswordInput} from "@/components/forms/PasswordInput";

import {AppDispatch, RootState} from "@/lib/store/store";
import {signInAction} from "@/lib/store/features/auth/accountActions";
import {useState} from "react";
import {formatErrorMessage} from "@/lib/errorMessages";


interface SignInFormProps {
    onSuccess?: () => void;
}

const formSchema = z.object({
    email: z.string().email('Невалиден имейл адрес'),
    password: z.string().min(8, 'Паролата трябва да съдържа поне 8 символа'),
});

export function SignInForm({onSuccess}: SignInFormProps) {
    const {toast} = useToast();
    const dispatch = useDispatch<AppDispatch>();
    const router = useRouter();

    const loading = useSelector((state: RootState) => state.account.loading);

    const [errors, setErrors] = useState<string[]>([]);

    const form = useForm({
        resolver: zodResolver(formSchema),
        defaultValues: {email: '', password: ''}
    });

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        const response = await dispatch(signInAction(values));

        if (signInAction.fulfilled.match(response)) {
            onSuccess?.();
            toast({variant: 'success', duration: 3000, description: 'Успешно се вписахте в профила си!'});
            router.push('/');
        } else {
            const errors: string[] = formatErrorMessage(response.payload as string);
            setErrors(errors);
        }
    };

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <EmailInput
                    control={form.control}
                    name="email"
                    label="Имейл"
                />

                <PasswordInput
                    control={form.control}
                    name="password"
                    label="Парола"
                    isMainPassword
                />

                {errors.length > 0 && (
                    <Alert variant="destructive">
                        {errors.map((err, index) => (
                            <AlertDescription key={index}>{err}</AlertDescription>
                        ))}
                    </Alert>
                )}

                <Button type={'submit'} className="w-full">
                    {loading ? <LoaderCircle className="mr-2 h-4 w-4 animate-spin"/> : 'Вписване'}
                </Button>
            </form>
        </Form>
    )
}