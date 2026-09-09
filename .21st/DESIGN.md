# Website design

The portfolio uses warm paper, charcoal, Georgia headlines and system body text; a two-column app grid becomes one column on phones. Each app has its own color field, icon, introduction and availability.

Reading Habit follows the supplied Classical homepage in reading-habit-site/design/site: Cormorant Garamond, Lora, paper, hairlines, and gold. The icon is copied from the current native AppIcon-1024.png: an unframed gold R on charcoal. Supplied CSS app illustrations are illustrations, not app screenshots. Preserve opt-in progress copy and reading marks without checkmarks.

Where Do We Eat follows site-design/Where Do We Eat Homepage.zip: self-hosted Archivo, 2px rules, flat geometry, left alignment and red. Keep original screenshot colors; no rounded cards or shadows in this app section.

Who’s First? uses the current native Five Seats, One Table icon, the exact Wingspan Original watercolor palette (#DFE6E0, #C9D7D4, #7EAFCA), coral/saffron/sky/leaf/plum accents, and existing native build-18 native captures. Chooser, Tap In and Pinball each have a dedicated section. The website markets only the iPhone app: no playable web route or browser-game links.

Folio uses warm neutral surfaces, an orange accent, system typography and real native library/reader screenshots. Its support and privacy copy is preserved from folio-privacy.

Common header/footer and document layout are in assets/family.css. All subpages inherit their app’s theme. Keyboard focus, semantic landmarks, guide anchors and reduced motion are required. No analytics or third-party font requests. Fonts from google/fonts are bundled under their OFL licenses.

21st search: "minimal app portfolio static landing page" (2026-09-08). Catalog matches were React components; no catalog code was retrieved or installed. Existing static HTML primitives and supplied designs are the implementation source.

Lankford Legends is the fifth portfolio-app card, linking to https://lankfordlegends.co/. Its September 9 revision uses a muted rose background (#eee5e4) and dark rose text (#553e40), with dark-mode equivalents. It inherits the shared system headline font at weight 500, app label, eyebrow, heading arrow, and footer styling. The cream-backed baseball diamond SVG has smaller, thinner white LL lettering and cream bases. The earlier navy card, bold serif headline, yellow accents, and red bottom rule are superseded. Copy leads with a daily Cardinals catch-up; see MESSAGING.md. Utilities remain separate at the bottom.

The homepage is a portfolio of AI-assisted apps, tools, and experiments. Per Brian’s request, spreadsheet utilities are the last section before the footer, after the blog and About. Link to the existing public browser tools and the spreadsheet-scripts GitHub repository; preserve their hosting.

Where Do We Eat’s September 9 gallery uses four actual Work Lunch simulator screenshots with fictional sample data. Decide remains in the hero; Choices/Log share a two-column ruled gallery that stacks on phones; visit details illustrate memory. Use the exact 4A native red-background icon everywhere. Its 22.4% HTML corner mask is the icon-specific exception to flat page geometry; source PNG stays square.

The Work Lunch gallery now uses a compact Choose/Remember tabbed showcase, with context and people-specific exclusions explained beside one native screenshot. Tabs follow the explanatory copy on phones. Preserve full-size image links and the no-JavaScript fallback. Existing Archivo, rule, button and screenshot primitives are reused; 21st feature-showcase search informed the pattern without importing React components.

Spreadsheet Tools is hosted at /spreadsheet-tools/ and follows Folio’s cream/orange palette. Source is in the sibling spreadsheet-webapp frontend; generated files are synced into this repository. Its portfolio placement remains at the bottom.
