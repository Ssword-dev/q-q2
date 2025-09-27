import "../tailwind.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { CalendarPage } from ".";

createRoot(document.body).render(
  <StrictMode>
    <CalendarPage />
  </StrictMode>
);
