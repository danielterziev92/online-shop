'use client';

import {useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import Link from "next/link";
import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import * as z from "zod";

import {Form, FormControl, FormField, FormItem, FormLabel, FormMessage} from "@/components/ui/form";
import {Checkbox} from "@/components/ui/checkbox";
import {Alert, AlertDescription} from "@/components/ui/alert";
import {Button} from "@/components/ui/button";

import {EmailInput} from "@/components/forms/EmailInput";
import {PasswordInput} from "@/components/forms/PasswordInput";

import {AppDispatch, RootState} from "@/lib/store/store";
import {signUpAction} from "@/lib/store/features/auth/accountActions";

import {API_ROUTES} from "@/lib/routes";
import {formatErrorMessage} from "@/lib/errorMessages";

const UPPERCASE_REGEX = /[A-Z]/;
const LOWERCASE_REGEX = /[a-z]/;
const SPECIAL_CHAR_REGEX = /[!@#$%^&*(),.?":{}|<>]/;

interface SignUpFormProps {
    onSuccess?: () => void;
}

const formSchema = z.object({
    email: z.string().email('Невалиден имейл адрес'),
    password: z.string()
        .min(8, 'Паролата трябва да съдържа поне 8 символа.')
        .refine(val => /\d/.test(val), 'Паролата трябва да съдържа поне едно число')
        .refine(val => !/^\d+$/.test(val), 'Паролата не може да съдържа само цифри'),
    repeatPassword: z.string(),
    terms: z.boolean().refine(val => val, {
        message: 'Трябва да приемете Условията за ползване и Политиката за поверителност.'
    })
}).refine((data) => data.password === data.repeatPassword, {
    message: "Паролите не съвпадат",
    path: ["repeatPassword"],
});

export function SignUpForm({onSuccess}: SignUpFormProps) {
    const dispatch = useDispatch<AppDispatch>();
    const loading = useSelector((state: RootState) => state.account.loading);
    const [passwordStrength, setPasswordStrength] = useState({score: 0, color: 'bg-destructive'});
    const [errors, setErrors] = useState<string[]>([]);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {email: '', password: '', repeatPassword: '', terms: false}
    });

    const calculatePasswordStrength = (password: string) => {
        let score = 0;
        if (password.length >= 8) score += 1;
        if (UPPERCASE_REGEX.test(password)) score += 1;
        if (LOWERCASE_REGEX.test(password)) score += 1;
        if (/[0-9]/.test(password)) score += 1;
        if (SPECIAL_CHAR_REGEX.test(password)) score += 1;

        const colors = {
            1: 'bg-destructive',
            2: 'bg-orange-500',
            3: 'bg-yellow-500',
            4: 'bg-yellow-500',
            5: 'bg-green-500'
        };

        setPasswordStrength({
            score: score || 1,
            color: colors[score as keyof typeof colors] || colors[1]
        });
    };

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        const response = await dispatch(signUpAction(values));

        if (signUpAction.fulfilled.match(response)) {
            onSuccess?.();
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
                    onChange={(e) => calculatePasswordStrength(e.target.value)}
                />


                <PasswordInput
                    control={form.control}
                    name="repeatPassword"
                    label="Повтори паролата"
                    matchValue={form.watch('password')}
                />

                <FormField
                    control={form.control}
                    name="terms"
                    render={({field}) => (
                        <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                            <FormControl>
                                <Checkbox
                                    checked={field.value}
                                    onCheckedChange={field.onChange}
                                />
                            </FormControl>
                            <div className="space-y-1 leading-none">
                                <FormLabel>
                                    Регистрирайки се, вие се съгласявате с нашите{' '}
                                    <Link href={API_ROUTES.TERMS} className="text-primary hover:underline">
                                        Условия за ползване
                                    </Link>{' '}
                                    и{' '}
                                    <Link href={API_ROUTES.POLICY} className="text-primary hover:underline">
                                        Политика за поверителност.
                                    </Link>
                                </FormLabel>
                                <FormMessage/>
                            </div>
                        </FormItem>
                    )}
                />

                <div className="space-y-2">
                    <div className="w-full h-2 rounded-full bg-slate-200">
                        <div
                            className={`h-full rounded-full transition-all ${passwordStrength.color}`}
                            style={{width: `${passwordStrength.score * 20}%`}}
                        />
                    </div>
                    <p className="text-sm text-muted-foreground text-center">
                        Сила на паролата:{' '}
                        <span className="font-medium">
              {passwordStrength.score <= 1 ? 'Слаба' :
                  passwordStrength.score === 2 ? 'Средна' :
                      passwordStrength.score >= 3 && passwordStrength.score <= 4 ? 'Силна' :
                          'Много силна'}
            </span>
                    </p>
                </div>

                {errors.length > 0 && (
                    <Alert variant="destructive">
                        {errors.map((err, index) => (
                            <AlertDescription key={index}>{err}</AlertDescription>
                        ))}
                    </Alert>
                )}

                <Button type="submit" className="w-full">
                    {loading ? 'Регистриране...' : 'Регистрация'}
                </Button>
            </form>
        </Form>
    )
        ;
}