import useCursor from "@/app/lib/hooks/useCursor";
import "../tailwind.css";
import { createRoot } from "react-dom/client";
import { Card, CardContent, CardTitle } from "@/app/lib/components/ui/card";
import Cursor from "../lib/components/ui/cursor";
import { useRef } from "react";
import { SwordIcon } from "lucide-react";

function TestPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  return (
    <>
      <Card ref={containerRef}>
        <CardTitle>Sword Cursor</CardTitle>
        <CardContent>Hover me to change your cursor to a sword.</CardContent>
        <Cursor
          bound={containerRef}
          className={`
            w-max h-max cursor-none
        `}
        >
          <SwordIcon></SwordIcon>
        </Cursor>
      </Card>
    </>
  );
}

createRoot(document.getElementById("root")!).render(<TestPage />);
