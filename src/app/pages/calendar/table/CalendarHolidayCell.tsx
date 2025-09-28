import { Card, CardTitle, CardContent } from '@/app/lib/dom/components/ui/card';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/app/lib/dom/components/ui/popover';
import { CalendarHolidayCellProps } from '../types';

const CalendarHolidayCell = ({
  day,
  holidayMetadata,
}: CalendarHolidayCellProps) => {
  return (
    <td className="border border-gray-400 w-10 h-10 text-center relative">
      <Popover modal>
        <PopoverTrigger anchor asChild>
          <button className="w-full h-full flex items-center justify-center text-secondary">
            {day}
          </button>
        </PopoverTrigger>

        <PopoverContent
          align="center"
          side="top"
          sideOffset={5}
          className="min-w-20 rounded-lg bg-surface p-0 border-none"
        >
          <Card className="opacity-100 px-4 py-2">
            <CardTitle className="italic">{holidayMetadata.name}</CardTitle>
            <CardContent>
              &ldquo;{holidayMetadata.description.shortDescription}&rdquo;
            </CardContent>
          </Card>
        </PopoverContent>
      </Popover>
    </td>
  );
};

export default CalendarHolidayCell;
