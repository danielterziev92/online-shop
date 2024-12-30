import Link from "next/link";
import {API_ROUTES} from "@/lib/routes";

export function Logo() {
    return (
        <div className="flex items-center">
            <Link href={API_ROUTES.HOME} className="text-2xl font-bold text-blue-600">Cloud Control</Link>
        </div>
    );
}