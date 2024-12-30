import {PhoneCall} from "lucide-react";

export function ContactInfo() {
    return (
        <div className="flex items-center gap-2">
            <PhoneCall/>
            <div>
                <div className="text-xs text-gray-600">CALL ANYTIME</div>
                <div className="font-semibold">280 900 3434</div>
            </div>
        </div>
    );
}