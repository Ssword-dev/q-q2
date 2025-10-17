import { Button } from "@/app/lib/dom/components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/app/lib/dom/components/ui/card";
import { ErrorData } from "@/app/lib/dom/utils/error-boundary";
import { useCallback } from "react";

function ErrorBoundaryFallback({ error, info }: ErrorData) {
  const reload = useCallback(() => {
    window.location.reload();
  }, []);
  return (
    <div className="flex h-screen w-screen items-center justify-center bg-background">
      <Card className="w-4/5 max-w-4xl h-4/5 overflow-hidden shadow-lg border border-destructive-foreground/30">
        <CardHeader className="border-b border-border p-4 bg-destructive/10">
          <CardTitle className="flex flex-row text-xl font-bold text-destructive-foreground">
            <div className="text-destructive-foreground text-xl font-bold">
              Application Error
            </div>
            <CardAction className="ml-auto">
              <Button
                variant="ghost"
                className="bg-transparent"
                onClick={reload}
              >
                Reload
              </Button>
            </CardAction>
          </CardTitle>
        </CardHeader>

        <CardContent className="flex flex-col gap-4 overflow-y-auto p-6">
          {/* Error message */}
          <div className="space-y-2">
            <h2 className="text-lg font-semibold text-destructive-foreground">
              Error:
            </h2>
            <pre className="rounded-md bg-destructive/10 p-3 text-sm text-destructive-foreground whitespace-pre-wrap">
              {error.message}
            </pre>
          </div>

          {/* Stack trace */}
          {error.stack && (
            <div className="space-y-2">
              <h2 className="text-lg font-semibold text-foreground">
                Stack Trace:
              </h2>
              <pre className="rounded-md bg-muted p-3 text-xs text-muted-foreground overflow-x-auto">
                {error.stack}
              </pre>
            </div>
          )}

          {/* Component trace */}
          {info?.componentStack && (
            <div className="space-y-2">
              <h2 className="text-lg font-semibold text-foreground">
                Component Trace:
              </h2>
              <pre className="rounded-md bg-muted p-3 text-xs text-muted-foreground overflow-x-auto">
                {info.componentStack}
              </pre>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default ErrorBoundaryFallback;
