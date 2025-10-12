import {
  createContext,
  forwardRef,
  PropsWithChildren,
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
import { Display, Year } from "../types";

// * fetches year descriptions from the server.
async function fetchYear(year: number): Promise<Year> {
  const res = await fetch(
    // ! important to encode the year to avoid passing invalid
    // ! urls.
    `/api/php/calendar/getYear?year=${encodeURIComponent(year)}`
  );

  // * for those reading the code, wondering why i named it
  // * year$1, it is because `year` is already used as a parameter
  // * name. i could have named it something else, but i could not
  // * think of a better name. the $1 is just to avoid naming collisions / conflict.
  const year$1 = (await res.json()) as Year;
  return year$1;
}

// * helper factory functions that create helper functions
// ! DO NOT DELETE THESE FUNCTIONS.

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
  setDisplay,
  setCurrentMonth,
  setCurrentYear,
  cache,
  prepareYearFn,
}: CreateGotoFnOptions): GotoFn {
  return async function goto(year: number, month: number): Promise<void> {
    // * the key. i could use String(year) but this is better.
    // * template literals are generally more clearer, especially
    // * if you have an editor coloring your syntax, which
    // * in this case, you can infer that `${someVariable}` is a variable
    // * being used to form a formatted / templated string.
    const key = `${year}`;

    // * ensure the year is loaded.
    // * no-op if already loaded.
    // * this will populate the cache with description data.
    await prepareYearFn(year);

    // * now that the year is loaded, set the display.

    // * the display year is just the cache for the key for the current year.
    const displayYear = cache[key];

    // * the display month is just the current month in the display year.
    const displayMonth = displayYear.months[month];

    // * set the display state. the display is what the server wanted to display.
    // * this is used to render the calendar after server computation.
    // * the client is limited by the strength and the speed of the device,
    // * in a real production app, the server would be much stronger than the client so
    // * the server computation would be faster and better. plus on the added bonus,
    // * it is dynamic, does not depend on the client's architecture, etc.
    setDisplay({
      currentMonth: displayMonth,
      currentYear: displayYear,
    });

    // * set the current month and year state. used for the
    // * controls of the calendar.
    setCurrentMonth(month);
    setCurrentYear(year);
  } as GotoFn;
}

// * relative month setter factory.
function createRelativeMonthSetter({
  gotoFn,
  currentMonth,
  currentYear,
}: CreateRelativeMonthSetterFnOptions): RelativeMonthSetterFn {
  // * relative month setter.
  // * sets the month relative to the state's current month.
  // * e.g: offset = -1; previous month.
  // * e.g: offset = 1; next month
  // * e.g: offset = 0; current month (nothing changes.)
  return function setMonthFromCurrent(offset: number): void {
    // * assume the month will not be the last or previous.
    // * so, the year is just the current year.
    let newYear = currentYear;

    // * move the month by an offset.
    let newMonth = currentMonth + offset;

    // * if the new month is either -1 or 12, then
    // * we need to handle the edge cases of year change.
    // * -1 means from january, to december of previous year.
    // * 12 means from december, to january of next year.
    if (newMonth < 0) {
      newMonth = 11;
      newYear--;
    } else if (newMonth > 11) {
      newMonth = 0;
      newYear++;
    }

    // * go to the new year and month.
    gotoFn(newYear, newMonth);
  } as RelativeMonthSetterFn;
}

// * a context that may have a calendar state, or null.
export const CalendarStateContext = createContext<CalendarState | null>(null);

// * a hook used to access calendar state.
// ! important that this is not ever be deleted in this entire codebase.
// ! if deleted, also delete the whole calendar app feature.
// ! this is streamed down deeply to many components.
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
    // * today.
    // XXX: This is only set once. if the user keeps the tab open,
    // XXX: for like the 11:59PM and then 12:00AM, the today will be wrong.
    // XXX: but fixing will add complexity, so leaving this probably forever.
    const today = useRef(new Date()).current;

    // * is the current month.
    const [currentMonth, setCurrentMonth] = useState<number>(today.getMonth());

    const [currentYear, setCurrentYear] = useState<number>(today.getFullYear());

    // * signal to render skeleton instead.
    const [initializing, setInitializing] = useState(true);

    // * display data. from the server.
    const [display, setDisplay] = useState<Display | null>(null);

    // * cache ref. holds fetched data.
    // ! important that this is a ref so that it does not cause re-renders AND
    // ! is stable across rerenders.
    const cacheRef = useRef<Record<string, Year>>({});

    // * state without helpers. is a stepping stone to create full state.
    // * useMemo avoids unneccessary re-renders of consumers.
    // * go here for the documentation of useMemo:
    // * https://react.dev/reference/react/useMemo
    const stateWithoutHelpers: CalendarStateWithoutHelpers = useMemo(
      () => ({
        today,
        currentMonth,
        currentYear,
        initializing,
        display,
        setCurrentMonth,
        setCurrentYear,
        setDisplay,
        cacheRef,
      }),
      // * dependancies. states that when any of these change,
      // * the state without helpers is re-computed. this is the
      // * probably only place the client will compute anything.
      // * outside of react's own computations.
      [
        today,
        currentMonth,
        currentYear,
        display,
        setCurrentMonth,
        setCurrentYear,
        setDisplay,
        cacheRef,
      ]
    );

    // * create helper functions.

    // * useCallback avoids unneccessary re-creations of these functions
    // * and also avoids unneccessary re-renders of consumers (because of
    // * callback identity change).
    // * go here for the documentation of useCallback:
    // * https://react.dev/reference/react/useCallback
    const prepareYearFn = useCallback(
      createPrepareYearFn({ cache: cacheRef.current }),
      []
    );

    const gotoFn = useCallback(
      createGotoFn({
        setDisplay,
        setCurrentMonth,
        setCurrentYear,
        prepareYearFn,
        cache: cacheRef.current,
      }),
      [setDisplay, setCurrentMonth, setCurrentYear, prepareYearFn]
    );

    const setMonthRelativeFn = useCallback(
      createRelativeMonthSetter({
        gotoFn,
        currentMonth,
        currentYear,
      }),
      [gotoFn, currentMonth, currentYear]
    );

    // * state with the helper functions.
    // * is memoized to avoid unnecessary re-renders and
    // * re-computations in the client.
    const state = useMemo(() => {
      return {
        ...stateWithoutHelpers,
        goto: gotoFn,
        prepareYear: prepareYearFn,
        setMonthRelative: setMonthRelativeFn,
      };
    }, [stateWithoutHelpers, gotoFn, prepareYearFn, setMonthRelativeFn]);

    // * expose the state via ref (forwardRef).
    // * useImperativeHandle is a hook that shortens the ref value
    // * assignment and exposure. can be done in useEffect, but
    // * this is shorter, and cleaner.
    // * go here for the documentation of useImperativeHandle:
    // * https://react.dev/reference/react/useImperativeHandle
    useImperativeHandle(ref, () => state, [state]);

    // * on mount (context mount). load the description
    // * of the display.
    // * this is done only once on mount to initialize the page.
    useEffect(
      () => {
        // * immediately invoke a named async function.
        // * this is async because i do not want to make
        // * .then calls.
        (async function onMount() {
          // * go to the current year and month and load the description
          // * via prepareYear called inside `state.goto`.
          await state.goto(currentYear, currentMonth);

          // * hint that there is now data to show.
          setInitializing(false);
        })();
      },
      [
        /* onload */
      ]
    );

    return (
      <CalendarStateContext.Provider value={state}>
        {children}
      </CalendarStateContext.Provider>
    );
  }
);
