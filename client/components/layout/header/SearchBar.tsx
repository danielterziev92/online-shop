import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";

import {Search} from "lucide-react";

export function SearchBar() {
    return (
        <div className="flex w-full max-w-2xl gap-2">
            <Input type="text" placeholder="Search your favorite products" className="w-full"/>
            <Button>
                <Search strokeWidth={3}/>
            </Button>
        </div>
    );
}