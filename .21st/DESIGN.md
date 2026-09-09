# Website design

The portfolio uses warm paper, charcoal, Georgia headlines and system body text; a two-column app grid becomes one column on phones. Each app has its own color field, icon, introduction and availability. The approved card order is Folio, Who’s First?, Where Do We Eat, Reading Habit, then Lankford Legends, then Spreadsheet Tools, numbered 01 through 06.

Reading Habit follows the supplied Classical homepage in reading-habit-site/design/site: Cormorant Garamond, Lora, paper, hairlines, and gold. The icon is copied from the current native AppIcon-1024.png: an unframed gold R on charcoal. Supplied CSS app illustrations are illustrations, not app screenshots. Preserve opt-in progress copy and reading marks without checkmarks.

Where Do We Eat follows site-design/Where Do We Eat Homepage.zip: self-hosted Archivo, 2px rules, flat geometry, left alignment and red. Keep original screenshot colors; no rounded cards or shadows in this app section.

Who’s First? uses the current native Five Seats, One Table icon, the exact Wingspan Original watercolor palette (#DFE6E0, #C9D7D4, #7EAFCA), coral/saffron/sky/leaf/plum accents, and existing native build-18 native captures. Chooser, Tap In and Pinball each have a dedicated section. The website markets only the iPhone app: no playable web route or browser-game links.

Folio uses warm neutral surfaces, an orange accent, system typography and real native library/reader screenshots. Its support and privacy copy is preserved from folio-privacy.

Common header/footer and document layout are in assets/family.css. All subpages inherit their app’s theme. Keyboard focus, semantic landmarks, guide anchors and reduced motion are required. No analytics or third-party font requests. Fonts from google/fonts are bundled under their OFL licenses.

21st search: "minimal app portfolio static landing page" (2026-09-08). Catalog matches were React components; no catalog code was retrieved or installed. Existing static HTML primitives and supplied designs are the implementation source.

Lankford Legends is the fifth portfolio-app card, linking to https://lankfordlegends.co/. Use a crisp white card background (#ffffff), Cardinals navy text (#0C2340), and Cardinals red accents (#C41E3A). Dark mode uses navy with white text. It inherits the shared system headline font at weight 500 and card structure. The white-backed baseball diamond SVG uses Cardinals red, a navy outline, and smaller, thinner white LL lettering. The owner rejected the dusty rose revision; preserve the team colors exactly. The heavy serif headline, yellow accents, and thick bottom rule remain removed. Copy leads with a daily Cardinals catch-up; see MESSAGING.md. Spreadsheet Tools shares the final row beside the blog.

The homepage is a portfolio of AI-assisted apps, tools, and experiments. Per Brian’s latest request, Spreadsheet Tools is a card beside Lankford Legends, before About. Link to the existing public browser tools and the spreadsheet-scripts GitHub repository; preserve their hosting.

Where Do We Eat’s September 9 gallery uses four actual Work Lunch simulator screenshots with fictional sample data. Decide remains in the hero; Choices/Log share a two-column ruled gallery that stacks on phones; visit details illustrate memory. Use the exact 4A native red-background icon everywhere. Its 22.4% HTML corner mask is the icon-specific exception to flat page geometry; source PNG stays square.

The Work Lunch gallery now uses a compact Choose/Remember tabbed showcase, with context and people-specific exclusions explained beside one native screenshot. Tabs follow the explanatory copy on phones. Preserve full-size image links and the no-JavaScript fallback. Existing Archivo, rule, button and screenshot primitives are reused; 21st feature-showcase search informed the pattern without importing React components.

Spreadsheet Tools is hosted at /spreadsheet-tools/ and follows Folio’s cream/orange palette. Source is in the sibling spreadsheet-webapp frontend; generated files are synced into this repository. Its portfolio card is sixth, beside Lankford Legends.

Each card identifies its type beneath the project name: iOS app, Blog, or Utility. Reuse the existing static card structure. Spreadsheet Tools has a simple pale-blue/slate spreadsheet SVG icon. Remove the dedicated blog navigation link. On phones the final pair stacks in blog-then-utility order.

Approved brighter homepage palette: Folio apricot #ffdbb5 with orange accents; Who’s First? seafoam #bde0d2 with deep teal; Where Do We Eat ivory #fff3df with tomato red; Reading Habit parchment #f2dfae with charcoal; Lankford Legends white with exact Cardinals navy and red; Spreadsheet Tools pale blue #d5e6f4 with slate. These are portfolio card treatments; app-page palettes remain independent. Preserve legible dark-mode colors and use full-opacity eyebrow accents.

Homepage share preview: assets/social-projects-v2.png is a 1200 × 630 image using the current headline, all six projects in order, approved card colors, and app/blog/utility labels. Rebuild with `python3 scripts/build_social.py` (Pillow required). Change the image URL when revising the artwork to help sharing services refresh cached previews. Homepage Open Graph and Twitter metadata reference this image.
