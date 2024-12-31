'use client';

import {useEffect, useRef, useState} from "react";
import {useRouter} from "next/navigation";
import {useDispatch, useSelector} from "react-redux";
import {toast} from "@/hooks/use-toast";

import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";
import {Alert, AlertDescription} from "@/components/ui/alert";

import {LoaderCircle} from "lucide-react";

import {formatErrorMessage} from "@/lib/errorMessages";
import {AppDispatch, RootState} from "@/lib/store/store";
import {verifyCodeAction} from "@/lib/store/features/auth/accountActions";
import {API_ROUTES} from "@/lib/routes";

interface VerificationFormProps {
    onSuccess?: () => void;
}

export function VerificationForm({onSuccess}: VerificationFormProps) {
    const dispatch = useDispatch<AppDispatch>();
    const router = useRouter();

    const loading = useSelector((state: RootState) => state.account.loading);

    const [values, setValues] = useState<string[]>(Array(6).fill(''));
    const [errors, setErrors] = useState<string[]>([]);
    const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

    useEffect(() => {
        if (values.every(value => value !== '')) {
            handleSubmit(values.join(''));
        }
    }, [values]);

    const handleChange = (index: number, value: string) => {
        if (/^\d$/.test(value)) {
            const newValues = [...values];
            newValues[index] = value;
            setValues(newValues);

            if (index < 5) {
                inputRefs.current[index + 1]?.focus();
            }
        }
    };

    const handleKeyDown = (index: number, key: string) => {
        if (key === 'Backspace') {
            if (!values[index] && index > 0) {
                inputRefs.current[index - 1]?.focus();
            }
            const newValues = [...values];
            newValues[index] = '';
            setValues(newValues);
        } else if (key === 'ArrowLeft' && index > 0) {
            inputRefs.current[index - 1]?.focus();
        } else if (key === 'ArrowRight' && index < 5) {
            inputRefs.current[index + 1]?.focus();
        }
    };

    const handlePaste = (e: React.ClipboardEvent) => {
        e.preventDefault();
        const pastedData = e.clipboardData.getData('Text').trim();

        if (/^\d+$/.test(pastedData)) {
            const newValues = [...values];
            for (let i = 0; i < Math.min(6, pastedData.length); i++) {
                newValues[i] = pastedData[i];
            }
            setValues(newValues);
            const lastIndex = Math.min(5, pastedData.length - 1);
            inputRefs.current[lastIndex]?.focus();
        }
    };

    const handleSubmit = async (code: string) => {
        const response = await dispatch(verifyCodeAction(code));

        if (verifyCodeAction.fulfilled.match(response)) {
            onSuccess?.();
            toast({variant: 'success', duration: 3000, description: 'Успешно потвърдихте профила си!'});
            router.push(API_ROUTES.HOME);
        } else {
            const errors: string[] = formatErrorMessage(response.payload as string);
            setErrors(errors);
        }
    };

    return (
        <div className="mt-5">
            <div className="flex justify-evenly gap-2">
                {values.map((value, index) => (
                    <Input
                        key={index}
                        ref={(el: HTMLInputElement | null) => {
                            if (el) {
                                inputRefs.current[index] = el;
                            }
                        }}
                        type="text"
                        maxLength={1}
                        value={value}
                        autoFocus={index === 0}
                        className={`w-12 h-12 text-2xl text-center ${
                            value ? 'border-primary border-2' : ''
                        }`}
                        onChange={(e) => handleChange(index, e.target.value)}
                        onKeyDown={(e) => handleKeyDown(index, e.key)}
                        onPaste={index === 0 ? handlePaste : undefined}
                    />
                ))}
            </div>

            {errors.length > 0 && (
                <Alert variant="destructive">
                    {errors.map((err, index) => (
                        <AlertDescription key={index}>{err}</AlertDescription>
                    ))}
                </Alert>
            )}

            <Button className="w-full mt-5" onClick={() => handleSubmit(values.join(''))}>
                {loading ? <LoaderCircle className="mr-2 h-4 w-4 animate-spin"/> : 'Изпрати'}
            </Button>
        </div>
    );
}