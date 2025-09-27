import { CalendarPageState, Day } from "./types";

export function ucfirst(s: string) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

export async function fetchYear(year: number): Promise<any> {
  const res = await fetch(
    `../api/php/v2/calendar/getYear?year=${encodeURIComponent(year)}`
  );
  const year$1 = await res.json();
  return year$1;
}

export async function prepareYearIfNotCached(
  cache: Record<string, any>,
  year: number,
  {}: CalendarPageState
): Promise<void> {
  const key = String(year);

  if (cache[key]) return;

  cache[key] = await fetchYear(year);
}

function formatHelper(n: number) {
  return n < 10 ? `0${n}` : n;
}

export async function goto(
  year: number,
  month: number,
  state: CalendarPageState
): Promise<void> {
  const { setTableData, setCurrentMonth, setCurrentYear, cacheRef } = state;

  const key = `${year}`;

  await prepareYearIfNotCached(cacheRef.current, year, state);

  const data = cacheRef.current[key];
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
}

export function setMonth(offset: number, state: CalendarPageState): void {
  const { currentYear, currentMonth } = state;
  let newYear = currentYear;
  let newMonth = currentMonth + offset;
  if (newMonth < 0) {
    newMonth = 11;
    newYear--;
  } else if (newMonth > 11) {
    newMonth = 0;
    newYear++;
  }

  goto(newYear, newMonth, state);
}
