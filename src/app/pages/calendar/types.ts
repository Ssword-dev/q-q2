export interface CalendarControlsProps {
  setMonth: (offset: number) => void;
  currentMonth: number;
  currentYear: number;
  cache: Record<string, any>;
}

export interface Zodiac {
  chinese: string;
}

export interface Holiday {
  name: string;
  type: "public" | "optional" | "observance";
}

export interface Day {
  day: number;
  index: number;
}

export interface Month {
  number_of_days: number;
  days: Array<Array<Day>>;
}

export interface Year {
  year: number;
  leap_year: boolean;
  months: Month[];
  zodiac: Zodiac;
  holidays: Record<string, Holiday>;
}

export interface Display {
  currentYear: Year;
  currentMonth: Month;
}

export interface CardTableBodyProps {
  tableData: Array<Array<Day | null>>;
}

export interface CalendarDayCellProps extends Day {}

export interface CalendarTableProps extends React.PropsWithChildren {
  isLoading?: boolean;
}

export interface CalendarTableWrapperProps extends React.PropsWithChildren {
  className?: string;
}

export * from "./schemas/types";
export * from "./context/types";
