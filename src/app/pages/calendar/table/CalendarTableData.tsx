import { useCalendarState } from '../context/CalendarContext';
import CalendarDayTableCell from './CalendarDayTableCell';

export default function CalendarTableData() {
  const { tableData } = useCalendarState();
  return tableData.map((week, wi) => (
    <tr key={wi}>
      {week.map((day, di) => (
        <CalendarDayTableCell day={day} key={di} />
      ))}
    </tr>
  ));
}
