import React, {
  createContext,
  PropsWithChildren,
  useContext,
  useEffect,
  useState,
} from "react";
import { useCalendarState } from "../context/CalendarContext";

interface CalendarTableBodyContentContextValue {
  setFallback: (fallback: React.ReactNode) => void;
  setContent: (content: React.ReactNode) => void;
  fallback?: React.ReactNode;
  content?: React.ReactNode;
}

interface CalendarTableBodyComponentsProps {}

const CalendarTableBodyContentContext =
  createContext<CalendarTableBodyContentContextValue | null>(null);

const useCalendarContent = () => {
  const context = useContext(CalendarTableBodyContentContext);
  if (!context) {
    throw new Error(
      "useCalendarContent must be used within a CalendarTableBodyContent"
    );
  }
  return context;
};

const CalendarTableBodyContents = ({ children }: PropsWithChildren) => {
  const [fallback, setFallback] = useState<React.ReactNode | null>(null);
  const [content, setContent] = useState<React.ReactNode | null>(null);

  // controlled context.
  return (
    <CalendarTableBodyContentContext.Provider
      value={{ fallback, setFallback, content, setContent }}
    >
      {children}
    </CalendarTableBodyContentContext.Provider>
  );
}; // alias.

function CalendarTableBodyContentSource({ children }: PropsWithChildren) {
  const { setContent } = useCalendarContent();

  useEffect(() => {
    setContent(children);
  }, [children]);
  return null; // pragmatic component.
}

function CalendarTableBodyContentFallback({ children }: PropsWithChildren) {
  const { setFallback } = useCalendarContent();

  useEffect(() => {
    setFallback(children);
  }, [children]);
  return null; // pragmatic component.
}

function CalendarTableBodyContent() {
  const { content, fallback } = useCalendarContent();
  const { initializing } = useCalendarState();

  return initializing ? (fallback ?? null) : (content ?? null); // if no content on both, render nothing.
}

export {
  CalendarTableBodyContents,
  CalendarTableBodyContent,
  CalendarTableBodyContentSource,
  CalendarTableBodyContentFallback,
};
