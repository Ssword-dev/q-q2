import React, { PropsWithChildren, ReactElement } from 'react';

const CalendarTableBody = React.memo(function CalendarTableBody({
  children,
}: PropsWithChildren<{}>): ReactElement {
  return <tbody>{children}</tbody>;
});

export default CalendarTableBody;
