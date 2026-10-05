# Ingest 0.9.5 website audit

Reviewed October 5, 2026 against signed Ingest **0.9.5, build 41**, release source `661216f`, and observed native behavior. Historical release entries retain the behavior of their stated versions. The website retains static HTML, the existing neutral/amber design, public routes, and permanent Sparkle feed.

| Reference | Current authority and corrections |
| --- | --- |
| Landing and portfolio | Exact “Ingest. Cull. Browse. Organize.” headline; Workspaces before Metadata Assist; five explicitly illustrative shoots; current Review screenshot; Social Export and optional analysis secondary; native Mac developer story; 0.9.5 download and social artwork. |
| Getting Started | Browse is central. Import… opens reviewed Import Settings. Start with Selected if a selection exists, otherwise All; choose Tagged explicitly. Display filters do not define import scope. Organize and Social Export open separate windows. |
| Guide | Canonical workflows: fixed Review queue, face/detail inspection, reference/candidate comparison, review decisions, workspace settings, import scope/defaults, independent Organize and Social Export. Copy Metadata lets you choose field groups; Paste Metadata applies the clipboard fields directly. |
| Shortcuts | Canonical default keys and contextual behavior, checked against `Commands/CommandCatalog.swift` and Review implementation. F toggles Focus; Shift-F fits. Face inspection and reference/candidate commands depend on the active view. Select/deselect and tab-close keys corrected. |
| Naming & Metadata | Canonical tokens, counters, RAW/JPEG behavior, snippets, and saved metadata. Social Export's native default is `{base}_social`. Settings paths agree with 0.9.5. Metadata Assist reviews Append/Replace operations; Apply leaves the editor open, while Use for Import stages details. |
| Automation | Canonical URL scheme, actions, callbacks, and settings files. Actions use normal native command checks; no claim that every operation always prompts. Settings → Automation is current. |
| Support | macOS 15+, Apple silicon, free during beta, no Ingest account. Scope/defaults agree with the Guide. Backup examples require separate physical drives. Card cleanup and optional network features agree with Privacy. |
| Privacy | Canonical storage/network behavior. Built-in analysis stays local. Optional Claude Second Opinion sends the question and requested previews/crops/measurements through the user's Claude account when Ask is clicked. Its tools cannot modify marks, metadata, or originals. Ingest disables session persistence without making claims about Anthropic retention. RAW-only card cleanup can also delete excluded JPEG/HEIF twins after the RAW is verified at every destination. Default is Leave card alone. |
| Search and sharing | Search index follows current sections, including privacy and support. Site search resolves Download from the page's current release link, with a 0.9.5 fallback. Same-page search navigation respects reduced motion. Dedicated Ingest share image and page metadata updated. |

Release-source evidence includes `Ingest/IngestController.swift` (initial scope and Import Settings), `Ingest/IngestRun.swift` and card-maintenance implementation (verified cleanup), `Workspace/FocusedPhotoReviewView.swift` and `Commands/CommandCatalog.swift` (Review and keys), `IngestCore/Social/SocialModels.swift` (Social Export naming), `Workspace/SecondOpinion.swift` and `Images/ClaudeCullingProvider.swift` (explicit network requests and read-only tool scope). Paths are relative to the native repository's `Sources/` tree. No native source was changed.

All 28 active app screenshots were recaptured from the installed release using the existing 155 licensed public RAW photographs. Every still is a cursor-free native Retina capture, encoded losslessly without resizing or compositing. The new Metadata Assist video is one continuous 30-second native take, applying changes only to disposable demo metadata. Full provenance, PNG/video checksums, dimensions, display limits, and historical archives are in `site/ingest/assets/SOURCES.md`, `screenshots.json`, and `raw-samples.json`. All original RAW hashes were reverified; the demo sidecar was restored. Superseded asset bytes remain unchanged at their original URLs.

Validation:

- Site validator: routes, links, anchors, metadata, assets, American English, plus search-index targets.
- Screenshot validator: 28 active images, 100 archived images, two current videos, and retained historical videos; dimensions, encoding, checksums, poster relationships, and 2× display limits.
- Interaction checks: visibility, looping, native/custom pause, restart, fullscreen, reduced motion, autoplay rejection, load failure, and asynchronous playback races.
- Chrome visual inspection at 390, 834, and 1440 CSS pixels for the landing page, Getting Started, Guide, Shortcuts, Naming & Metadata, Automation, Support, Privacy, and portfolio. Native screenshots, video frames, and share artwork inspected separately. Long reference tables retain contained horizontal scrolling.
- Keyboard checks: workspace dialog initial focus, Tab/Shift-Tab wrapping, Escape and restored trigger focus; full-resolution viewer; search typing and Enter navigation to Review. Phone workspace dialog checked for readable text and contained scrolling. Chrome reduced-motion emulation keeps the video opt-in and disables automatic showcase advancement. With JavaScript disabled, all five workspace examples and full-resolution links remain available inline, with native video controls and the text walkthrough.
- `21st review` reported zero findings for the landing page, Guide, Getting Started, and search script. Catalog access returned HTTP 401, so existing project primitives supplied the design context.
- Both deployment exports and `git diff --check` run before publishing through the existing GitHub Pages workflow. Live route, asset, download, and social metadata verification follows deployment.

Historical release articles, all prior Ingest anchor IDs, the Quick Start redirect, and `site/ingest/appcast.xml` were checked against the pre-refresh revision and preserved.
