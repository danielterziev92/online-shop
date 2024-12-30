'use client'

import {useState} from "react";

import {useSelector} from "react-redux";

import {Popover, PopoverContent, PopoverTrigger,} from "@/components/ui/popover";
import {Avatar, AvatarFallback, AvatarImage} from "@/components/ui/avatar";
import {Button} from "@/components/ui/button";

import {UserRound} from "lucide-react";
import {AuthDialog} from "@/components/auth/AuthDialog";
import SignInForm from "@/components/forms/SignInForm";
import {RootState} from "@/lib/store/store";

export function AuthPopover() {
    const isAuthenticated = useSelector((state: RootState) => state.account.isAuthenticated);

    const [isSignInOpen, setIsSignInOpen] = useState(false);
    const [isSignUpOpen, setIsSignUpOpen] = useState(false);

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
                        <Button onClick={() => setIsSignInOpen(true)}>Sign In</Button>
                        <Button onClick={() => setIsSignUpOpen(true)}>Sign Up</Button>
                    </div>
                </PopoverContent>
            </Popover>

            <AuthDialog open={isSignInOpen} onOpenChange={setIsSignInOpen} title="Sign In">
                <SignInForm onSuccess={() => setIsSignInOpen(false)}/>
            </AuthDialog>

            <AuthDialog open={isSignUpOpen} onOpenChange={setIsSignUpOpen} title="Sign Up">
                <SignInForm/>
            </AuthDialog>

        </>
    );
}
