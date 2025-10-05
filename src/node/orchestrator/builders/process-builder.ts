import { SpawnOptions, SpawnOptionsWithoutStdio, spawn } from "child_process";
import { AppBase } from "../types";
import Builder from "./base";

/**
 * # ProcessBuilder
 *
 * A ProcessBuilder is a description of a ***Process***.
 *
 * ## Purpose
 *
 * The purpose of a ProcessBuilder is to provide a fluent API to configure
 * individual ***Process**.
 *
 * ## Finalization
 *
 * The builder must be ***finalized*** for the builder to take effect.
 *
 * Note that after finalization, the builder will dispose the reference
 * to the owner and the corresponding builder result reference is released.
 *
 * ## Termination
 *
 * The process will be **terminated** at the **disposal** of the ***owner application.***
 */
class ProcessBuilder<O extends AppBase> extends Builder<O> {
  _executable: string;
  _args: string[];
  _options: SpawnOptions;

  constructor(owner: O, executable: string, args: string[]) {
    super(owner);
    this._executable = executable;
    this._args = args;
    this._options = {};
  }

  addOption<O extends keyof SpawnOptionsWithoutStdio>(
    opt: O,
    value: SpawnOptionsWithoutStdio[O]
  ) {
    this._options[opt] = value;
    return this;
  }

  finalize() {
    this.owner?._sub_processes.push(
      spawn(this._executable, this._args, this._options)
    );

    return super.finalize();
  }
}

export default ProcessBuilder;
