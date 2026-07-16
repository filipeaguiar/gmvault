import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import test from "node:test";

function createWindowMock() {
  const listeners = new Map();
  return {
    addEventListener(type, listener) {
      if (!listeners.has(type)) listeners.set(type, new Set());
      listeners.get(type).add(listener);
    },
    removeEventListener(type, listener) {
      listeners.get(type)?.delete(listener);
    },
    dispatchMessage(event) {
      for (const listener of [...(listeners.get("message") || [])]) listener(event);
    },
    listenerCount(type) {
      return listeners.get(type)?.size || 0;
    },
  };
}

function createOBRMock() {
  const listeners = new Map();
  const sent = [];
  return {
    broadcast: {
      async sendMessage(channel, data, options) {
        sent.push({ channel, data, options });
        for (const listener of [...(listeners.get(channel) || [])]) {
          listener({ data, connectionId: "local" });
        }
      },
      onMessage(channel, listener) {
        if (!listeners.has(channel)) listeners.set(channel, new Set());
        listeners.get(channel).add(listener);
        return () => listeners.get(channel)?.delete(listener);
      },
    },
    deliver(channel, data) {
      for (const listener of [...(listeners.get(channel) || [])]) {
        listener({ data, connectionId: "dice-plus" });
      }
    },
    sent,
    listenerCount(channel) {
      return listeners.get(channel)?.size || 0;
    },
  };
}

function createIframe(origin = "https://filipeaguiar.github.io") {
  const messages = [];
  return {
    src: `${origin}/gmvault/campaigns/example/characters/hero/`,
    contentWindow: {
      postMessage(data, targetOrigin) {
        messages.push({ data, targetOrigin });
      },
    },
    messages,
  };
}

const temporaryDirectory = await mkdtemp(path.join(os.tmpdir(), "gmvault-dice-test-"));
const protocolSource = await readFile(
  new URL("../static/owlbear-character-sheet/protocol.js", import.meta.url),
  "utf8",
);
const bridgeSource = (
  await readFile(new URL("../static/owlbear-character-sheet/bridge.js", import.meta.url), "utf8")
).replace('from "./protocol.js"', 'from "./protocol.mjs"');
await writeFile(path.join(temporaryDirectory, "protocol.mjs"), protocolSource);
await writeFile(path.join(temporaryDirectory, "bridge.mjs"), bridgeSource);

const windowMock = createWindowMock();
globalThis.window = windowMock;
const protocol = await import(pathToFileURL(path.join(temporaryDirectory, "protocol.mjs")));
const bridge = await import(pathToFileURL(path.join(temporaryDirectory, "bridge.mjs")));

const {
  SOURCE,
  MessageType,
  DicePlusChannel,
  createEnvelope,
} = protocol;
const {
  initBridge,
  bindIframe,
  destroyBridge,
  isDiceReady,
} = bridge;

test.after(async () => {
  destroyBridge();
  delete globalThis.window;
  await rm(temporaryDirectory, { recursive: true, force: true });
});

test("readiness uses Owlbear event.data and ignores the request echo", async () => {
  const obr = createOBRMock();
  const iframe = createIframe();
  initBridge(obr, { id: "player-1", name: "Pinky" });
  bindIframe(iframe);

  const request = obr.sent.find((entry) => entry.channel === DicePlusChannel.IS_READY);
  assert.ok(request);
  assert.deepEqual(request.options, { destination: "ALL" });
  assert.equal(isDiceReady(), false, "echo without ready:true must be ignored");

  obr.deliver(DicePlusChannel.IS_READY, {
    requestId: request.data.requestId,
    ready: true,
    timestamp: Date.now(),
  });

  assert.equal(isDiceReady(), true);
  assert.equal(obr.listenerCount(DicePlusChannel.IS_READY), 0);
  const readyMessage = iframe.messages.find((entry) => entry.data.type === MessageType.DICE_READY);
  assert.equal(readyMessage.data.payload.ready, true);
  destroyBridge();
});

test("roll request matches the documented Dice+ payload and result shape", async () => {
  const obr = createOBRMock();
  const iframe = createIframe();
  initBridge(obr, { id: "player-2", name: "Ana" });
  bindIframe(iframe);

  const readyRequest = obr.sent.find((entry) => entry.channel === DicePlusChannel.IS_READY);
  obr.deliver(DicePlusChannel.IS_READY, {
    requestId: readyRequest.data.requestId,
    ready: true,
  });
  iframe.messages.length = 0;

  windowMock.dispatchMessage({
    source: iframe.contentWindow,
    origin: "https://filipeaguiar.github.io",
    data: createEnvelope(MessageType.ROLL_REQUEST, {
      requestId: "sheet-request-1",
      notation: "1d20+7",
      label: "Acrobacia",
    }),
  });

  const rollRequest = obr.sent.find((entry) => entry.channel === DicePlusChannel.ROLL_REQUEST);
  assert.ok(rollRequest);
  assert.equal(rollRequest.data.source, SOURCE);
  assert.equal(rollRequest.data.playerId, "player-2");
  assert.equal(rollRequest.data.playerName, "Ana");
  assert.equal(rollRequest.data.rollTarget, "everyone");
  assert.equal(rollRequest.data.diceNotation, "1d20+7");
  assert.equal(rollRequest.data.showResults, true);
  assert.deepEqual(rollRequest.options, { destination: "ALL" });
  assert.equal("notation" in rollRequest.data, false);

  obr.deliver(DicePlusChannel.ROLL_RESULT, {
    rollId: rollRequest.data.rollId,
    playerId: "player-2",
    playerName: "Ana",
    rollTarget: "everyone",
    timestamp: Date.now(),
    result: {
      rollId: rollRequest.data.rollId,
      diceNotation: "1d20+7",
      totalValue: 19,
      rollSummary: "12 + 7 = 19",
      groups: [{ diceType: "d20", total: 12, dice: [] }],
    },
  });

  const result = iframe.messages.find((entry) => entry.data.type === MessageType.ROLL_RESULT);
  assert.ok(result);
  assert.equal(result.data.payload.requestId, "sheet-request-1");
  assert.equal(result.data.payload.total, 19);
  assert.equal(result.data.payload.summary, "12 + 7 = 19");
  assert.equal(result.data.payload.groups.length, 1);
  destroyBridge();
});

test("Dice+ errors are correlated and cleanup removes listeners", async () => {
  const obr = createOBRMock();
  const iframe = createIframe();
  initBridge(obr, { id: "player-3", name: "Beto" });
  bindIframe(iframe);

  const readyRequest = obr.sent.find((entry) => entry.channel === DicePlusChannel.IS_READY);
  obr.deliver(DicePlusChannel.IS_READY, {
    requestId: readyRequest.data.requestId,
    ready: true,
  });
  iframe.messages.length = 0;

  windowMock.dispatchMessage({
    source: iframe.contentWindow,
    origin: "https://filipeaguiar.github.io",
    data: createEnvelope(MessageType.ROLL_REQUEST, {
      requestId: "sheet-request-error",
      notation: "2d6+3",
      label: "Dano",
    }),
  });
  const rollRequest = obr.sent.find((entry) => entry.channel === DicePlusChannel.ROLL_REQUEST);

  obr.deliver(DicePlusChannel.ROLL_ERROR, {
    rollId: rollRequest.data.rollId,
    notation: "2d6+3",
    error: "Invalid dice model",
  });

  const error = iframe.messages.find((entry) => entry.data.type === MessageType.ROLL_ERROR);
  assert.ok(error);
  assert.equal(error.data.payload.requestId, "sheet-request-error");
  assert.equal(error.data.payload.error, "Invalid dice model");

  destroyBridge();
  assert.equal(windowMock.listenerCount("message"), 0);
  assert.equal(obr.listenerCount(DicePlusChannel.ROLL_RESULT), 0);
  assert.equal(obr.listenerCount(DicePlusChannel.ROLL_ERROR), 0);
});
