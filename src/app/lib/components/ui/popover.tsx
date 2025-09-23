"use client";

import * as React from "react";
import { useEffect, useState, useRef } from "react";
import * as PopoverPrimitive from "@radix-ui/react-popover";
import { motion, AnimatePresence, AnimationDefinition } from "framer-motion";
import { cn } from "@/app/lib/utils";
import useViewport from "../../hooks/useViewport";

interface PopoverContextValue {
  open: boolean;
}

const PopoverContext = React.createContext<PopoverContextValue | null>(null);

const usePopover = () => {
  const context = React.useContext(PopoverContext);

  if (!context) {
    throw new Error("usePopover can only be used inside a <Popover />");
  }

  return context;
};

function Popover({
  defaultOpen = false,
  ...props
}: React.ComponentProps<typeof PopoverPrimitive.Root>) {
  const [open, setOpen] = React.useState(defaultOpen);
  return (
    <PopoverContext.Provider value={{ open: open }}>
      <PopoverPrimitive.Root
        open={open}
        onOpenChange={setOpen}
        data-slot="popover"
        {...props}
      />
    </PopoverContext.Provider>
  );
}

interface PopoverTriggerProps
  extends React.ComponentProps<typeof PopoverPrimitive.Trigger> {
  /**
   * Whether to anchor the popover in the trigger (or explicitly anchor via PopoverAnchor)
   */
  anchor?: boolean;
}

function PopoverTrigger({ anchor = false, ...props }: PopoverTriggerProps) {
  const jsx = React.useMemo(() => {
    if (anchor) {
      return (
        <PopoverPrimitive.Anchor>
          <PopoverPrimitive.Trigger data-slot="popover-trigger" {...props} />
        </PopoverPrimitive.Anchor>
      );
    } else {
      return (
        <PopoverPrimitive.Trigger data-slot="popover-trigger" {...props} />
      );
    }
  }, [anchor]);

  return jsx;
}

type BasePopoverContentProps = React.ComponentProps<
  typeof PopoverPrimitive.Content
>;

/**
 * The origin classes for
 * each side where the popover is displayed.
 */
const origins = {
  top: "origin-bottom",
  bottom: "origin-top",
  left: "origin-right",
  right: "origin-left",
} as const;

const contentAnimationVariants = {
  initial: {
    scale: 0,
  },
  enter: {
    scale: 1,
  },
  exit: {
    scale: 0,
  },
} as const;

function PopoverContent({
  className,
  align = "center",
  side = "top",
  sideOffset = 4,
  children,
  ...props
}: BasePopoverContentProps) {
  const { open } = usePopover();

  return (
    <PopoverPrimitive.Portal forceMount>
      <AnimatePresence>
        {/** Note to self: The presence can only animate direct child it seems. */}
        {open && (
          <PopoverPrimitive.Content
            asChild
            align={align}
            side={side}
            sideOffset={sideOffset}
            {...props}
          >
            <motion.div
              variants={contentAnimationVariants}
              initial="initial"
              animate="enter"
              exit="exit"
              transition={{ duration: 0.2 }}
              className={cn(
                "bg-surface text-text z-50 w-72 rounded-md border p-4 shadow-md outline-hidden",
                origins[side],
                className
              )}
            >
              {children}
              <PopoverPrimitive.PopoverArrow />
            </motion.div>
          </PopoverPrimitive.Content>
        )}
      </AnimatePresence>
    </PopoverPrimitive.Portal>
  );
}

function PopoverAnchor({
  ...props
}: React.ComponentProps<typeof PopoverPrimitive.Anchor>) {
  return <PopoverPrimitive.Anchor data-slot="popover-anchor" {...props} />;
}

export { Popover, PopoverTrigger, PopoverContent, PopoverAnchor };

// previous code for popover content

// const viewport = useViewport();
// const [baseSide, setBaseSide] = useState<BasePopoverContentProps["side"]>(
//   () => (side === "auto" ? "top" : side)
// );
// const ref = useRef<HTMLDivElement>(null);

// useEffect(() => {
//   if (!ref.current) return;
//   if (side === "auto") {
//     const rect = ref.current.getBoundingClientRect();
//     const { x, y, width, height } = rect;

//     // clip points
//     const clipPointX = x + width;
//     const clipPointY = y + height;

//     // too far to the right.
//     if (clipPointX < viewport.width && baseSide !== "left") {
//       setBaseSide("left");
//     } else if (clipPointX > 0 && baseSide !== "right") {
//       setBaseSide("right");
//     } else if (clipPointY < viewport.height && baseSide !== "top") {
//       setBaseSide("top");
//     } else if (clipPointY > 0 && baseSide !== "bottom") {
//       setBaseSide("bottom");
//     } else {
//     } // no-op. just for semantics.
//   }
// }, [align, viewport]);
