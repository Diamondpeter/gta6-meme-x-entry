// Entry program for make.fun's gta6-meme-x-01 bounty (Node 22, standard library only).
//
// The entry itself is a post on X: a GTA 6 meme whose picture carries make.fun's ghost,
// posted publicly with the bounty link and a play code in its text. This repository hands
// in the post's address: POST.json at the repository root names it, and all this program
// does is copy POST.json to /output/POST.json, where the gate reads it.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for
// /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// Two runs write the same bytes: the copy is byte for byte.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
