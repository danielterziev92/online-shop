import {Dialog, DialogContent, DialogHeader, DialogTitle} from "@/components/ui/dialog";

export interface AuthDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    title: string;
    children: React.ReactNode;
}

export const AuthDialog = ({open, onOpenChange, title, children}: AuthDialogProps) => {
    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent>
                <DialogHeader className={'flex flex-col items-center justify-center'}>
                    <DialogTitle className={'text-3xl font-semibold'}>{title}</DialogTitle>
                </DialogHeader>
                {children}
            </DialogContent>
        </Dialog>
    );
}