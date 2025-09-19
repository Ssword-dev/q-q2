import { cn } from "@/lib/utils";
import {
  HoverCard,
  HoverCardTrigger,
  HoverCardContent,
} from "@radix-ui/react-hover-card";
import React, { ReactElement } from "react";
import { Button } from "../components/ui/button";
import { monthNames, dayNames } from "./constants";
import { setMonth, ucfirst } from "./functions";
import {
  CalendarControlsProps,
  CalendarDayCellProps,
  CardTableBodyProps,
  CalendarTableProps,
  CalendarTableWrapperProps,
  CalendarPageState,
} from "./types";

// this should not be memoized. this is stateful.
export function CalendarControls({ state }: { state: CalendarPageState }) {
  const { currentMonth, currentYear, cacheRef } = state;
  const cache = cacheRef.current;
  const yearOfAnimal: string | undefined =
    cache[`${currentYear}`]?.zodiac?.chinese;
  return (
    <>
      {/**
       * Disabled on 1970s and earlier.
       * most date time apis are implemented
       * to start counting since the epoch of
       * 1970.
       */}
      <div className="flex justify-between items-center mb-4 w-full">
        <Button
          className="text-primary select-none"
          onClick={() => setMonth(-1, state)}
          disabled={currentMonth <= 0 && currentYear <= 1970}
        >
          Prev
        </Button>
        <HoverCard>
          <HoverCardTrigger>
            <div className="flex flex-col justify-center font-bold">
              {monthNames[currentMonth]} {currentYear}
            </div>
          </HoverCardTrigger>
          <HoverCardContent className="bg-surface">
            {` Year of the ${yearOfAnimal ? ucfirst(yearOfAnimal) : ""}`}
          </HoverCardContent>
        </HoverCard>
        <Button
          className="text-primary select-none"
          onClick={() => setMonth(1, state)}
        >
          Next
        </Button>
      </div>
    </>
  );
}

export const CalendarTableHeader = React.memo(
  function CalendarTableHeader(): ReactElement {
    return (
      <thead>
        <tr>
          {dayNames.map((d) => (
            <th key={d} className="border border-gray-400 px-2 py-1">
              {d}
            </th>
          ))}
        </tr>
      </thead>
    );
  }
);

export const CalendarDayCell = ({ day }: CalendarDayCellProps) => {
  return (
    <td
      className={cn("border border-gray-400 w-10 h-10 text-center", {
        "text-primary": day && day.isHoliday,
      })}
    >
      {day ? day.day : ""}
    </td>
  );
};

export const CalendarTableBody = React.memo(function CalendarTableBody({
  tableData,
}: CardTableBodyProps): ReactElement {
  return (
    <tbody>
      {tableData.map((week, wi) => (
        <tr key={wi}>
          {week.map((day, di) => (
            <CalendarDayCell day={day} key={di} />
          ))}
        </tr>
      ))}
    </tbody>
  );
});

export const CalendarTable = React.memo(function CalendarTable({
  children,
  isLoading = false,
}: CalendarTableProps): ReactElement {
  return (
    <table
      className={cn(
        "w-full border border-seperate rounded-3xl border-gray-400",
        {
          "opacity-0 pointer-events-none absolute": isLoading,
        }
      )}
    >
      {children}
    </table>
  );
});

export const CalendarTableWrapper = React.memo(function CalendarTableWrapper({
  children,
  className = "",
}: CalendarTableWrapperProps): ReactElement {
  return (
    <div
      className={cn(
        "relative flex justify-center items-start w-3/5 rounded-3xl",
        className
      )}
    >
      {children}
    </div>
  );
});
