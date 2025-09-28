// this is just here for fine grained control.
// intentionally split from day cell and holiday cell
// to get much control.
const EmptyCalendarDayCell = () => {
  return (
    <td className="border border-gray-400 w-10 h-10 text-center">&nbsp;</td>
  );
};

export default EmptyCalendarDayCell;
