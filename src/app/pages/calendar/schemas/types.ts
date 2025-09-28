import z from 'zod';
import calendarBasicControlSchema from './calendar-basic-controls-schema';

export type CalendarBasicControlsSchema = z.infer<
  typeof calendarBasicControlSchema
>;
export type CalendarBasicControlsSchemaInput = z.input<
  typeof calendarBasicControlSchema
>;
