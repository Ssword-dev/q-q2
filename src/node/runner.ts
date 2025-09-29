// import path from "node:path";

import path from 'path';
import app, { App } from './app';
import os from 'node:os';

function indent(s: string, spaces: number) {
  return ' '.repeat(spaces) + s;
}

function applyRoutes(app: App) {
  function handleHolidaysRoute(){}
}

async function main() {
  const cwd = process.cwd();
  const project = path.basename(cwd);
  const viteConfig = path.resolve(cwd, './config/vite.config.ts');

  await app()
    .ifDev((app) => {
      const pythonServerPath = path.resolve(cwd, './src/python/main.py');
      app
        .addService('wampapache64')
        .finalize()
        .addService('wampmariadb64')
        .finalize()
        .addService('wampmysqld64')
        .finalize()
        .apply((_) => console.log('Spawned wampapache64'))
        .addSubprocess('python', [pythonServerPath])
        .addOption('stdio', 'inherit')
        .finalize()
        .addProxy('/api/php/', {
          target: 'http://localhost', // Listen to WAMP's apache.
          changeOrigin: true,
          pathRewrite: (p) => p.replace(/^\/(.+)/, `/${project}/public/api/$1`),
        })
        .addProxy('/api/python/', {
          target: 'http://localhost:5000', // Listen to flask server. mostly for holidays.
          changeOrigin: true,
          pathRewrite: (p) => p.replace(/^\/(.+)/, `/api/$1`),
        })
        .addVite({
          configFile: viteConfig,
        })
        .apply((_) => {
          console.log('Finished configuring app for development!');
        });
    })
    .listen(4000, '0.0.0.0')
    .apply((app) => {
      const nets = os.networkInterfaces();

      console.log('Server is available at:');

      for (const name of Object.keys(nets)) {
        for (const net of nets[name] ?? []) {
          console.log(indent(net.address, 4));
        }
      }
    })
    .bindLifecycle()
    .promise();
}

main().catch(console.error);
