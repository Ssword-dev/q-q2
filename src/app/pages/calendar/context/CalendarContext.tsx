import {
  createContext,
  forwardRef,
  PropsWithChildren,
  RefObject,
  useCallback,
  useContext,
  useEffect,
  useImperativeHandle,
  useMemo,
  useRef,
  useState,
} from "react";
import {
  CalendarState,
  CalendarStateWithoutHelpers,
  CreateGotoFnOptions,
  CreatePrepareYearFnOptions,
  CreateRelativeMonthSetterFnOptions,
  GotoFn,
  PrepareYearFn,
  RelativeMonthSetterFn,
} from "./types";
import { CalendarDay, Day } from "../types";

async function fetchYear(year: number): Promise<any> {
  const res = await fetch(
    `/api/php/calendar/getYear?year=${encodeURIComponent(year)}`
  );
  const year$1 = await res.json();
  return year$1;
}

function createPrepareYearFn({
  cache,
}: CreatePrepareYearFnOptions): PrepareYearFn {
  return async function prepareYear(year: number) {
    const key = String(year);
    if (cache[key]) return;
    cache[key] = await fetchYear(year);
  } as PrepareYearFn;
}

function createGotoFn({
  setTableData,
  setCurrentMonth,
  setCurrentYear,
  cache,
  prepareYearFn,
}: CreateGotoFnOptions): GotoFn {
  return async function goto(year: number, month: number): Promise<void> {
    const key = `${year}`;

    await prepareYearFn(year);

    const data = cache[key];
    const mat: Array<Array<Day | null>> = Array.from({ length: 6 }, () =>
      Array(7).fill(null)
    );

    let p = 0,
      cy = 0;

    const monthData = data.months[month];
    const startIndex: number = monthData.baseIndex ?? 0;

    while (p < monthData.days.length) {
      const week = mat[cy];
      let cx = cy === 0 ? startIndex : 0;
      while (cx < 7 && p < monthData.days.length) {
        const dayData = monthData.days[p++];

        week[cx] = dayData;
        cx++;
      }
      cy++;
    }

    setTableData(mat);
    setCurrentMonth(month);
    setCurrentYear(year);
  } as GotoFn;
}

function createRelativeMonthSetter({
  gotoFn,
  currentMonth,
  currentYear,
}: CreateRelativeMonthSetterFnOptions): RelativeMonthSetterFn {
  return function setMonthFromCurrent(offset: number): void {
    let newYear = currentYear;
    let newMonth = currentMonth + offset;
    if (newMonth < 0) {
      newMonth = 11;
      newYear--;
    } else if (newMonth > 11) {
      newMonth = 0;
      newYear++;
    }

    gotoFn(newYear, newMonth);
  } as RelativeMonthSetterFn;
}

export const CalendarStateContext = createContext<CalendarState | null>(null);

export const useCalendarState = () => {
  const calendarState = useContext(CalendarStateContext);

  if (!calendarState) {
    throw new Error(
      "Calendar cannot be used without a calendar provider anscestor."
    );
  }

  return calendarState;
};

export const Calendar = forwardRef<CalendarState, PropsWithChildren>(
  ({ children }, ref) => {
    const today = useRef(new Date()).current;
    const [currentMonth, setCurrentMonth] = useState<number>(today.getMonth());
    const [currentYear, setCurrentYear] = useState<number>(today.getFullYear());
    const [tableData, setTableData] = useState<
      Array<Array<CalendarDay | null>>
    >([]);
    const cacheRef = useRef<Record<string, any>>({});
    const stateWithoutHelpers: CalendarStateWithoutHelpers = useMemo(
      () => ({
        today,
        currentMonth,
        currentYear,
        tableData,
        setCurrentMonth,
        setCurrentYear,
        setTableData,
        cacheRef,
      }),
      [
        today,
        currentMonth,
        currentYear,
        tableData,
        setCurrentMonth,
        setCurrentYear,
        setTableData,
        cacheRef,
      ]
    );

    const prepareYearFn = useCallback(
      createPrepareYearFn({ cache: cacheRef.current }),
      []
    );

    const gotoFn = useCallback(
      createGotoFn({
        setTableData,
        setCurrentMonth,
        setCurrentYear,
        prepareYearFn,
        cache: cacheRef.current,
      }),
      [setTableData, setCurrentMonth, setCurrentYear, prepareYearFn]
    );

    const setMonthRelativeFn = useCallback(
      createRelativeMonthSetter({
        gotoFn,
        currentMonth,
        currentYear,
      }),
      [gotoFn, currentMonth, currentYear]
    );

    const state = useMemo(() => {
      return {
        ...stateWithoutHelpers,
        goto: gotoFn,
        prepareYear: prepareYearFn,
        setMonthRelative: setMonthRelativeFn,
      };
    }, [stateWithoutHelpers, gotoFn, prepareYearFn, setMonthRelativeFn]);

    // useEffect(() => {
    //   if (ref) {
    //     if (typeof ref === "function") {
    //       ref(state);
    //     } else if (typeof ref === "object" && "current" in ref) {
    //       ref.current = state;
    //     } else {
    //       throw new Error("Invalid Ref!");
    //     }
    //   }
    // }, [ref, state]);

    useImperativeHandle(ref, () => state, [state]);

    return (
      <CalendarStateContext.Provider value={state}>
        {children}
      </CalendarStateContext.Provider>
    );
  }
);
