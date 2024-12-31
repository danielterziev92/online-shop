import {ChangeEvent, useState} from "react";
import {FieldValues, Path, UseFormReturn, useWatch} from "react-hook-form";

import {FormControl, FormField, FormItem, FormLabel, FormMessage} from "@/components/ui/form";
import {Input} from "@/components/ui/input";

import {Check, Eye, EyeOff} from "lucide-react";

interface PasswordInputProps<T extends FieldValues> {
    control: UseFormReturn<T>['control'];
    name: Path<T>;
    label: string;
    isMainPassword?: boolean;
    matchValue?: string;
    onChange?: (e: ChangeEvent<HTMLInputElement>) => void;
}

export function PasswordInput<T extends FieldValues>(
    {control, name, label, isMainPassword, matchValue, onChange, ...props}: PasswordInputProps<T>) {
    const [showPassword, setShowPassword] = useState(false);
    const value = useWatch({control, name});

    const isValid = value && (
        isMainPassword
            ? value.length >= 8 && /\d/.test(value) && !/^\d+$/.test(value)
            : value === matchValue
    );

    return (
        <FormField
            control={control}
            name={name}
            render={({field}) => (
                <FormItem>
                    <FormLabel>{label}</FormLabel>
                    <FormControl>
                        <div className="relative">
                            <Input
                                type={showPassword ? 'text' : 'password'}
                                className={isValid ? 'border-[var(--valid-input)] focus:border-[var(--valid-input)]' : ''}
                                {...field}
                                onChange={(e) => {
                                    field.onChange(e);
                                    onChange?.(e);
                                }}
                                {...props}
                            />
                            {isValid && (
                                <Check
                                    className="absolute right-10 top-1/2 -translate-y-1/2 text-[var(--valid-input)] w-4 h-4"/>
                            )}
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                            >
                                {showPassword ? <EyeOff className="h-4 w-4"/> : <Eye className="h-4 w-4"/>}
                            </button>
                        </div>
                    </FormControl>
                    <FormMessage/>
                </FormItem>
            )}
        />
    );
}