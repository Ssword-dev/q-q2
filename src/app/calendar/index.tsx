import React, {
  useState,
  useRef,
  useEffect,
  PropsWithChildren,
  ReactElement,
} from "react";
import { cn } from "@/lib/utils";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/app/components/ui/hover-card";
import { Button } from "@/app/components/ui/button";
interface CalendarControlsProps {
  setMonth: (offset: number) => void;
  currentMonth: number;
  currentYear: number;
  cache: Record<string, any>;
}

interface CalendarDay {
  day: number;
  isHoliday: boolean;
}

interface CardTableBodyProps {
  tableData: Array<Array<CalendarDay | null>>;
}

interface CalendarDayCellProps {
  day: CalendarDay | null;
}

interface CalendarTableProps extends PropsWithChildren {
  isLoading?: boolean;
}

interface CalendarTableWrapperProps extends PropsWithChildren {
  className?: string;
}

interface CalendarPageState {
  today: Date;
  currentMonth: number;
  currentYear: number;
  tableData: Array<Array<CalendarDay | null>>;
  setCurrentMonth: React.Dispatch<React.SetStateAction<number>>;
  setCurrentYear: React.Dispatch<React.SetStateAction<number>>;
  setTableData: React.Dispatch<Array<Array<CalendarDay | null>>>;
  cacheRef: React.RefObject<Record<string, any>>;
}
