import { cn } from "@/app/lib/utils";
import React, { ReactElement } from "react";
import { CalendarTableProps } from "../types";
import { useCalendarState } from "../context/CalendarContext";

const CalendarTable = React.memo(
  React.forwardRef<HTMLTableElement, CalendarTableProps>(function CalendarTable(
    { children },
    forwardedRef
  ): ReactElement {
    return (
      <table
        ref={forwardedRef}
        className={cn(
          "w-full border border-seperate rounded-3xl border-gray-400"
        )}
      >
        {children}
      </table>
    );
  })
);

export default CalendarTable;
