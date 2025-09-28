interface Method<T, P extends unknown[], R> {
  (this: T, ...args: P): R;
}

interface GenericMethod extends Method<unknown, unknown[], unknown> {}

type InferThis<M extends GenericMethod> =
  M extends Method<infer T, unknown[], unknown> ? T : never;
type InferParameters<M extends GenericMethod> =
  M extends Method<unknown, infer P, unknown> ? P : never;
type InferReturn<M extends GenericMethod> =
  M extends Method<unknown, unknown[], infer R> ? R : never;

declare const UNSPECIFIED_TYPE_PARAMETER: unique symbol;

type Defaulted<T = typeof UNSPECIFIED_TYPE_PARAMETER> =
  | T
  | typeof UNSPECIFIED_TYPE_PARAMETER;
type InferDefaulted<T, D> = T extends typeof UNSPECIFIED_TYPE_PARAMETER ? D : T;

interface ForwardMethod<
  F extends (this: unknown, ...args: any) => unknown,
  T extends Defaulted<unknown> = typeof UNSPECIFIED_TYPE_PARAMETER,
  P extends Defaulted<unknown[]> = typeof UNSPECIFIED_TYPE_PARAMETER,
  R extends Defaulted<unknown> = typeof UNSPECIFIED_TYPE_PARAMETER,
> extends Method<
    InferDefaulted<T, InferThis<F>>,
    InferDefaulted<P, InferParameters<F>>,
    InferDefaulted<R, InferReturn<F>>
  > {}

export { UNSPECIFIED_TYPE_PARAMETER };
export type { ForwardMethod, GenericMethod };
