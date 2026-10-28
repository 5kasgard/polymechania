// The door: the only way E1's workers and judges reach a model.
//
// Workers get text in and text out, nothing else, and this code is what
// enforces it. The Anthropic key lives here as a secret the owner sets in
// the Cloudflare dashboard; nothing that calls the door ever sees it.
//
//   POST /v1/messages   Claude, text only: allowed models, no tools, no
//                       files or images, capped tokens, no streaming.
//   POST /ai            Workers AI, for the outside reviewer and judges:
//                       allowed models only, capped tokens.
//   GET  /health        whether the door is up and the key is set (never the key).
//
// Every call needs the header x-door-token, a separate, revocable token.

const CLAUDE = new Set(["claude-haiku-5-5", "claude-sonnet-5-5"]);
const WORKERS_AI = new Set([
  "@cf/google/gemma-4-26b-a4b-it", "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
  // E-ext (prereg/eext-benchmarks.md): free text models with a public Coding Index entry
  "@cf/qwen/qwen3.8-27b", "@cf/nvidia/nemotron-3-120b-a12b", "@cf/openai/gpt-oss-120b",
  "@cf/meta/llama-4-scout-17b-16e-instruct", "@cf/meta/llama-3.1-8b-instruct-fp8-fast",
]);
const MAX_TOKENS = 4096;
const MAX_BODY = 256 * 1024;
const FIELDS = new Set(["model", "max_tokens", "system", "messages", "temperature", "stop_sequences", "thinking", "output_config"]);
// Effort levels the door passes: xhigh and max need far more than MAX_TOKENS, so they are refused.
const EFFORT = new Set(["low", "medium", "high"]);

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json", "x-door": "1" } });

function sameToken(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

function textOnly(content) {
  if (typeof content === "string") return true;
  return Array.isArray(content) && content.every((b) => b && b.type === "text" && typeof b.text === "string");
}

function checkClaude(body) {
  for (const k of Object.keys(body)) if (!FIELDS.has(k)) return `field not allowed: ${k}`;
  if (!CLAUDE.has(body.model)) return "model not allowed";
  if (!Number.isInteger(body.max_tokens) || body.max_tokens < 1 || body.max_tokens > MAX_TOKENS)
    return `max_tokens must be 1-${MAX_TOKENS}`;
  if (body.system !== undefined && !textOnly(body.system)) return "system must be text";
  if (!Array.isArray(body.messages) || body.messages.length === 0) return "messages required";
  for (const m of body.messages) {
    if (!m || !["user", "assistant"].includes(m.role) || !textOnly(m.content)) return "messages must be text only";
  }
  if (body.thinking !== undefined) {
    const t = body.thinking;
    if (!t || !["enabled", "disabled", "adaptive", "between_tools"].includes(t.type)) return "bad thinking";
    for (const k of Object.keys(t)) if (!["type", "budget_tokens"].includes(k)) return `thinking field not allowed: ${k}`;
    if (t.type !== "enabled" && "budget_tokens" in t) return "budget_tokens only with enabled";
    if (t.type === "enabled" && !(Number.isInteger(t.budget_tokens) && t.budget_tokens < body.max_tokens))
      return "thinking budget must be below max_tokens";
  }
  if (body.output_config !== undefined) {
    const o = body.output_config;
    if (!o || typeof o !== "object" || Array.isArray(o)) return "bad output_config";
    for (const k of Object.keys(o)) if (k !== "effort") return `output_config field not allowed: ${k}`;
    if (!EFFORT.has(o.effort)) return "effort must be low, medium or high";
  }
  return null;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/health") {
      return json({ ok: true, key_set: Boolean(env.ANTHROPIC_API_KEY), token_set: Boolean(env.DOOR_TOKEN) });
    }
    if (!env.DOOR_TOKEN || !sameToken(request.headers.get("x-door-token"), env.DOOR_TOKEN)) {
      return json({ error: "not allowed" }, 401);
    }
    if (request.method !== "POST") return json({ error: "POST only" }, 405);
    const raw = await request.text();
    if (raw.length > MAX_BODY) return json({ error: "body too large" }, 413);
    let body;
    try {
      body = JSON.parse(raw);
    } catch {
      return json({ error: "not JSON" }, 400);
    }

    if (url.pathname === "/v1/messages") {
      if (!env.ANTHROPIC_API_KEY) return json({ error: "key not set yet" }, 503);
      const problem = checkClaude(body);
      if (problem) return json({ error: problem }, 400);
      const r = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "x-api-key": env.ANTHROPIC_API_KEY,
          "anthropic-version": "2023-06-01",
        },
        body: JSON.stringify(body),
      });
      return new Response(r.body, { status: r.status, headers: { "content-type": "application/json", "x-door": "1" } });
    }

    if (url.pathname === "/ai") {
      if (!WORKERS_AI.has(body.model)) return json({ error: "model not allowed" }, 400);
      if (!Array.isArray(body.messages) || !body.messages.every((m) => m && typeof m.content === "string"))
        return json({ error: "messages must be text" }, 400);
      const max = Math.min(Number.isInteger(body.max_tokens) ? body.max_tokens : 512, MAX_TOKENS);
      const input = { messages: body.messages, max_tokens: max, temperature: 0 };
      if (body.default_thinking !== undefined && body.default_thinking !== true) return json({ error: "default_thinking must be true or absent" }, 400);
      // Gemma's thinking is off unless a test asks for every model's own default
      if (body.model.includes("gemma") && body.default_thinking !== true) input.chat_template_kwargs = { enable_thinking: false };
      try {
        const out = await env.AI.run(body.model, input);
        return json(out);
      } catch (e) {
        return json({ error: String(e && e.message ? e.message : e) }, 502);
      }
    }

    return json({ error: "no such door" }, 404);
  },
};
