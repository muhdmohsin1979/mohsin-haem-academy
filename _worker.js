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
  "/guidelines/mcl/guideline.docx",
  "/guidelines/mcl/guideline.pdf",
  "/guidelines/mcl",
  "/guidelines/mcl/",
  "/guidelines/mcl/index.html",
  "/guidelines/mcl/guideline-v2.0.docx",
  "/guidelines/mcl/guideline-v2.0.pdf",
  "/guidelines/mcl/quickref-v2.0.docx",
  "/guidelines/mcl/quickref-v2.0.pdf",
  "/guidelines/mcl/algorithm-v2.0.svg",
  "/guidelines/mcl/algorithm-v2.0.excalidraw",
  "/guidelines/mcl/release-manifest-v2.0.json",
  "/guidelines/mcl/release-record-v2.0.json",
  "/assets/figures/mcl-access-status-chart.excalidraw",
  "/assets/figures/mcl-access-status-chart.png",
  "/assets/figures/mcl-access-status-chart.svg",
  "/assets/figures/mcl-first-line-algorithm.excalidraw",
  "/assets/figures/mcl-first-line-algorithm.png",
  "/assets/figures/mcl-first-line-algorithm.svg",
  "/assets/figures/mcl-pathway-at-a-glance.excalidraw",
  "/assets/figures/mcl-pathway-at-a-glance.png",
  "/assets/figures/mcl-pathway-at-a-glance.svg",
  "/assets/figures/mcl-visuals.mmd",
  "/assets/pdfs/mcl-access-status-chart.pdf",
  "/assets/pdfs/mcl-first-line-algorithm.pdf",
  "/assets/pdfs/mcl-pathway-at-a-glance.pdf",
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
