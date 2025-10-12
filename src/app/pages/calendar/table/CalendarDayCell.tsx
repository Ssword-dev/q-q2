import { cn } from "@/app/lib/utils";
import { CalendarDayCellProps } from "../types";

const CalendarDayCell = ({ day }: CalendarDayCellProps) => {
  return (
    <td className={cn("border border-border w-10 h-10 text-center")}>{day}</td>
  );
};

export default CalendarDayCell;
