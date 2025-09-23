// React
import React, { PropsWithChildren, ReactElement, useEffect } from "react";

// utilities
import { cn } from "@/app/lib/utils";

// Components
import { Button } from "@/app/lib/components/ui/button";
import { Card, CardContent, CardTitle } from "@/app/lib/components/ui/card";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/app/lib/components/ui/popover";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/app/lib/components/ui/form";
import { Input } from "@/app/lib/components/ui/input";
import { Separator } from "../lib/components/ui/separator";

// framer motion
import { motion } from "framer-motion";

// lucide react
import {} from "lucide-react";

import {
  Tabs,
  TabsList,
  TabsContent,
  TabsTrigger,
} from "@/app/lib/components/ui/tabs";

// validation library
import z from "zod";

// forms
import { Control, useForm } from "react-hook-form";

// rhf + zod integration
import { zodResolver } from "@hookform/resolvers/zod";

// constants
import { monthNames, dayNames, monthIndexes } from "./constants";

// environment functions
import { goto, setMonth } from "./functions";

// types
import {
  CalendarDayCellProps,
  CardTableBodyProps,
  CalendarTableProps,
  CalendarTableWrapperProps,
  CalendarPageState,
  CalendarHolidayCellProps,
  CalendarDay,
  StatefulComponentProps,
} from "./types";

const yearSchema = z.preprocess(
  (inp) => {
    console.log(JSON.stringify(inp));
    if (typeof inp !== "string") {
      return inp;
    }

    if (/\d+/.test(inp)) {
      return parseInt(inp);
    }

    return inp;
  },
  z
    .number({
      error: "year must be a number",
    })
    .min(1970, {
      error: "year must be 1970 or later.",
    })
    .max(9999, {
      error: "year must be reasonable.",
    })
);

const monthSchema = z.union([
  // numeric.
  z
    .int()
    .min(1, { error: "month must be greater than or equal 1 (January)." })
    .max(12, { error: "month must be less than or equal 12 (December)." }),
  // string
  z.preprocess((val) => {
    if (typeof val !== "string") return val;
    // Normalize first letter uppercase, rest lowercase
    return val[0].toUpperCase() + val.slice(1).toLowerCase();
  }, z.enum(monthNames)),
]);

const calendarControlSchema = z.object({
  year: yearSchema,
  month: monthSchema,
});

// infered types.
type CalendarControlSchemaType = z.infer<typeof calendarControlSchema>;
type CalendarControlSchemaInputType = z.input<typeof calendarControlSchema>;

// text field of calendar.
export function CalendarFormField({
  name,
  label,
  control,
}: {
  name: string;
  label: string;
  control: Control;
}) {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field: { value, ...field } }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <Input value={(value as string) ?? ""} {...field} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}

// calendar control modal.
// this is tabbed.
// first tab is basic tab, does not have the
// one with country and subdivision specification.
export function CalendarControlModal({ state }: StatefulComponentProps) {
  const resolver = zodResolver<
    CalendarControlSchemaInputType,
    unknown,
    CalendarControlSchemaType
  >(calendarControlSchema);
  const form = useForm<
    CalendarControlSchemaInputType,
    unknown,
    CalendarControlSchemaType
  >({
    resolver,
  });
  const { handleSubmit: createOnSubmit, control } = form;

  const handleValidFormSubmit = ({
    year,
    month,
  }: CalendarControlSchemaType) => {
    let monthIndex;

    if (typeof month === "string") {
      monthIndex = monthIndexes[month];
    } else {
      monthIndex = month;
    }

    goto(year, monthIndex, state);
  };

  const onSubmit = createOnSubmit(handleValidFormSubmit);

  return (
    <Card className="z-10 h-full w-full px-4 py-2">
      <Tabs>
        <TabsList className="flex flex-row justify-between w-full">
          <TabsTrigger value="basic">Basic</TabsTrigger>
          <Separator orientation="vertical" />
          <TabsTrigger value="advanced">Advanced</TabsTrigger>
        </TabsList>
        <TabsContent value="basic">
          <CardTitle>Calendar Settings</CardTitle>
          <CardContent className="flex flex-col gap-6">
            <Form {...form}>
              <form className="flex flex-col gap-4 pt-4" onSubmit={onSubmit}>
                <CalendarFormField
                  label="Year"
                  name="year"
                  control={control as unknown as Control}
                />
                <CalendarFormField
                  label="Month"
                  name="month"
                  control={control as unknown as Control}
                />
                <Button type="submit">Submit</Button>
              </form>
            </Form>
          </CardContent>
        </TabsContent>
        <TabsContent value="advanced">
          <CardTitle>Advanced Calendar Settings</CardTitle>
          <CardContent>
            <Form {...form}>
              <form className="flex flex-col gap-4 pt-4" onSubmit={onSubmit}>
                <CalendarFormField
                  label="Year"
                  name="year"
                  control={control as unknown as Control}
                />
                <CalendarFormField
                  label="Month"
                  name="month"
                  control={control as unknown as Control}
                />
                <Button type="submit">Submit</Button>
              </form>
            </Form>
          </CardContent>
        </TabsContent>
      </Tabs>
    </Card>
  );
}

export function CalendarControlButton({
  state,
  offset = 1,
  disabled = false,
  children,
}: StatefulComponentProps &
  PropsWithChildren<{ offset: number; disabled: boolean }>) {
  return (
    <Button asChild>
      <motion.button
        initial={{ scale: 1 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        transition={{ type: "spring", stiffness: 300, duration: 0.2 }}
        className="text-primary select-none"
        onClick={() => setMonth(offset, state)}
        disabled={disabled}
      >
        {children}
      </motion.button>
    </Button>
  );
}

export function CalendarControls({ state }: StatefulComponentProps) {
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
          state={state}
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
              <CalendarControlModal state={state} />
            </PopoverContent>
          </Popover>
        </div>

        <CalendarControlButton state={state} offset={1} disabled={false}>
          Next
        </CalendarControlButton>
      </div>
    </>
  );
}

export const CalendarTableHeader = React.memo(
  function CalendarTableHeader(): ReactElement {
    return (
      <thead>
        <tr>
          {dayNames.map((d) => (
            <th key={d} className="border border-gray-400 px-2 py-1">
              {d}
            </th>
          ))}
        </tr>
      </thead>
    );
  }
);

export const EmptyCalendarDayCell = () => {
  return (
    <td className="border border-gray-400 w-10 h-10 text-center">&nbsp;</td>
  );
};

export const CalendarSundayCell = ({ day }: CalendarDayCellProps) => {
  return (
    <td className="border border-gray-400 w-10 h-10 text-center text-primary">
      {day}
    </td>
  );
};

export const CalendarDayCell = ({ day }: CalendarDayCellProps) => {
  return (
    <td className="border border-gray-400 w-10 h-10 text-center">{day}</td>
  );
};

export const CalendarHolidayCell = ({
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

export function CalendarDayDisplay({ day }: { day: CalendarDay | null }) {
  return !day ? (
    <EmptyCalendarDayCell />
  ) : day.isHoliday ? (
    <CalendarHolidayCell {...day} />
  ) : day.index === 0 ? (
    <CalendarSundayCell {...day} />
  ) : (
    <CalendarDayCell {...day} />
  );
}

export function CalendarTableData({
  data,
}: {
  data: Array<Array<CalendarDay | null>>;
}) {
  return data.map((week, wi) => (
    <tr key={wi}>
      {week.map((day, di) => (
        <CalendarDayDisplay day={day} key={di} />
      ))}
    </tr>
  ));
}

export const CalendarTableBody = React.memo(function CalendarTableBody({
  tableData,
}: CardTableBodyProps): ReactElement {
  return (
    <tbody>
      <CalendarTableData data={tableData} />
    </tbody>
  );
});

export const CalendarTable = React.memo(function CalendarTable({
  children,
  isLoading = false,
}: CalendarTableProps): ReactElement {
  return (
    <table
      className={cn(
        "w-full border border-seperate rounded-3xl border-gray-400",
        {
          "opacity-0 pointer-events-none absolute": isLoading,
        }
      )}
    >
      {children}
    </table>
  );
});

export const CalendarTableWrapper = React.memo(function CalendarTableWrapper({
  children,
  className = "",
}: CalendarTableWrapperProps): ReactElement {
  return (
    <div
      className={cn(
        "relative flex justify-center items-start w-3/5 rounded-3xl",
        className
      )}
    >
      {children}
    </div>
  );
});
