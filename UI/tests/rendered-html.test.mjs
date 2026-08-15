import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost/", {
      headers: { accept: "text/html" },
    }),
    {
      ASSETS: {
        fetch: async () => new Response("Not found", { status: 404 }),
      },
    },
    {
      waitUntil() {},
      passThroughOnException() {},
    },
  );
}

test("server-renders the BSRS review surface", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /隱形溫度計/);
  assert.match(html, /醫病對話 BSRS 輔助評估/);
  assert.match(html, /核心評估/);
  assert.match(html, /上傳音檔/);
  assert.match(html, /待上傳/);
  assert.doesNotMatch(html, /從聲音分析|載入 JSON|最新結果/);
  assert.doesNotMatch(html, /Your site is taking shape|Building your site/);
});

test("keeps the browser UI connected to the local voice pipeline endpoint", async () => {
  const page = await readFile(new URL("../app/page.tsx", import.meta.url), "utf8");

  assert.match(page, /DEFAULT_PIPELINE_API_URL = "http:\/\/127\.0\.0\.1:8765"/);
  assert.match(page, /\/api\/analyze-audio/);
  assert.match(page, /\/api\/latest-result/);
  assert.match(page, /FormData/);
  assert.match(page, /void analyzeSelectedAudio\(file\)/);
  assert.match(page, /accept="audio\/\*,\.wav,\.mp3,\.m4a,\.flac,\.ogg,\.webm"/);
  assert.match(page, /unwrapAssessmentDocument/);
});
