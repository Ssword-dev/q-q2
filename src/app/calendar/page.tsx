import "../tailwind.css";
import { ReactElement, useState, useRef, useEffect, StrictMode } from "react";
import { createRoot } from "react-dom/client";
import {
  CalendarTableWrapper,
  CalendarTable,
  CalendarTableHeader,
  CalendarTableBody,
  CalendarControls,
} from "./components";
import { goto } from "./functions";
import { CalendarDay, CalendarPageState } from "./types";

export function CalendarPage(): ReactElement {
  const today = new Date();
  const [currentMonth, setCurrentMonth] = useState<number>(today.getMonth());
  const [currentYear, setCurrentYear] = useState<number>(today.getFullYear());
  const [tableData, setTableData] = useState<Array<Array<CalendarDay | null>>>(
    []
  );
  const cacheRef = useRef<Record<string, any>>({});
  const state: CalendarPageState = {
    today,
    currentMonth,
    currentYear,
    tableData,
    setCurrentMonth,
    setCurrentYear,
    setTableData,
    cacheRef,
  };

  useEffect(() => {
    goto(currentYear, currentMonth, state);
    // i disabled this warning because well its false alarm here.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div
      id="page"
      className="h-full w-full flex flex-col justify-center items-center"
    >
      {/* Calendar container */}
      <div className="flex flex-col justify-center items-center">
        <CalendarControls state={state} />
        <CalendarTableWrapper className="w-full">
          <CalendarTable>
            <CalendarTableHeader />
            <CalendarTableBody tableData={tableData} />
          </CalendarTable>
        </CalendarTableWrapper>
      </div>
    </div>
  );
}

createRoot(document.body).render(
  <StrictMode>
    <CalendarPage />
  </StrictMode>
);
