import { Button } from "@/app/lib/dom/components/ui/button";
import { PropsWithChildren } from "react";
import { useCalendarState } from "../context/CalendarContext";

// * button used for next / previous actions
export default function CalendarControlButton({
  offset = 1,
  disabled = false,
  children,
}: PropsWithChildren<{ offset: number; disabled: boolean }>) {
  const state = useCalendarState();
  return (
    <Button
      className="text-primary select-none shadow-none hover:transition-all hover:duration-200 hover:three-dimensional hover:depth-xs active:depth-none! transition-shadow duration-100 active:transition-shadow active:duration-100 cursor-pointer"
      onClick={() => state.setMonthRelative(offset)}
      disabled={disabled}
    >
      {children}
    </Button>
  );
}
