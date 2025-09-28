import React, {
  createRef,
  forwardRef,
  useEffect,
  useRef,
  useState,
} from 'react';
import useCursor, { BoundTarget } from '@/app/lib/shared/hooks/useCursor';
import { cn } from '@/app/lib/utils';

interface CursorProps extends React.ComponentProps<'div'> {
  bound?: BoundTarget;
}

const Cursor = forwardRef<HTMLDivElement, CursorProps>(
  ({ className, style, bound = window, ...props }, ref) => {
    const [{ x, y }, setXY] = useState({ x: 0, y: 0 });
    const selfRef = useRef<HTMLDivElement>(null);
    const cursor = useCursor(bound);

    useEffect(() => {
      if (selfRef.current) {
        const { height, width } = selfRef.current.getBoundingClientRect();
        setXY({
          x: cursor.vec.to.x - width / 2,
          y: cursor.vec.to.y - height / 2,
        });
      }
    }, [cursor.vec.to.x, cursor.vec.to.y]);

    const setRef = (val: HTMLDivElement) => {
      selfRef.current = val;

      if (ref) {
        if (typeof ref === 'function') {
          ref(val);
        } else {
          ref.current = val;
        }
      }
    };

    return (
      <div
        {...props}
        ref={setRef}
        className={cn('absolute', className)}
        style={{
          ...style,
          left: x,
          top: y,
        }}
      />
    );
  }
);

export default Cursor;
