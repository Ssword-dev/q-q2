import "../../tailwind.css";
import { StrictMode, useEffect, useRef } from "react";
import { createRoot } from "react-dom/client";

import { Button } from "@/app/lib/dom/components/ui/button";

// lucide. svg library. provides components for svg icons.
// so like. i do not have to worry about needing svg icons..
// lucide probably has the needed icon.
import { ArrowDown, ChevronDown, CogIcon, Layers, Wrench } from "lucide-react";
import { Card, CardContent, CardTitle } from "@/app/lib/dom/components/ui/card";
import { useTemporalState } from "@/app/lib/shared/hooks/useTemporalState";

function HeroSection() {
  const [{ count }, setValue] = useTemporalState<{ count: number }>(
    { count: 0 },
    "x-home-page-state"
  );
  return (
    <div className="flex flex-row h-screen w-screen" id="hero">
      {/** Split into 2 containers */}
      <div className="flex flex-col gap-6 text-center justify-center items-center h-full w-1/2 bg-background/60">
        <h1 className="text-4xl">Built for your convinience</h1>
        <div
          className="flex flex-row justify-center gap-2 w-full h-max"
          id="button-tray"
        >
          <Button asChild className="flex flex-row items-center gap-2 group">
            <a href="#">
              <Wrench className="stroke-text transition-colors duration-150 group-hover:stroke-amber-300" />
              Tools
            </a>
          </Button>

          <Button asChild className="flex flex-row items-center gap-2 group">
            <a href="#">
              <Layers className="stroke-text transition-colors duration-150 group-hover:stroke-fuchsia-300" />
              Services
            </a>
          </Button>
          <Button asChild className="flex flex-row items-center gap-2 group">
            <a
              href="#"
              onClick={() => setValue(({ count }) => ({ count: count + 1 }))}
            >
              <Layers className="stroke-text transition-colors duration-150 group-hover:stroke-fuchsia-300" />
              {count}
            </a>
          </Button>
        </div>
      </div>
      <div className="flex flex-col justify-center align-center gap-6 h-full w-1/2 bg-background/30">
        <Card className="w-4/5 h-3/5">
          <CardTitle className="text-xl">Boosted Productivity.</CardTitle>
          <CardContent className="h-4/5">
            {/* ahem. calendar page. */}
            <div className="h-full w-3/5 bg-surface/90 border-[1px] border-text rounded-xl">
              Uhh, heyy, Boss!
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function ToolsSection() {
  return (
    <div className="flex flex-row h-screen w-screen">
      {/** Split into 2 containers */}
      <div className="flex flex-col justify-center align-center gap-6 h-full w-1/2 bg-background/30">
        <ul className="bg-surface rounded-lg list-dotted h-3/5 w-4/5 px-8 py-4"></ul>
      </div>
      <div className="flex flex-col gap-6 text-center justify-center items-center h-full w-1/2 bg-background/60">
        <h1 className="text-4xl">Life made easier.</h1>
        <div
          className="flex flex-row justify-center gap-2 w-full h-max"
          id="button-tray"
        >
          <Button asChild className="flex flex-row items-center gap-2 group">
            <a href="#">
              <Wrench className="stroke-text transition-colors duration-150 group-hover:stroke-amber-300" />
              Tools
            </a>
          </Button>

          <Button asChild className="flex flex-row items-center gap-2 group">
            <a href="#">
              <Layers className="stroke-text transition-colors duration-150 group-hover:stroke-fuchsia-300" />
              Services
            </a>
          </Button>
        </div>
      </div>
    </div>
  );
}

function LandingPage() {
  return (
    <>
      <HeroSection />
    </>
  );
}
createRoot(document.body).render(
  <StrictMode>
    <LandingPage />
    <ToolsSection />
  </StrictMode>
);
