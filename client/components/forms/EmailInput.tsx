import {ChangeEvent} from "react";

import {FieldValues, Path, UseFormReturn, useWatch} from "react-hook-form";

import {FormControl, FormField, FormItem, FormLabel, FormMessage} from "@/components/ui/form";
import {Input} from "@/components/ui/input";

import {Check} from 'lucide-react';

interface EmailInputProps<T extends FieldValues> {
    control: UseFormReturn<T>['control'];
    name: Path<T>;
    label: string;
    onChange?: (e: ChangeEvent<HTMLInputElement>) => void;
}

export function EmailInput<T extends FieldValues>({control, name, label, onChange, ...props}: EmailInputProps<T>) {
    const email = useWatch({control, name: name});
    const isValid = email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    return (
        <FormField control={control} name={name} render={({field}) => (
            <FormItem>
                <FormLabel>{label}</FormLabel>
                <FormControl>
                    <div className="relative">
                        <Input
                            type="email"
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
                                className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--valid-input)] w-4 h-4"/>
                        )}
                    </div>
                </FormControl>
                <FormMessage/>
            </FormItem>
        )}/>
    );
}