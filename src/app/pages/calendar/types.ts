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

export * from './schemas/types';
export * from './context/types';
