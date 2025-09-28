import React, { PropsWithChildren } from "react";

interface ErrorData {
  error: Error;
  info: React.ErrorInfo;
}

interface ErrorBoundaryProps extends PropsWithChildren<{}> {
  fallback: React.FC<ErrorData>;
}

interface ErrorBoundaryState {
  errorData: ErrorData | null;
}

class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      errorData: null,
    };
  }

  render() {
    const Fallback = this.props.fallback;

    if (this.state.errorData) {
      return <Fallback {...this.state.errorData} />;
    }

    return this.props.children;
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    this.setState(prev => {
      if (prev.errorData) {
        console.error("Caught another error whilst displaying current error.");
        return prev;
      }

      return {
        errorData: {
          error,
          info: errorInfo,
        },
      };
    });
  }
}

export default ErrorBoundary;
export type { ErrorData, ErrorBoundaryState };
