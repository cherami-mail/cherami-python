// Standalone generation: only the bundled public contract is required.
// HTTPX handles I/O; these generated wrappers share one request/response policy.
import { unlink } from "node:fs/promises";
const root = new URL("../", import.meta.url);
const spec = await Bun.file(new URL("openapi.json", root)).json();
const selected: string[] = await Bun.file(new URL("operations.json", root)).json();
const snake = (s: string) => s.replace(/[A-Z]/g, c => `_${c.toLowerCase()}`);
const pascal = (s: string) => s[0]!.toUpperCase() + s.slice(1);
const found = new Map<string, any>();
for (const [path, methods] of Object.entries(spec.paths)) {
  for (const [method, op] of Object.entries(methods as Record<string, any>)) {
    if (!op.operationId) continue;
    if (!selected.includes(op.operationId) || found.has(op.operationId)) throw new Error(`Unexpected operation: ${op.operationId}`);
    found.set(op.operationId, { ...op, path, method: method.toUpperCase() });
  }
}
if (found.size !== selected.length) throw new Error("Missing selected operations.");
const models = structuredClone(spec);
const descriptors: Record<string, any> = {};
const methods: string[][] = [[], []];
const pageFields: Record<string, string> = { listMessages: "messages", listSentMessages: "messages", listDrafts: "drafts", listLabels: "labels", listThreads: "threads", getThread: "messages" };
const pages: string[][] = [[], []];
const items: string[][] = [[], []];
function resolve(s: any): any { return s.$ref ? resolve(spec.components.schemas[s.$ref.split("/").at(-1)]) : s; }
for (const id of selected) {
  const op = found.get(id), name = snake(id), prefix = pascal(id);
  const properties: Record<string, any> = {}, required: string[] = [];
  for (const p of op.parameters ?? []) { properties[p.name] = p.schema; if (p.required) required.push(p.name); }
  if (op.requestBody) { properties.body = op.requestBody.content["application/json"].schema; required.push("body"); }
  const hasParams = Object.keys(properties).length > 0;
  if (hasParams) models.components.schemas[`${prefix}Params`] = { type: "object", properties, required, additionalProperties: false };
  const successes = Object.entries(op.responses).filter(([s]) => /^2\d\d$/.test(s));
  const binary = id === "downloadRawMessage" || id === "downloadAttachment";
  let result = "httpx.Response";
  if (!binary) {
    const responses = successes.map(([, r]: any) => r.content["application/json"].schema);
    models.components.schemas[`${prefix}Result`] = responses.length === 1 ? responses[0] : { anyOf: responses };
    result = `models.${prefix}Result`;
  }
  descriptors[name] = { path: op.path, method: op.method, path_params: (op.parameters ?? []).filter((p: any) => p.in === "path").map((p: any) => p.name), query_params: (op.parameters ?? []).filter((p: any) => p.in === "query").map((p: any) => p.name), body: !!op.requestBody, binary, success_statuses: successes.map(([s]) => Number(s)) };
  for (let async = 0; async < 2; async++) {
    const args = hasParams ? `params: models.${prefix}Params, ` : "";
    methods[async]!.push(`    ${async ? "async " : ""}def ${name}(self, ${args}*, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[${result}]:\n        """${op.summary.replaceAll('"', "'")}. See the HTTP reference for state/recovery semantics."""\n        return ${async ? "await " : ""}self._request(ROUTES[${JSON.stringify(name)}], ${hasParams ? "params" : "{}"}, timeout=timeout)\n`);
    if (pageFields[id]) {
      const schema = resolve((successes[0]![1] as any).content["application/json"].schema);
      models.components.schemas[`${prefix}Item`] = schema.properties[pageFields[id]!].items;
      const iterator = async ? "AsyncIterator" : "Iterator";
      const args = `self, operation: Literal[${JSON.stringify(name)}], params: models.${prefix}Params, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT`;
      pages[async]!.push(`    @overload\n    def pages(${args}) -> ${iterator}[ApiResponse[${result}]]: ...\n`);
      items[async]!.push(`    @overload\n    def iterate(${args}) -> ${iterator}[models.${prefix}Item]: ...\n`);
    }
  }
}
// TypedDicts intentionally use HTTP wire strings for timestamps and preserve names
// such as "from" through functional TypedDict declarations. No schema coercion.
// The generator models these allOf refinements as TypedDict inheritance, which
// Python rejects when an optional bool becomes a required Literal. Flatten only
// the known receipt refinements in the generation input, not the public contract.
// Fail on a new kind of overlap instead of silently broadening an intersection.
function flattenReceipts(value: any): any {
  if (Array.isArray(value)) return value.map(flattenReceipts);
  if (!value || typeof value !== "object") return value;
  if (value.allOf?.length === 2 && ["CreatedInbox", "CreatedDraft", "SendReceipt"].some(name => value.allOf[0].$ref === `#/components/schemas/${name}`)) {
    const base = structuredClone(resolve(value.allOf[0]));
    const extra = value.allOf[1];
    for (const [key, schema] of Object.entries(extra.properties) as [string, any][]) {
      const original = base.properties[key];
      if (JSON.stringify(original) !== JSON.stringify(schema) && !(key === "replayed" && original.type === "boolean" && typeof schema.const === "boolean")) {
        throw new Error(`Review new allOf property refinement: ${key}`);
      }
      base.properties[key] = schema;
    }
    base.required = [...new Set([...base.required, ...extra.required])];
    return flattenReceipts(base);
  }
  return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, flattenReceipts(v)]));
}
const temp = new URL(".generation.json", root);
await Bun.write(temp, JSON.stringify(flattenReceipts(models)));
try {
  const child = Bun.spawn(["uv", "run", "--locked", "datamodel-codegen", "--input", ".generation.json", "--input-file-type", "openapi", "--output", "src/cherami/models.py", "--output-model-type", "typing.TypedDict", "--target-python-version", "3.11", "--use-standard-collections", "--use-union-operator", "--enum-field-as-literal", "all", "--disable-timestamp", "--formatters", "builtin", "--no-use-closed-typed-dict", "--allof-class-hierarchy", "if-no-conflict", "--type-mappings", "string+date-time=string", "string+date=string"], { cwd: root.pathname, stdout: "inherit", stderr: "inherit" });
  if (await child.exited) throw new Error("Model generation failed.");
} finally { await unlink(temp); }
const banner = "# Generated from openapi.json by bun scripts/generate.mts. Do not edit.\n";
await Bun.write(new URL("src/cherami/_routes.py", root), `${banner}from ._transport import Route\n\nROUTES = {\n${Object.entries(descriptors).map(([name, d]) => `    ${JSON.stringify(name)}: Route(path=${JSON.stringify(d.path)}, method=${JSON.stringify(d.method)}, path_params=${JSON.stringify(d.path_params)}, query_params=${JSON.stringify(d.query_params)}, body=${d.body ? "True" : "False"}, binary=${d.binary ? "True" : "False"}, success_statuses=${JSON.stringify(d.success_statuses)}),`).join("\n")}\n}\n\nPAGE_FIELDS = ${JSON.stringify(Object.fromEntries(Object.entries(pageFields).map(([k, v]) => [snake(k), v])))}\n`);
const pagination = (async: number) => `${pages[async]!.join("\n")}\n    def pages(self, operation: str, params: Any, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> ${async ? "AsyncIterator" : "Iterator"}[ApiResponse[Any]]:\n        return self._pages(operation, params, max_pages=max_pages, timeout=timeout)\n\n${items[async]!.join("\n")}\n    def iterate(self, operation: str, params: Any, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> ${async ? "AsyncIterator" : "Iterator"}[Any]:\n        return self._iterate(operation, params, max_pages=max_pages, timeout=timeout)\n`;
await Bun.write(new URL("src/cherami/_operations.py", root), `${banner}from collections.abc import AsyncIterator, Iterator\nfrom typing import Any, Literal, overload\nimport httpx\nfrom . import models\nfrom ._transport import ApiResponse, DEFAULT_TIMEOUT, Timeout\nfrom ._client import SyncClient, AsyncClient\nfrom ._routes import ROUTES\n\nclass Cherami(SyncClient):\n${methods[0]!.join("\n")}\n${pagination(0)}\n\nclass AsyncCherami(AsyncClient):\n${methods[1]!.join("\n")}\n${pagination(1)}`);
console.log(`Generated shared models and sync/async methods for ${selected.length} operations.`);
