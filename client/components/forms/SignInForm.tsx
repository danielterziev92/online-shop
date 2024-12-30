'use client';

import {useRouter} from "next/navigation";
import {useDispatch, useSelector} from "react-redux";

import {zodResolver} from "@hookform/resolvers/zod";
import {useForm} from "react-hook-form";

import * as z from "zod";

import {Form, FormControl, FormField, FormItem, FormLabel, FormMessage} from "@/components/ui/form";
import {Input} from "@/components/ui/input";
import {Alert, AlertDescription} from "@/components/ui/alert";
import {Button} from "@/components/ui/button";

import {AppDispatch, RootState} from "@/lib/store/store";
import {signIn} from "@/lib/store/features/auth/accountActions";

interface SignInFormProps {
    onSuccess?: () => void;
}


const formSchema = z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
});

export default function SignInForm({onSuccess}: SignInFormProps) {
    const dispatch = useDispatch<AppDispatch>();
    const router = useRouter();

    const {error, loading} = useSelector((state: RootState) => state.account);

    const form = useForm({
        resolver: zodResolver(formSchema),
        defaultValues: {email: '', password: ''}
    });

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        const resultAction = await dispatch(signIn(values));

        if (signIn.fulfilled.match(resultAction)) {
            onSuccess?.();
            router.push('/');
        }
    };

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormField
                    control={form.control}
                    name={'email'}
                    render={({field}) => (
                        <FormItem>
                            <FormLabel>Email</FormLabel>
                            <FormControl><Input type={'email'} {...field}/></FormControl>
                            <FormMessage/>
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name={'password'}
                    render={({field}) => (
                        <FormItem>
                            <FormLabel>Password</FormLabel>
                            <FormControl><Input type={'password'} {...field}/></FormControl>
                            <FormMessage/>
                        </FormItem>
                    )}
                />

                {error && (
                    <Alert variant={'destructive'}>
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                )}

                <Button type={'submit'} className="w-full">
                    {loading ? 'Signing in...' : 'Sign In'}
                </Button>
            </form>
        </Form>
    )
}