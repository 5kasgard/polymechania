// Local checks of the door, with the network and Workers AI faked.
import door from "./worker.js";
import assert from "node:assert/strict";

let forwarded = null;
globalThis.fetch = async (url, init) => { forwarded = { url, init }; return new Response('{"ok":1}', { status: 200 }); };
const env = { DOOR_TOKEN: "t0k", ANTHROPIC_API_KEY: "sk-secret", AI: { run: async (m, i) => ({ response: "PASS", model: m, input: i }) } };
const call = (path, body, token = "t0k", method = "POST") =>
  door.fetch(new Request("https://d/" + path, { method, headers: token ? { "x-door-token": token } : {}, body: method === "POST" ? JSON.stringify(body) : undefined }), env);
const ok = { model: "claude-haiku-5-5", max_tokens: 100, messages: [{ role: "user", content: "hi" }] };

let r = await call("health", null, null, "GET"); let j = await r.json();
assert.equal(j.key_set, true); assert.ok(!JSON.stringify(j).includes("sk-secret"));
assert.equal((await call("v1/messages", ok, "wrong")).status, 401);
assert.equal((await call("v1/messages", ok, null)).status, 401);
for (const bad of [
  { ...ok, tools: [{ name: "bash" }] }, { ...ok, tool_choice: { type: "any" } }, { ...ok, model: "claude-opus-5-5" },
  { ...ok, max_tokens: 99999 }, { ...ok, stream: true }, { ...ok, mcp_servers: [] },
  { ...ok, messages: [{ role: "user", content: [{ type: "image", source: {} }] }] },
  { ...ok, messages: [{ role: "user", content: [{ type: "tool_result", content: "x" }] }] },
  { ...ok, thinking: { type: "enabled", budget_tokens: 500 } },
  { ...ok, output_config: { effort: "max" } }, { ...ok, output_config: { effort: "xhigh" } },
  { ...ok, output_config: { effort: "low", format: { type: "json_schema" } } }, { ...ok, output_config: [] },
  { ...ok, thinking: { type: "adaptive", display: "full" } }, { ...ok, thinking: { type: "turbo" } },
  { ...ok, thinking: { type: "adaptive", budget_tokens: 99999 } }, { ...ok, thinking: { type: "disabled", budget_tokens: 1 } },
  { ...ok, thinking: null }, { ...ok, thinking: [] }, { ...ok, output_config: null }, { ...ok, output_config: {} },
  { ...ok, output_config: { effort: ["low"] } }, { ...ok, output_config: { effort: "low", task_budget: 10 } },
  JSON.parse('{"model":"claude-haiku-5-5","max_tokens":100,"messages":[{"role":"user","content":"hi"}],"__proto__":{"tools":[]}}'),
  { ...ok, output_config: JSON.parse('{"effort":"low","__proto__":{"format":1}}') },
]) assert.equal((await call("v1/messages", bad)).status, 400, JSON.stringify(bad));
forwarded = null;
r = await call("v1/messages", ok); assert.equal(r.status, 200);
assert.equal(forwarded.url, "https://api.anthropic.com/v1/messages");
assert.equal(forwarded.init.headers["x-api-key"], "sk-secret");
assert.deepEqual(JSON.parse(forwarded.init.body), ok);
for (const good of [
  { ...ok, output_config: { effort: "low" } }, { ...ok, output_config: { effort: "high" } },
  { ...ok, thinking: { type: "adaptive" }, output_config: { effort: "medium" } },
  { ...ok, thinking: { type: "disabled" } }, { ...ok, thinking: { type: "between_tools" } },
  { ...ok, thinking: { type: "enabled", budget_tokens: 50 } },
]) { forwarded = null; assert.equal((await call("v1/messages", good)).status, 200, JSON.stringify(good));
     assert.deepEqual(JSON.parse(forwarded.init.body), good); }
assert.equal((await call("ai", { model: "@cf/openai/gpt-oss-20b", messages: [{ role: "user", content: "x" }] })).status, 400);
r = await call("ai", { model: "@cf/google/gemma-4-26b-a4b-it", messages: [{ role: "user", content: "x" }], max_tokens: 99999 });
j = await r.json(); assert.equal(j.input.max_tokens, 4096); assert.equal(j.input.temperature, 0);
r = await call("ai", { model: "@cf/google/gemma-4-26b-a4b-it", messages: [{ role: "user", content: "x" }] });
j = await r.json(); assert.deepEqual(j.input.chat_template_kwargs, { enable_thinking: false });
r = await call("ai", { model: "@cf/google/gemma-4-26b-a4b-it", messages: [{ role: "user", content: "x" }], default_thinking: true });
j = await r.json(); assert.equal(j.input.chat_template_kwargs, undefined); assert.equal(j.input.temperature, 0);
assert.equal((await call("ai", { model: "@cf/google/gemma-4-26b-a4b-it", messages: [{ role: "user", content: "x" }], default_thinking: "yes" })).status, 400);
for (const m of ["@cf/qwen/qwen3.8-27b", "@cf/nvidia/nemotron-3-120b-a12b", "@cf/openai/gpt-oss-120b", "@cf/meta/llama-4-scout-17b-16e-instruct", "@cf/meta/llama-3.1-8b-instruct-fp8-fast"]) {
  r = await call("ai", { model: m, messages: [{ role: "user", content: "x" }], max_tokens: 99999 });
  j = await r.json(); assert.equal(j.model, m); assert.equal(j.input.max_tokens, 4096); assert.equal(j.input.temperature, 0);
}
assert.equal((await call("ai", { model: "@cf/zai-org/glm-5.3", messages: [{ role: "user", content: "x" }] })).status, 400);
assert.equal((await call("nowhere", ok)).status, 404);
const noKey = await door.fetch(new Request("https://d/v1/messages", { method: "POST", headers: { "x-door-token": "t0k" }, body: JSON.stringify(ok) }), { ...env, ANTHROPIC_API_KEY: undefined });
assert.equal(noKey.status, 503);
console.log("door: all checks passed");
