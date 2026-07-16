import { copyFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const frontendSource = resolve(root, "src", "frontend");
const frontendOutput = resolve(root, "dist", "frontend");
const staticOutput = resolve(frontendOutput, "static");

const assets = [
  {
    from: resolve(frontendSource, "index.html"),
    to: resolve(frontendOutput, "index.html")
  },
  {
    from: resolve(frontendSource, "style.css"),
    to: resolve(staticOutput, "style.css")
  },
  {
    from: resolve(frontendSource, "favicon.png"),
    to: resolve(frontendOutput, "favicon.png")
  }
];

await mkdir(staticOutput, { recursive: true });

await Promise.all(assets.map((asset) => copyFile(asset.from, asset.to)));
