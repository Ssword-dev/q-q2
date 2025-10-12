import { Card, CardContent } from "@/app/lib/dom/components/ui/card";
import { PropsWithChildren } from "react";

function HolidayPanel({ children }: PropsWithChildren) {
  return (
    <Card className="h-full w-full">
      <CardContent className="overflow-y-hidden">{children}</CardContent>
    </Card>
  );
}

export default HolidayPanel;
