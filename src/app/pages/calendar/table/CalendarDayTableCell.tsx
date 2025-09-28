import { CalendarDay } from '..';
import CalendarDayCell from './CalendarDayCell';
import CalendarHolidayCell from './CalendarHolidayCell';
import EmptyCalendarDayCell from './EmptyCalendarDayCell';

export default function CalendarDayTableCell({
  day,
}: {
  day: CalendarDay | null;
}) {
  return !day ? (
    <EmptyCalendarDayCell />
  ) : day.isHoliday ? (
    <CalendarHolidayCell {...day} />
  ) : (
    <CalendarDayCell {...day} />
  );
}
