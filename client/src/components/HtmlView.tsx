import { Card } from "./ui/card";
import { useState, useEffect } from "react";
import { ExternalLink, ChevronRight } from "lucide-react";
import { Button } from "./ui/button";
import { cn } from "@/lib/utils";

interface HtmlViewProps {
    url?: string;
    onClose?: () => void;
}

const HtmlView = ({ url, onClose }: HtmlViewProps) => {
    const [iframeError, setIframeError] = useState(false);

    useEffect(() => {
        setIframeError(false);
    }, [url]);

    if (!url) {
        return null;
    }

    const handleOpenInNewTab = () => {
        window.open(url, '_blank');
    };

    return (
        <Card className="border-none w-[30%] bg-black/20 h-full p-0 overflow-hidden animate-slide-from-right relative group">
            <Button
                onClick={onClose}
                className={cn(
                    "absolute left-1 top-1/2 -translate-y-1/2 w-8 h-14",
                    "bg-slate-500/20 hover:bg-slate-600/30",
                    "rounded-sm flex items-center justify-center",
                    "backdrop-blur-sm",
                    "opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                )}
            >
                <div className="scale-[2]">
                    <ChevronRight className="text-white" />
                </div>
            </Button>
            {iframeError ? (
                <div className="w-full h-full flex flex-col items-center justify-center text-white">
                    <p className="mb-4 text-center">This website cannot be displayed in an iframe.</p>
                    <Button
                        onClick={handleOpenInNewTab}
                        className="flex items-center gap-2 bg-white text-slate-500 hover:bg-slate-100"
                    >
                        Open in new tab <ExternalLink size={16} />
                    </Button>
                </div>
            ) : (
                <iframe
                    src={url}
                    className="w-full h-full border-0"
                    title="HTML Content"
                    onError={() => setIframeError(true)}
                    sandbox="allow-same-origin allow-scripts"
                />
            )}
        </Card>
    );
}

export default HtmlView;