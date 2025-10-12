import React from "react";

interface HolidayListProps {
  children?: React.ReactNode;
}

const HolidayList: React.FC<HolidayListProps> = ({ children }) => {
  return (
    <ul className="w-full h-full no-scrollbar overflow-y-scroll">{children}</ul>
  );
};

export default HolidayList;
