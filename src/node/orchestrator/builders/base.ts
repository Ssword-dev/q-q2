import { AppBase } from "../types";

/**
 * The Builder base class, provides common methods for all
 * builder subclasses.
 */
class Builder<O extends AppBase> {
  owner: O | null;

  constructor(owner: O) {
    this.owner = owner;
  }

  /**
   * Finalizes the builder and returns the owner.
   */
  finalize() {
    const owner = this.owner;
    this.owner = null;
    return owner!;
  }
}

export default Builder;
