import { spawn } from "node:child_process";
import EventEmitter from "node:events";

class Service extends EventEmitter {
  exited: boolean;
  killed: boolean;
  name: string;

  constructor(name: string) {
    super();
    this.exited = false;
    this.killed = false;
    this.name = name;
  }

  get finished() {
    return this.exited || this.killed;
  }

  private async runScCommand(args: string[]): Promise<string> {
    return new Promise((resolve, reject) => {
      let output = "";
      const proc = spawn("sc", args, { windowsHide: true });

      proc.stdout.on("data", (data) => {
        output += data.toString();
      });

      proc.stderr.on("data", (data) => {
        output += data.toString();
      });

      proc.on("exit", (code) => {
        this.exited = true;
        if (code === 0) {
          resolve(output);
        } else {
          reject(new Error(output.trim() || `sc ${args.join(" ")} failed`));
        }
      });

      proc.on("error", (err) => {
        this.killed = true;
        reject(err);
      });
    });
  }

  private async query(): Promise<"STOPPED" | "RUNNING" | "OTHER"> {
    const result = await this.runScCommand(["query", this.name]);
    if (/STATE\s*:\s*\d+\s+RUNNING/i.test(result)) {
      return "RUNNING";
    }
    if (/STATE\s*:\s*\d+\s+STOPPED/i.test(result)) {
      return "STOPPED";
    }
    return "OTHER";
  }

  async start(): Promise<void> {
    await this.runScCommand(["start", this.name]);
    const state = await this.query();
    if (state !== "RUNNING") {
      throw new Error(`Service ${this.name} failed to start (state=${state}).`);
    }
  }

  async stop(): Promise<void> {
    await this.runScCommand(["STOP", this.name]);
    const state = await this.query();
    if (state !== "STOPPED") {
      throw new Error(`Service ${this.name} failed to stop (state=${state}).`);
    }
  }

  async dispose(): Promise<void> {
    console.log(`Disposing service ${this.name}...`);
    await this.stop().catch((err) =>
      console.error(`Dispose failed: ${err.message}`)
    );
  }
}

export { Service };
