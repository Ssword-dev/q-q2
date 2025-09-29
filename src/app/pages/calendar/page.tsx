import "../../tailwind.css";
import { StrictMode, useEffect, useRef } from "react";
import { createRoot } from "react-dom/client";

// React
import { ReactElement } from "react";

// page components.
import CalendarControls from "./controls/CalendarControls";
import {
  CalendarTableWrapper,
  CalendarTable,
  CalendarTableHeader,
  CalendarTableBody,
  CalendarTableData,
} from "./table";
import { CalendarState } from "./types";
import { Calendar } from "./context/CalendarContext";
import CalendarBackground from "./background";
import ErrorBoundary from "@/app/lib/dom/utils/error-boundary";
import ErrorBoundaryFallback from "./error";

function CalendarPage(): ReactElement {
  // connect to the state.
  const stateRef = useRef<CalendarState>(null);

  useEffect(() => {
    if (!stateRef.current) return;

    const state = stateRef.current;

    state.goto(state.today.getFullYear(), state.today.getMonth());
  }, []);
  return (
    // page container. this is what i actually work with.
    <div
      id="page"
      className="h-full w-full flex flex-col justify-center items-center"
    >
      {/**
       * calendar state provider.
       * streams the calendar state down to its children. allows
       * me to useCalendarState instead of passing state deeply.
       */}
      <Calendar ref={stateRef}>
        {/* actual calendar container. */}
        <div className="flex flex-col justify-center items-center">
          <CalendarControls />
          <CalendarTableWrapper className="w-full">
            <CalendarTable>
              <CalendarTableHeader />
              <CalendarTableBody>
                <CalendarTableData />
              </CalendarTableBody>
            </CalendarTable>
          </CalendarTableWrapper>
        </div>

        {/* react-three animated background. */}
        <CalendarBackground />
      </Calendar>
    </div>
  );
}

createRoot(document.body).render(
  <StrictMode>
    <ErrorBoundary fallback={ErrorBoundaryFallback}>
      <CalendarPage />
    </ErrorBoundary>
  </StrictMode>
);
