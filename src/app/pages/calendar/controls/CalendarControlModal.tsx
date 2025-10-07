import { Button } from "@/app/lib/dom/components/ui/button";
import { Card, CardTitle, CardContent } from "@/app/lib/dom/components/ui/card";
import { zodResolver } from "@hookform/resolvers/zod";
import { Separator } from "@/app/lib/dom/components/ui/separator";
import {
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
} from "@/app/lib/dom/components/ui/tabs";
import { useForm, Control } from "react-hook-form";
import CalendarControlFormField from "./CalendarControlFormField";
import { monthIndexes } from "../constants";
import {
  CalendarBasicControlsSchema,
  CalendarBasicControlsSchemaInput,
} from "../types";
import calendarBasicControlsSchema from "../schemas/calendar-basic-controls-schema";
import { useCalendarState } from "../context/CalendarContext";
import { Form } from "@/app/lib/dom/components/ui/form";

export default function CalendarControlModal() {
  const state = useCalendarState();
  const resolver = zodResolver<
    CalendarBasicControlsSchemaInput,
    unknown,
    CalendarBasicControlsSchema
  >(calendarBasicControlsSchema);
  const form = useForm<
    CalendarBasicControlsSchemaInput,
    unknown,
    CalendarBasicControlsSchema
  >({
    resolver,
  });
  const { handleSubmit: createOnSubmit, control } = form;

  const handleValidFormSubmit = ({
    year,
    month,
  }: CalendarBasicControlsSchema) => {
    let monthIndex;

    if (typeof month === "string") {
      monthIndex = monthIndexes[month];
    } else {
      monthIndex = month - 1; // users are going to input 1-12.
    }

    state.goto(year, monthIndex);
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
                <CalendarControlFormField
                  label="Year"
                  name="year"
                  control={control as unknown as Control}
                />
                <CalendarControlFormField
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
