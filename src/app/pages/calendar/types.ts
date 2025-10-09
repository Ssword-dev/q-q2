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
  index: number;
}

export interface HolidayMetadata {
  description: HolidayDescription;
  name: string;
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

export * from './schemas/types';
export * from './context/types';
