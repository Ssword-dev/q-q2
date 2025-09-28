import z from 'zod';
import { monthNames } from '../constants';

const yearSchema = z.preprocess(
  (inp) => {
    console.log(JSON.stringify(inp));
    if (typeof inp !== 'string') {
      return inp;
    }

    if (/\d+/.test(inp)) {
      return parseInt(inp);
    }

    return inp;
  },
  z
    .number({
      error: 'year must be a number',
    })
    .min(1970, {
      error: 'year must be 1970 or later.',
    })
    .max(9999, {
      error: 'year must be reasonable.',
    })
);

const monthSchema = z.union([
  // numeric.
  z
    .int()
    .min(1, { error: 'month must be greater than or equal 1 (January).' })
    .max(12, { error: 'month must be less than or equal 12 (December).' }),
  // string
  z.preprocess((val) => {
    if (typeof val !== 'string') return val;
    // Normalize first letter uppercase, rest lowercase
    return val[0].toUpperCase() + val.slice(1).toLowerCase();
  }, z.enum(monthNames)),
]);

const calendarBasicControlsSchema = z.object({
  year: yearSchema,
  month: monthSchema,
});

export default calendarBasicControlsSchema;
