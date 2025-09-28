import { cn } from '@/app/lib/utils';
import React, { ReactElement } from 'react';
import { CalendarTableProps } from '../types';

const CalendarTable = React.memo(
  React.forwardRef<HTMLTableElement, CalendarTableProps>(function CalendarTable(
    { children, isLoading = false },
    forwardedRef
  ): ReactElement {
    return (
      <table
        ref={forwardedRef}
        className={cn(
          'w-full border border-seperate rounded-3xl border-gray-400',
          {
            'opacity-0 pointer-events-none absolute': isLoading,
          }
        )}
      >
        {children}
      </table>
    );
  })
);

export default CalendarTable;
