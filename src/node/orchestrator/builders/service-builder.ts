import Service from "../service";
import { AppBase } from "../types";
import Builder from "./base";

/**
 * # ServiceBuilder
 *
 * A ServiceBuilder is a description of a ***Service***.
 *
 * ## Purpose
 *
 * The purpose of a WatcherBuilder is to provide a fluent API to configure
 * individual ***services**.
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
 * The service will be **terminated** at the **disposal** of the ***owner application.***
 */
class ServiceBuilder<O extends AppBase> extends Builder<O> {
  _service: string;

  constructor(owner: O, service: string) {
    super(owner);
    this._service = service;
  }

  finalize() {
    const owner = this.owner!;
    owner.enterCritical(async () => {
      const service = new Service(this._service);
      owner._services.push(service);
      await service.start();
    });
    return super.finalize();
  }
}

export default ServiceBuilder;
