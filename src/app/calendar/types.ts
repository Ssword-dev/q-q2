export interface CalendarControlsProps {
  setMonth: (offset: number) => void;
  currentMonth: number;
  currentYear: number;
  cache: Record<string, any>;
}

export interface HolidayDescription {
  shortDescription: string;
  longDescription: string;
}

export interface Day {
  day: number;
  timestamp: number;
  index: number;
  isHoliday: false;
}

export interface HolidayMetadata {
  description: HolidayDescription;
  name: string;
}

export interface Holiday {
  day: number;
  timestamp: number;
  index: number;
  isHoliday: true;
  holidayMetadata: HolidayMetadata;
}

export type CalendarDay = Day | Holiday;

export interface CardTableBodyProps {
  tableData: Array<Array<CalendarDay | null>>;
}

export interface CalendarDayCellProps extends Day {}

export interface CalendarHolidayCellProps extends Holiday {}

export interface CalendarTableProps extends React.PropsWithChildren {
  isLoading?: boolean;
}

export interface CalendarTableWrapperProps extends React.PropsWithChildren {
  className?: string;
}

export interface CalendarPageState {
  today: Date;
  currentMonth: number;
  currentYear: number;
  tableData: Array<Array<CalendarDay | null>>;
  setCurrentMonth: React.Dispatch<React.SetStateAction<number>>;
  setCurrentYear: React.Dispatch<React.SetStateAction<number>>;
  setTableData: React.Dispatch<Array<Array<CalendarDay | null>>>;
  cacheRef: React.RefObject<Record<string, any>>;
}

export interface StatefulComponentProps {
  state: CalendarPageState;
}
