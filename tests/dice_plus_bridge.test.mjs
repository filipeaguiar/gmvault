import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

async function importSource(path) {
  const source = await readFile(path, "utf8");
  return import(`data:text/javascript;base64,${Buffer.from(source).toString("base64")}`);
}

function eventTarget() {
  const listeners = new Map();
  return {
    addEventListener(type, callback) {
      listeners.set(type, callback);
    },
    removeEventListener(type) {
      listeners.delete(type);
    },
    dispatch(type, event) {
      listeners.get(type)?.(event);
    },
    hasListener(type) {
      return listeners.has(type);
    },
  };
}

const bridgePath = new URL("../assets/js/dice-plus-bridge.js", import.meta.url);
const hostPath = new URL("../assets/js/dice-plus-host.js", import.meta.url);

await test("iframe client sends a validated request and receives its result", async () => {
  const { createDicePlusClient } = await importSource(bridgePath);
  const iframe = eventTarget();
  iframe.location = { origin: "https://filipeaguiar.github.io" };
  iframe.document = { referrer: "https://owlbear-gm-vault.netlify.app/index.html" };
  const parent = { posted: [], postMessage(message, targetOrigin) { this.posted.push({ message, targetOrigin }); } };
  const client = createDicePlusClient({
    windowRef: iframe,
    parentWindow: parent,
    targetOrigin: "https://owlbear-gm-vault.netlify.app",
  });

  const resultPromise = client.requestRoll({ diceNotation: "1d20+5", label: "Ataque" });
  assert.equal(parent.posted.length, 1);
  const sent = parent.posted[0];
  assert.equal(sent.targetOrigin, "https://owlbear-gm-vault.netlify.app");
  assert.equal(sent.message.channel, "gm-vault/dice");
  assert.equal(sent.message.type, "roll-request");
  assert.equal(sent.message.request.diceNotation, "1d20+5");

  iframe.dispatch("message", {
    source: parent,
    origin: "https://owlbear-gm-vault.netlify.app",
    data: {
      channel: "gm-vault/dice",
      version: 1,
      type: "roll-result",
      requestId: sent.message.requestId,
      rollId: sent.message.rollId,
      result: { totalValue: 18, rollSummary: "1d20+5 = 18" },
    },
  });

  const result = await resultPromise;
  assert.equal(result.result.totalValue, 18);
  client.destroy();
  assert.equal(iframe.hasListener("message"), false);
});

test("iframe client ignores an untrusted origin", async () => {
  const { createDicePlusClient } = await importSource(bridgePath);
  const iframe = eventTarget();
  iframe.location = { origin: "https://filipeaguiar.github.io" };
  const parent = { posted: [], postMessage(message, targetOrigin) { this.posted.push({ message, targetOrigin }); } };
  const client = createDicePlusClient({ windowRef: iframe, parentWindow: parent, targetOrigin: "https://owlbear-gm-vault.netlify.app", timeoutMs: 20 });
  const resultPromise = client.requestRoll({ diceNotation: "1d20" });
  const sent = parent.posted[0].message;
  iframe.dispatch("message", {
    source: parent,
    origin: "https://untrusted.example",
    data: { channel: "gm-vault/dice", version: 1, type: "roll-result", requestId: sent.requestId, rollId: sent.rollId, result: { totalValue: 1 } },
  });
  await assert.rejects(resultPromise, /não respondeu/);
  client.destroy();
});

test("iframe client rejects invalid notation and degrades without a parent", async () => {
  const { createDicePlusClient } = await importSource(bridgePath);
  const topLevel = eventTarget();
  topLevel.location = { origin: "https://filipeaguiar.github.io" };
  const client = createDicePlusClient({ windowRef: topLevel, parentWindow: topLevel });
  assert.equal(client.available, false);
  await assert.rejects(client.requestRoll({ diceNotation: "<script>" }), /notação/);
  client.destroy();
});

test("iframe client can fall back to wildcard targetOrigin", async () => {
  const { createDicePlusClient } = await importSource(bridgePath);
  const iframe = eventTarget();
  iframe.location = { origin: "https://filipeaguiar.github.io" };
  iframe.document = { referrer: "" };
  const parent = { posted: [], postMessage(message, targetOrigin) { this.posted.push({ message, targetOrigin }); } };
  const client = createDicePlusClient({ windowRef: iframe, parentWindow: parent, targetOrigin: "*" });
  assert.equal(client.available, true);
  const rollPromise = client.requestRoll({ diceNotation: "1d20" });
  const sent = parent.posted[0];
  assert.equal(sent.targetOrigin, "*");
  iframe.dispatch("message", {
    source: parent,
    origin: "https://owlbear-gm-vault.netlify.app",
    data: {
      channel: "gm-vault/dice",
      version: 1,
      type: "roll-result",
      requestId: sent.message.requestId,
      rollId: sent.message.rollId,
      result: { totalValue: 12 },
    },
  });
  const result = await rollPromise;
  assert.equal(result.result.totalValue, 12);
  client.destroy();
});

test("multiple iframe rolls remain correlated", async () => {
  const { createDicePlusClient } = await importSource(bridgePath);
  const iframe = eventTarget();
  iframe.location = { origin: "https://filipeaguiar.github.io" };
  const parent = { posted: [], postMessage(message, targetOrigin) { this.posted.push({ message, targetOrigin }); } };
  const client = createDicePlusClient({ windowRef: iframe, parentWindow: parent, targetOrigin: "https://owlbear-gm-vault.netlify.app" });
  const first = client.requestRoll({ diceNotation: "1d20+1" });
  const second = client.requestRoll({ diceNotation: "2d6" });
  const firstRequest = parent.posted[0].message;
  const secondRequest = parent.posted[1].message;
  iframe.dispatch("message", {
    source: parent,
    origin: "https://owlbear-gm-vault.netlify.app",
    data: { channel: "gm-vault/dice", version: 1, type: "roll-result", requestId: secondRequest.requestId, rollId: secondRequest.rollId, result: { totalValue: 9 } },
  });
  iframe.dispatch("message", {
    source: parent,
    origin: "https://owlbear-gm-vault.netlify.app",
    data: { channel: "gm-vault/dice", version: 1, type: "roll-result", requestId: firstRequest.requestId, rollId: firstRequest.rollId, result: { totalValue: 17 } },
  });
  assert.equal((await first).result.totalValue, 17);
  assert.equal((await second).result.totalValue, 9);
  client.destroy();
});

test("host forwards readiness and correlates Dice+ results", async () => {
  const { createDicePlusHost } = await importSource(hostPath);
  const hostWindow = eventTarget();
  const iframeWindow = { posted: [], postMessage(message, targetOrigin) { this.posted.push({ message, targetOrigin }); } };
  const broadcastListeners = new Map();
  const sentMessages = [];
  const OBR = {
    broadcast: {
      onMessage(channel, callback) {
        broadcastListeners.set(channel, callback);
        return () => broadcastListeners.delete(channel);
      },
      async sendMessage(channel, data, options) {
        sentMessages.push({ channel, data, options });
      },
    },
    player: {
      async getId() { return "player-1"; },
      async getName() { return "Pinky"; },
    },
  };
  const host = createDicePlusHost({ OBR, hostWindow, iframeWindow, iframeOrigin: "https://filipeaguiar.github.io" });
  host.start();

  hostWindow.dispatch("message", {
    source: iframeWindow,
    origin: "https://filipeaguiar.github.io",
    data: { channel: "gm-vault/dice", version: 1, type: "availability-request", requestId: "ready-1" },
  });
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(sentMessages[0].channel, "dice-plus/isReady");
  await broadcastListeners.get("dice-plus/isReady")({ data: { requestId: sentMessages[0].data.requestId, ready: true } });
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(iframeWindow.posted.at(-1).message.ready, true);

  hostWindow.dispatch("message", {
    source: iframeWindow,
    origin: "https://filipeaguiar.github.io",
    data: {
      channel: "gm-vault/dice",
      version: 1,
      type: "roll-request",
      requestId: "request-1",
      request: { diceNotation: "1d20+5", rollTarget: "everyone", showResults: true },
    },
  });
  await new Promise((resolve) => setImmediate(resolve));
  const readyMessage = sentMessages.at(-1);
  await broadcastListeners.get("dice-plus/isReady")({ data: { requestId: readyMessage.data.requestId, ready: true } });
  await new Promise((resolve) => setImmediate(resolve));
  const rollMessage = sentMessages.at(-1);
  assert.equal(rollMessage.channel, "dice-plus/roll-request");
  assert.equal(rollMessage.data.source, "gm-vault");
  assert.equal(rollMessage.data.playerId, "player-1");
  assert.equal(rollMessage.data.diceNotation, "1d20+5");

  await broadcastListeners.get("gm-vault/roll-result")({ data: { rollId: rollMessage.data.rollId, result: { totalValue: 18 } } });
  assert.equal(iframeWindow.posted.at(-1).message.type, "roll-result");
  assert.equal(iframeWindow.posted.at(-1).message.result.totalValue, 18);
  host.destroy();
  assert.equal(hostWindow.hasListener("message"), false);
});
