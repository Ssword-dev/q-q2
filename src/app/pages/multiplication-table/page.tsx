import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import ErrorBoundary from "@/app/lib/dom/utils/error-boundary";
import ErrorBoundaryFallback from "../../error";

async function fetchMultiplicationTableData(limit: number) {
  const multiplicationTableData = await fetch(
    `/api/multiplication-table/index.php?limit=${encodeURIComponent(limit)}`
  );

  return multiplicationTableData;
}

function MultiplicationTablePage() {
  return <div className="w-full h-full">Hello world!</div>;
}

createRoot(document.body).render(
  <StrictMode>
    <ErrorBoundary fallback={ErrorBoundaryFallback}>
      <MultiplicationTablePage />
    </ErrorBoundary>
  </StrictMode>
);
