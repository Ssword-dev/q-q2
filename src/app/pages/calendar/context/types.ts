import { Day, Display } from "../types";

type CalendarMonth = number;
type CalendarYear = number;

// the day is an object because it must contain metadata.
type CalendarTableData = Array<Array<Day | null>>;
type CalendarMonthSetter = React.Dispatch<React.SetStateAction<number>>;
type CalendarYearSetter = React.Dispatch<React.SetStateAction<number>>;
type CalendarDisplaySetter = React.Dispatch<
  React.SetStateAction<Display | null>
>;
type CalendarTableDataSetter = React.Dispatch<Array<Array<Day | null>>>;
type CalendarCacheRef = React.RefObject<Record<string, any>>;

interface CalendarStateWithoutHelpers {
  today: Date;
  currentMonth: CalendarMonth;
  currentYear: CalendarYear;
  initializing: boolean;
  display: Display | null; // what the server wanted to display.
  setCurrentMonth: CalendarMonthSetter;
  setCurrentYear: CalendarYearSetter;
  setDisplay: CalendarDisplaySetter;
  cacheRef: CalendarCacheRef;
}

interface CalendarState extends CalendarStateWithoutHelpers {
  goto: GotoFn;
  setMonthRelative: RelativeMonthSetterFn;
  prepareYear: PrepareYearFn;
}

interface CreatePrepareYearFnOptions {
  cache: CalendarCacheRef["current"];
}

interface PrepareYearFn {
  name: "prepareYear";
  (year: number): Promise<void>;
}

interface CreateGotoFnOptions
  extends Pick<
    CalendarState,
    "setDisplay" | "setCurrentMonth" | "setCurrentYear"
  > {
  cache: CalendarCacheRef["current"];
  prepareYearFn: PrepareYearFn;
}

interface GotoFn {
  name: "goto";
  (year: number, month: number): Promise<void>;
}

interface CreateRelativeMonthSetterFnOptions {
  currentMonth: number;
  currentYear: number;
  gotoFn: GotoFn;
}

interface RelativeMonthSetterFn {
  name: "setMonthRelative";
  (offset?: number): void;
}

export type {
  // Primitives
  CalendarMonth,
  CalendarYear,

  // State and DS
  CalendarTableData,
  CalendarStateWithoutHelpers,
  CalendarState,

  // Setters and Refs
  CalendarMonthSetter,
  CalendarYearSetter,
  CalendarTableDataSetter,
  CalendarCacheRef,

  // Helper factory function options
  CreatePrepareYearFnOptions,
  CreateGotoFnOptions,
  CreateRelativeMonthSetterFnOptions,

  // Function types
  PrepareYearFn,
  GotoFn,
  RelativeMonthSetterFn,
};
