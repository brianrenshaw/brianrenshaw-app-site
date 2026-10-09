# Decks help-center evidence

Content baseline: public iPhone/iPad build 113 and Mac build 112, release source `95465403d161aea0828584b78f66d890d7300aee`. Read-only snapshot extracted to `/tmp/decks-docs-source`; no native app files changed.

- iPhone/iPad task steps: `Social/App/SocialLearning.swift`, reconciled against visible section names in `SocialHome.swift` (Layout Builder, Templates, Projects; legacy internal identifiers remain Templates/Saved/Recent).
- Mac commands and shortcuts: `Social/Mac/DecksApp.swift` command catalog.
- Mac export: `DecksExport.swift`; folder/Photos destinations, width controls, job retries.
- Mac preferences, iCloud, recipes, gear and automation: `DecksSettings.swift`.
- Ingest receiving choices: `DecksHandoffReceiver.swift`.
- Fujifilm, destination ratios and Photos Shortcut explanation: previously reviewed Decks support content and release source. No new named-destination or 4K claims.
- Native screenshots: existing isolated-library captures with originals, hashes and provenance in `site/decks/assets/oct06-assets.json` and SOURCES.md.

This is a source-and-capture audit, not a claim that every procedure was freshly replayed on physical devices. Full end-to-end batch Photos Shortcuts and cross-device iCloud behavior retain the previously documented validation limits. No hardware Aura test was performed.

Website checks: 21 nonempty task articles with iPhone/iPad/Mac anchors; every previous support anchor retained. Static checker, both Decks builds, isolated portfolio build, JavaScript syntax and 21st UI review passed. Safari inspection: support hub at 375px, topic search filtered Aura to one matching guide, Mac export article and active sidebar at 1440px. Without JS the full topic directory and navigation remain available.

## October 7 update

Current source: 95a303fc005e0e32fb238027672fc0d5fcf82e17. Native help files SocialHelpContentPhone.swift and DecksHelpContent.swift replace the older shared SocialLearning instructions, with specialized website guides retained. Public beta verification: iOS 132 and Mac 125 externally IN_BETA_TESTING; see build132-testflight-status.json. Smart Layout planner and UI source inspected; seven focused native planner tests pass. Native Mac Layout Builder and Destinations inspected, with original-pixel screenshots. No fresh hardware frame, Photos Shortcuts end-to-end, or cross-device replay claimed.

Website review: homepage Smart Layout section at 375 and 1440 CSS pixels; Smart Layout help and Aura frame table at 834; Aura content at 375. No visible horizontal overflow in inspected views. Native disclosures toggled with Space and showed focus. New PNGs are linked at full size; WebP decoded pixels match the originals. The 200% Safari zoom selection was interrupted by external app-state changes and is not claimed as complete. Site checker, Decks build, portfolio build, and 21st review passed.

## Build 148 (October 9, 2026)

Current source: `42c30ae` in `photo-importer-details` (read-only; `git diff 95a303f..42c30ae` reviewed). The help center text now matches build 148 labels and flows: Layout Builder is Home on iPhone, iPad, and Mac; the start flow is one screen with Layout, Frame, and Camera tools, Photos per Page, Split Page, and Join with Next; smart layouts work for any destination; the Smart Layout builder, the single camera details card, Camera Details Designs, Date Stamp, logo Photo Corner, Snap to Guides on Mac, and Horizontal/Vertical position fields are documented. Two articles were added: `date-stamp` and `smart-layout-builder`.

Sources read for labels (all at `42c30ae`):

- iPhone/iPad: `SocialHome.swift`, `SocialHomeChrome.swift`, `SocialStartPage.swift`, `SocialStartFlow.swift`, `SocialSmartGroups.swift`, `SocialSmartLayoutBuilder.swift`, `SocialGroupingEditor.swift`, `SocialSaveTemplate.swift`, `SocialTemplateGallery.swift`, `SocialTemplatePicker.swift`, `SocialDetailsEditor.swift`, `SocialMetadataInspector.swift`, `SocialFujiInspector.swift`, `SocialStampInspector.swift`, `SocialStampEditing.swift`, `SocialPlaceEditor.swift`, `SocialPlacesList.swift`, `SocialArrangeFrames.swift`, `SocialCanvas.swift`, `SocialEditor.swift`, `SocialEditorAlign.swift`, `SocialTool.swift`, `SocialLibraryBrowser.swift`, and `SocialHelpContentPhone.swift` (its remaining "Layout Builder" wording was not copied).
- Mac: `DecksLayoutBuilder.swift`, `DecksRootView.swift`, `DecksApp.swift` (Go to Home, ⌘1), `DecksSmartLayoutBuilder.swift`, `DecksLibrary.swift`, `DecksSaveTemplate.swift`, `DecksInspector.swift`, `DecksStampInspector.swift`, `DecksEditor.swift`, `DecksWorkspace.swift`, `DecksSettings.swift`, and `DecksHelpContent.swift`.
- Shared kit: `SocialStarts.swift`, `SocialDesignedStarts.swift`, `SocialFrameStarts.swift`, `SocialDetailDesignStarts.swift`, `SocialDestinations.swift`, `SocialSmartLayout.swift`; `docs/social/parity.md`.

Screenshots: captures showing Layout Builder, the old Smart Layout step screens, the old camera card, or an editor tool strip without Stamp were removed from articles. Kept: `build132-mac-frame-menu` (Add a Photo Frame sheet), `oct08-smart-spot-phone-share-aura` (system share sheet), and the hardcoded Fujifilm Details, Photos Shortcut setup, and Ingest receiving captures. Replacement captures are listed as NEEDS-SHOT in each article's `source` field. Date Stamp purchase requirements are intentionally not described.

This is a source audit, not a fresh device replay. No new screenshots, hardware frame tests, or cross-device sync replays are claimed.
