import { Button } from '@/app/lib/dom/components/ui/button';
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from '@/app/lib/dom/components/ui/popover';
import { monthNames } from '../constants';
import { useCalendarState } from '../context/CalendarContext';
import CalendarControlButton from './CalendarControlButton';
import CalendarControlModal from './CalendarControlModal';

export default function CalendarControls() {
  const state = useCalendarState();
  return (
    <>
      {/**
       * Disabled on 1970s and earlier.
       * most date time apis are implemented
       * to start counting since the epoch of
       * 1970.
       */}
      <div className="flex justify-between items-center mb-4 w-full">
        <CalendarControlButton
          offset={-1}
          disabled={state.currentMonth <= 0 && state.currentYear <= 1970}
        >
          Prev
        </CalendarControlButton>

        <div className="flex flex-col justify-center font-bold">
          <Popover modal>
            <PopoverTrigger asChild>
              <Button variant="secondary">
                {monthNames[state.currentMonth]} {state.currentYear}
              </Button>
            </PopoverTrigger>
            <PopoverContent
              side="bottom"
              className="bg-transparent border-none p-0"
            >
              <CalendarControlModal />
            </PopoverContent>
          </Popover>
        </div>

        <CalendarControlButton offset={1} disabled={false}>
          Next
        </CalendarControlButton>
      </div>
    </>
  );
}
