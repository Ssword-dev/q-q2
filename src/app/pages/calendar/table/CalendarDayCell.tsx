import { cn } from '@/app/lib/utils';
import { CalendarDayCellProps } from '../types';

const CalendarDayCell = ({ day, index }: CalendarDayCellProps) => {
  return (
    <td
      className={cn('border border-gray-400 w-10 h-10 text-center', {
        'text-primary': index === 0, // add text-primary (strong) if sunday
      })}
    >
      {day}
    </td>
  );
};

export default CalendarDayCell;
