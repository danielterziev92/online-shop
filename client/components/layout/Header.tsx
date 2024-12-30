import {Logo} from "@/components/layout/header/Logo";
import {SearchBar} from "@/components/layout/header/SearchBar";
import {ContactInfo} from "@/components/layout/header/ContactInfo";
import {UserActions} from "@/components/layout/header/UserActions";

export function Header() {
    return (
        <header className="sticky top-0 z-50 bg-background border-b">
            <div className="container mx-auto px-4 py-3">
                <div className="flex items-center justify-between gap-4">
                    <Logo/>
                    <SearchBar/>
                    <ContactInfo/>
                    <UserActions/>
                </div>
            </div>
        </header>
    );
}