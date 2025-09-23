import { useEffect, useState } from "react";

function useViewport() {
  const [viewport, setViewport] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const controller = new AbortController();

    window.addEventListener(
      "resize",
      () => {
        setViewport({
          width: window.innerWidth,
          height: window.innerHeight,
        });
      },
      { signal: controller.signal }
    );

    return () => controller.abort();
  }, []);

  return viewport;
}

export default useViewport;
