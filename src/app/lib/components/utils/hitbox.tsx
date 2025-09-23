import { cn } from "@/app/lib/utils";
import { PropsWithChildren, useMemo } from "react";

interface HitboxProps extends PropsWithChildren {
  className?: string;
  inline?: boolean;
}

function Hitbox({ children, className = "", inline = false }: HitboxProps) {
  const Tag = useMemo(() => (inline ? "span" : "div"), [inline]);
  return (
    <Tag className={cn(className, "pointer-events-auto!")}>{children}</Tag>
  );
}

export default Hitbox;
