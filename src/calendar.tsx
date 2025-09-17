import React, {
  useState,
  useRef,
  useEffect,
  PropsWithChildren,
  ReactElement,
} from "react";
import gif_dialga from "./assets/dialga.gif";
import aud_dialga from "./assets/dialga_cry.mp3";
import { cn } from "@/lib/utils";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { Button } from "@/components/ui/button";

const monthNames = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
] as const;

const dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"] as const;

function Dialga(props: React.ImgHTMLAttributes<HTMLImageElement>) {
  return (
    <img
      {...props}
      src={gif_dialga}
      alt="Dialga"
      className="block w-32 aspect-square cursor-pointer"
    />
  );
}

interface CalendarControlsProps {
  setMonth: (offset: number) => void;
  currentMonth: number;
  currentYear: number;
  cache: Record<string, any>;
}

function ucfirst(s: string) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

// this should not be memoized. this is stateful.
function CalendarControls({
  setMonth,
  currentMonth,
  currentYear,
  cache,
}: CalendarControlsProps) {
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
          onClick={() => setMonth(-1)}
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
          onClick={() => setMonth(1)}
        >
          Next
        </Button>
      </div>
    </>
  );
}

function CalendarLoadingOverlay(): ReactElement {
  return (
    <>
      {/* imma just hide the loading spinner when not in use. */}
      <div className="absolute flex justify-center items-center bg-white/80 w-full h-full">
        <Dialga />
      </div>
    </>
  );
}

const CalendarTableHeader = React.memo(
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

interface CalendarDay {
  day: number;
}

interface CardTableBodyProps {
  tableData: Array<Array<CalendarDay | null>>;
}

const CalendarTableBody = React.memo(function CalendarTableBody({
  tableData,
}: CardTableBodyProps): ReactElement {
  return (
    <tbody>
      {tableData.map((week, wi) => (
        <tr key={wi}>
          {week.map((day, di) => (
            <td
              key={di}
              className="border border-gray-400 w-10 h-10 text-center"
            >
              {day ? day.day : ""}
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  );
});

interface CalendarTableProps extends PropsWithChildren {
  isLoading?: boolean;
}

const CalendarTable = React.memo(function CalendarTable({
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

interface CalendarTableWrapperProps extends PropsWithChildren {
  className?: string;
}

const CalendarTableWrapper = React.memo(function CalendarTableWrapper({
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

export default function CalendarPage(): ReactElement {
  const today = new Date();
  const [currentMonth, setCurrentMonth] = useState<number>(today.getMonth());
  const [currentYear, setCurrentYear] = useState<number>(today.getFullYear());
  const [tableData, setTableData] = useState<Array<Array<CalendarDay | null>>>(
    []
  );
  const cacheRef = useRef<Record<string, any>>({});

  async function fetchYear(year: number): Promise<any> {
    const res = await fetch(
      `./api/calendar/getYear?year=${encodeURIComponent(year)}`
    );
    const year$1 = await res.json();
    return year$1;
  }

  async function prepareYearIfNotCached(
    cache: Record<string, any>,
    year: number
  ): Promise<void> {
    const key = String(year);

    if (cache[key]) return;

    cache[key] = await fetchYear(year);
  }

  async function goto(year: number, month: number): Promise<void> {
    const key = `${year}`;

    await prepareYearIfNotCached(cacheRef.current, year);

    const data = cacheRef.current[key];
    const mat: Array<Array<CalendarDay | null>> = Array.from(
      { length: 6 },
      () => Array(7).fill(null)
    );

    let p = 0,
      cy = 0;

    const monthData = data.months[month];
    const startIndex: number = monthData.baseIndex ?? 0;

    while (p < monthData.days.length) {
      const week = mat[cy];
      let cx = cy === 0 ? startIndex : 0;
      while (cx < 7 && p < monthData.days.length) {
        week[cx] = monthData.days[p++];
        cx++;
      }
      cy++;
    }

    setTableData(mat);
  }

  function setMonth(offset: number): void {
    let newYear = currentYear;
    let newMonth = currentMonth + offset;
    if (newMonth < 0) {
      newMonth = 11;
      newYear--;
    } else if (newMonth > 11) {
      newMonth = 0;
      newYear++;
    }
    setCurrentYear(newYear);
    setCurrentMonth(newMonth);
    goto(newYear, newMonth);
  }

  useEffect(() => {
    goto(currentYear, currentMonth);
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
        <CalendarControls
          currentMonth={currentMonth}
          currentYear={currentYear}
          setMonth={setMonth}
          cache={cacheRef.current}
        />
        <CalendarTableWrapper className="w-full">
          <CalendarTable>
            <CalendarTableHeader />
            <CalendarTableBody tableData={tableData} />
          </CalendarTable>
        </CalendarTableWrapper>

        {/* <AudioPlayer src={aud_dialga} ref={dialgaCryAudioRef} /> */}
      </div>
    </div>
  );
}
