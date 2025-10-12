# q-q2

## Libraries / Frameworks

### App Level

- ReactJS (A library, not a framework!)
- Radix UI (provides headless components, pure logic.)
- Framer Motion (libraries for stunning animations.)
- Three JS (maybe used for animations. if i have enough time.)
- React Three (same as Three JS but can use jsx instead of bare three js primitives.)

### Server

- ExpressJS (A framework, not a library!)
- A bunch of utilities for ExpressJS.

### Build and Development

- Vite
- TailwindCSS

## Dependancies and Runtime.

- A browser that is not old. (no IE.)
- NodeJS (runtime, local when using production)
- PHP (runtime / interpreter, local when using production)

## Documentation

- [The React Docs](https://react.dev/reference/react).

- [ExpressJS Framework Documentation](https://expressjs.com/).

- [Vite Tooling Framework](https://vite.dev/guide/).

## Orchestrator Meta-Framework

Custom orchestrator meta-framework that organizes the app into steps and modules.

The orchestrator meta-framework allows for expressive app building, connecting tooling together, and setting
up the application's lifecycle.

### One Entry Point

The custom orchestrator meta-framework allows for better orchestrator of multiple programs, **_all processes invoked in one single script._**.

### Modular Nature

The custom orchestrator meta-framework encourages the use of _modular_ and _systematic_ approach. functions can be used to apply features in different apps of the app.

### Documentation

The documentation is on the code itself. as part of the JSDoc convention.

Additional Docs will follow.

## Modular and Systematic Programming Approach.

This app is composed of _systems_ and _components_ for scalability, and readability.

This app could have _a single 1000 line javascript file_ but such methods are less scalable than
a systematic approach.

## How To Run This App

This app is composed of a javascript build and a php api source. running this in a stack like **WampServer** will **not** work. Is Instead, use `yarn dev` or `yarn start`. prefer `yarn dev` since `yarn start` is experimental due to more setup required.
