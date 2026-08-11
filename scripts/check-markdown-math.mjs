#!/usr/bin/env node
// 防复发检查：
// 1) 渲染型 Markdown 禁止使用 \operatorname / \DeclareMathOperator（GitHub 数学渲染不支持，会显示红框）
// 2) Markdown 表格行内禁止出现 $...$ 数学分隔符（混用多段会导致符号按原始字符显示）
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const SKIP_DIRS = new Set([".git", "node_modules", "test-results", "playwright-report"]);

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (SKIP_DIRS.has(name) || name.startsWith(".")) continue;
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else if (name.endsWith(".md") || name.endsWith(".markdown")) out.push(p);
  }
  return out;
}

function isTableRow(line) {
  const s = line.trim();
  return s.startsWith("|") && s.split("|").length - 1 >= 2;
}

let violations = 0;
for (const file of walk(ROOT)) {
  const rel = file.slice(ROOT.length);
  const lines = readFileSync(file, "utf8").split("\n");
  let inCode = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const t = line.trim();
    if (t.startsWith("```") || t.startsWith("~~~")) {
      inCode = !inCode;
      continue;
    }
    if (inCode) continue;
    if (isTableRow(line) && line.includes("$")) {
      console.error(`${rel}:${i + 1}: 表格行不得使用 $...$ 数学分隔符`);
      violations++;
    }
    if (/\\operatorname|\\DeclareMathOperator/.test(line)) {
      console.error(`${rel}:${i + 1}: 不支持 \\operatorname 等命令，请改用 \\mathrm 或 Unicode`);
      violations++;
    }
  }
}
if (violations) {
  console.error(`\nMarkdown 数学渲染检查失败：${violations} 处违规`);
  process.exit(1);
}
console.log("Markdown 数学渲染检查通过：无 \\operatorname，表格内无数学分隔符");
