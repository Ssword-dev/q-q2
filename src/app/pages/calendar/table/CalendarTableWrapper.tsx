import { cn } from '@/app/lib/utils';
import React, { ReactElement } from 'react';
import { CalendarTableWrapperProps } from '../types';

const CalendarTableWrapper = React.memo(function CalendarTableWrapper({
  children,
  className = '',
}: CalendarTableWrapperProps): ReactElement {
  return (
    <div
      className={cn(
        'relative flex justify-center items-start w-4/5 rounded-3xl',
        className
      )}
    >
      {children}
    </div>
  );
});

export default CalendarTableWrapper;
