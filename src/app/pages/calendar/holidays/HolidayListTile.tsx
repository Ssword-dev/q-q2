import React from "react";
import { Holiday } from "../types";
import {
  CircleQuestionMark,
  Eye,
  FileQuestionMark,
  LucideIcon,
  Star,
} from "lucide-react";

type IconRecord = {
  [K in Holiday["type"]]: LucideIcon;
};

const icons: IconRecord = {
  public: Star,
  optional: CircleQuestionMark,
  observance: Eye,
};
interface HolidayListTileProps {
  date: string;
  holiday: Holiday;
}

function HolidayListTile({ date, holiday }: HolidayListTileProps) {
  const Icon = icons[holiday.type] ?? FileQuestionMark;
  return (
    <li className="h-1/5 w-full bg-surface border-b-[1px] border-text/20 last:border-0 flex flex-row justify-between items-center px-2">
      <div className="flex flex-row justify-start items-center gap-2">
        <Icon className="stroke-text" />
        <span className="font-bold">{holiday.name}</span>
      </div>
      <span className="text-sm italic">{date}</span>
    </li>
  );
}

export default HolidayListTile;
