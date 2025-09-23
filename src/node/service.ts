import { spawn } from "node:child_process";
import EventEmitter from "node:events";

const MAX_START_PENDING_RETRIES = 100;

function yieldToEventLoop(ms: number): Promise<void> {
  return new Promise<void>((res) => setTimeout(() => res(), ms));
}

async function runCommand(cmd: string, args: string[]): Promise<string> {
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
      if (code === 0) {
        resolve(output);
      } else {
        reject(new Error(output.trim() || `${cmd} ${args.join(" ")} failed`));
      }
    });

    proc.on("error", (err) => {
      reject(err);
    });
  });
}
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

  private async runNetCommand(args: string[]) {
    return await runCommand("net", args);
  }

  private async query(): Promise<string | null> {
    const result = await this.runScCommand(["query", this.name]);
    const match = /STATE\s*:\s*\d+\s+([a-zA-Z_]+)/i.exec(result);

    if (!match) {
      return null;
    }

    return match[1];
  }

  async start(): Promise<void> {
    const query = await this.query();

    if (["START_PENDING", "RUNNING"].includes(query!)) {
      return; // already started.
    }

    await this.runScCommand(["start", this.name]);
    let pendingCount = 0;

    while (true) {
      const state = await this.query();
      if (state === "START_PENDING") {
        pendingCount++;

        if (pendingCount >= MAX_START_PENDING_RETRIES) {
          console.error(`Starting service '${this.name}' took too long.`);
          break;
        }

        await yieldToEventLoop(30);
        continue;
      }

      if (state === "RUNNING") {
        break;
      }

      throw new Error(`Service ${this.name} failed to start (state=${state}).`);
    }
  }

  async stop(): Promise<void> {
    await this.runScCommand(["stop", this.name]);
    const state = await this.query();

    if (state !== "STOPPED") {
      await this.runNetCommand(["stop", this.name]);
      const newState = await this.query();

      if (newState !== null || newState!.trim() === "") {
        throw new Error(
          `Failed to stop ${this.name} with both 'sc' and 'net'. (state=${newState})`
        );
      }
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
