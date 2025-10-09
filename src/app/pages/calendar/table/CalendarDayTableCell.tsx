import { Day } from "../types";
import CalendarDayCell from "./CalendarDayCell";
import EmptyCalendarDayCell from "./EmptyCalendarDayCell";

export default function CalendarDayTableCell({ day }: { day: Day | null }) {
  return !day ? <EmptyCalendarDayCell /> : <CalendarDayCell {...day} />;
}
