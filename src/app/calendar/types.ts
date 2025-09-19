export interface CalendarControlsProps {
  setMonth: (offset: number) => void;
  currentMonth: number;
  currentYear: number;
  cache: Record<string, any>;
}

export interface CalendarDay {
  day: number;
  isHoliday: boolean;
}

export interface CardTableBodyProps {
  tableData: Array<Array<CalendarDay | null>>;
}

export interface CalendarDayCellProps {
  day: CalendarDay | null;
}

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
