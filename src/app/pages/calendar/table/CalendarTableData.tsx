import { useCalendarState } from "../context/CalendarContext";
import CalendarDayTableCell from "./CalendarDayTableCell";

export default function CalendarTableData() {
  const { display } = useCalendarState();
  return display!.currentMonth.days.map((week, wi) => (
    <tr key={wi}>
      {week.map((day, di) => (
        <CalendarDayTableCell day={day} key={di} />
      ))}
    </tr>
  ));
}
