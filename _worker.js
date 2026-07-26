const BLOCKED_PREFIXES = [
  "/.plan",
  "/.github",
  "/docs",
  "/scripts",
  "/sources",
  "/guidelines/myeloma/_dev",
];

const BLOCKED_FILES = new Set([
  "/README.md",
  "/WEBSITE_COMMANDS.md",
  "/_config.yml",
]);

function isBlocked(pathname) {
  if (BLOCKED_FILES.has(pathname)) return true;
  return BLOCKED_PREFIXES.some(
    (prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`),
  );
}

export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);

    if (isBlocked(pathname)) {
      return new Response("Not found", {
        status: 404,
        headers: {
          "cache-control": "no-store",
          "content-type": "text/plain; charset=utf-8",
          "x-content-type-options": "nosniff",
        },
      });
    }

    return env.ASSETS.fetch(request);
  },
};
