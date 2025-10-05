import { Button } from "@/app/lib/dom/components/ui/button";
import { motion } from "framer-motion";
import { PropsWithChildren } from "react";
import { useCalendarState } from "../context/CalendarContext";

export default function CalendarControlButton({
  offset = 1,
  disabled = false,
  children,
}: PropsWithChildren<{ offset: number; disabled: boolean }>) {
  const state = useCalendarState();
  return (
    <Button asChild>
      <motion.button
        initial={{ scale: 1 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        transition={{ type: "spring", stiffness: 300, duration: 0.2 }}
        className="text-primary select-none shadow shadow-"
        onClick={() => state.setMonthRelative(offset)}
        disabled={disabled}
      >
        {children}
      </motion.button>
    </Button>
  );
}
