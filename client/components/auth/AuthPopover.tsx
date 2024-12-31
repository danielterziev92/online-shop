'use client'

import {useState} from "react";

import {useSelector} from "react-redux";


import {Popover, PopoverContent, PopoverTrigger,} from "@/components/ui/popover";
import {Avatar, AvatarFallback, AvatarImage} from "@/components/ui/avatar";
import {Button} from "@/components/ui/button";

import {UserRound} from "lucide-react";

import {RootState} from "@/lib/store/store";
import {VerificationForm} from "@/components/forms/VerificationForm";

interface SignUpFormData {
    email: string;
    password: string;
}

interface VerificationFormData {
    code: string;
}

export function AuthPopover() {
    const isAuthenticated = useSelector((state: RootState) => state.account.isAuthenticated);

    const [signInDialog, setSignInDialog] = useState<any>(null);
    const [signUpDialog, setSignUpDialog] = useState<any>(null);
    const [isSignInOpen, setIsSignInOpen] = useState(false);
    const [isSignUpOpen, setIsSignUpOpen] = useState(false);
    const [signUpData, setSignUpData] = useState<SignUpFormData | null>(null);
    const [showVerification, setShowVerification] = useState(false);

    const loadSignInDialog = async () => {
        const [dialogModule, formModule] = await Promise.all([
            import("@/components/auth/AuthDialog"),
            import("@/components/forms/SignInForm")
        ]);
        setSignInDialog({
            Dialog: dialogModule.AuthDialog,
            Form: formModule.SignInForm
        });
    };

    const loadSignUpDialog = async () => {
        const [dialogModule, formModule] = await Promise.all([
            import("@/components/auth/AuthDialog"),
            import("@/components/forms/SignUpForm")
        ]);
        setSignUpDialog({
            Dialog: dialogModule.AuthDialog,
            Form: formModule.SignUpForm
        });
    };

    const handleSignUpSuccess = (data: SignUpFormData) => {
        setSignUpData(data);
        setShowVerification(true);
    };


    return (
        <>
            <Popover>
                <PopoverTrigger asChild>
                    {isAuthenticated
                        ? (
                            <Avatar>
                                <AvatarImage src="https://github.com/shadcn.png"/>
                                <AvatarFallback></AvatarFallback>
                            </Avatar>
                        )
                        : (
                            <UserRound className="w-6 h-6"/>
                        )
                    }
                </PopoverTrigger>
                <PopoverContent className="w-48">
                    <div className="flex flex-col gap-2">
                        <Button onClick={() => {
                            setIsSignInOpen(true);
                            if (!signInDialog) loadSignInDialog();
                        }}>Вписване</Button>
                        <Button onClick={() => {
                            setIsSignUpOpen(true);
                            if (!signUpDialog) loadSignUpDialog();
                        }}>Регистрация</Button>
                    </div>
                </PopoverContent>
            </Popover>

            {signInDialog && (
                <signInDialog.Dialog
                    open={isSignInOpen}
                    onOpenChange={setIsSignInOpen}
                    title="Вписване"
                >
                    <signInDialog.Form onSuccess={() => setIsSignInOpen(false)}/>
                </signInDialog.Dialog>
            )}

            {signUpDialog && (
                <signUpDialog.Dialog
                    open={isSignUpOpen}
                    onOpenChange={setIsSignUpOpen}
                    title={showVerification ? "Потвърждение" : "Регистрация"}
                >
                    {showVerification
                        ? (
                            <VerificationForm
                                onSuccess={() => {
                                    setIsSignUpOpen(false);
                                    setShowVerification(false);
                                    setSignUpData(null);
                                }}
                            />
                        ) : (
                            <signUpDialog.Form onSuccess={handleSignUpSuccess}/>
                        )}
                </signUpDialog.Dialog>
            )}

        </>
    );
}
