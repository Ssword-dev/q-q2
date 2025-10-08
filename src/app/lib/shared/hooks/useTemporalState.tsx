import e from "express";
import { Dispatch, useCallback, useEffect, useState } from "react";

type SetTemporalStateActionCallback<S> = (prev: S) => S;
type SetTemporalStateAction<S> = S | SetTemporalStateActionCallback<S>;

/**
 * # useTemporalState
 *
 * ## How to use
 *
 * ```tsx
 * function App(){
 *  const [myTempState, setMyTempState] = useTemporalState<MyStateShape>({count: 1});
 *
 *  // get the value of the temporal state.
 *  return <div onClick={()=>setMyTempState(({count}) => {count: count + 1})}>Click me. preferably in 10 different tabs. you have clicked me {myTempState.count} times!</div>
 * }
 * ```
 * @param initial Initial value.
 * @param key the key for the state.
 * @returns A temporal state and it's dispatch.
 */
function useTemporalState<T>(
  initial: T,
  key: string
): [T, Dispatch<SetTemporalStateAction<T>>] {
  const [value, _setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);

    if (stored) {
      try {
        return JSON.parse(stored);
      } catch (err) {
        return initial;
      }
    }

    return initial;
  });

  const sync = useCallback(() => {
    _setValue(JSON.parse(localStorage.getItem(key)!));
  }, [key]);

  const setValue = useCallback(
    (value: SetTemporalStateAction<T>) => {
      _setValue(prev => {
        const newValue =
          typeof value === "function"
            ? (value as SetTemporalStateActionCallback<T>)(prev)
            : value;
        localStorage.setItem(key, JSON.stringify(newValue));
        return newValue;
      });
    },
    [key]
  );

  useEffect(() => {
    // write to storage if key not yet exist.
    const stored = localStorage.getItem(key);

    if (!stored) {
      localStorage.setItem(key, JSON.stringify(value));
    } else {
      try {
        JSON.parse(stored);
      } catch (err) {
        console.error(err);
        localStorage.setItem(key, JSON.stringify(value)); // if the client edited it to be invalid. use initial value.
      }
    }

    // listen to further changes.
    const controller = new AbortController();
    const { signal } = controller;

    window.addEventListener(
      "storage",
      ev => {
        if (ev.storageArea === localStorage && ev.key === key) {
          sync();
        }
      },
      {
        signal,
      }
    );

    return () => controller.abort();
  }, [key]);

  return [value, setValue];
}

export { useTemporalState };
