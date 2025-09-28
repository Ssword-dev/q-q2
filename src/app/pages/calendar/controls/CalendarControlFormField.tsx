import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/app/lib/dom/components/ui/form';
import { Input } from '@/app/lib/dom/components/ui/input';
import { Control } from 'react-hook-form';

// text field of calendar.
export default function CalendarFormField({
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
            <Input value={(value as string) ?? ''} {...field} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
