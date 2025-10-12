import { useCalendarState } from "../context/CalendarContext";
import HolidayListTile from "./HolidayListTile";

function HolidayPanelListContent() {
  const { display } = useCalendarState();
  return Object.entries(display!.currentYear.holidays).map(
    ([isoDateString, holiday], _) => {
      console.log(isoDateString, holiday);
      return (
        <HolidayListTile
          key={isoDateString /* this is unique */}
          date={isoDateString /* pass raw date string for lazy computation. */}
          holiday={holiday /* holiday data. */}
        />
      );
    }
  );
}

export default HolidayPanelListContent;
