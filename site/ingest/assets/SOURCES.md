## 0.9.2 walkthrough refresh

`walkthrough-ingest-0.9.2.webp`, `walkthrough-metadata-0.9.2.webp`, and `walkthrough-workspaces-0.9.2.webp` are native SwiftUI view captures from source `9a36b07` using the opt-in FeatureTourTests capture harness and a disposable demo library. Light appearance, native 2× backing pixels, lossless PNG-to-WebP encoding with pixel equality verified; no resizing or visual edits. These are source-build captures, not signed-release window captures. Metadata is staged only; no real photo writes or imports were performed. Demo landscapes reuse the credited photographs below.

# Ingest assets

Icon: identical to the native Ingest AppIcon asset.

## Historical documentation captures

Screenshots refreshed September 20, 2026 from the signed Ingest 0.2.1 (build 6) release.
These are real, unretouched app captures, encoded as WebP. Versioned image URLs prevent stale browser caches; earlier image paths serve the same refreshed captures. A separate temporary library
and a read-only disk image contain 24 demonstration JPEGs with synthetic camera EXIF.
No personal or client photographs are included. The destination capture follows an actual
verified ingest. Settings examples use disposable demonstration preferences.

Photography from Unsplash via Lorem Picsum, under the Unsplash License
(https://unsplash.com/license):

- Paul Jarvis: https://unsplash.com/photos/6J--NXulQCs
- Paul Jarvis: https://unsplash.com/photos/Cm7oKel-X2Q
- Paul Jarvis: https://unsplash.com/photos/I_9ILwtsl_k
- Paul Jarvis: https://unsplash.com/photos/3MtiSMdnoCo
- Paul Jarvis: https://unsplash.com/photos/IQ1kOQTJrOQ
- Paul Jarvis: https://unsplash.com/photos/NYDo21ssGao
- Paul Jarvis: https://unsplash.com/photos/gkT4FfgHO5o
- Paul Jarvis: https://unsplash.com/photos/Ven2CV8IJ5A
- Paul Jarvis: https://unsplash.com/photos/Ps2n0rShqaM
- Paul Jarvis: https://unsplash.com/photos/P7Lh0usGcuk
- Alejandro Escamilla: https://unsplash.com/photos/du_OrQAA4r0
- Alejandro Escamilla: https://unsplash.com/photos/8yqds_91OLw
- Alejandro Escamilla: https://unsplash.com/photos/cZhUxIQjILg
- Alejandro Escamilla: https://unsplash.com/photos/Iuq0EL4EINY
- Jerry Adney: https://unsplash.com/photos/_WiFMBRT7Aw
- Go Wild: https://unsplash.com/photos/V0yAek6BgGk
- Shyamanta Baruah: https://unsplash.com/photos/aeVA-j1y2BY
- How-Soon Ngu: https://unsplash.com/photos/7Vz3DtQDT3Q

The repeated landscape frames are demonstration exposure variants used to exercise bracket
stacking. Camera details are synthetic fixture metadata, not claims about the original photographs.

## RAW histogram development capture

`raw-histogram-0.6.0-retina.webp` is an unretouched native 2× window capture of the Ingest 0.6.0 (12) release build. It shows the actual RAW histogram and LibRaw-rendered preview beside the largest embedded JPEG from the same Canon EOS R5 file. It is not a simulated exposure comparison. The capture excludes the cursor and window shadow and is encoded losslessly without resizing.

The public demonstration RAW is Benjamin Grimm-Lebsanft’s CC0 Canon EOS R5 sample, raw.pixls.us entry 4694: https://raw.pixls.us/getfile.php/4694/nice/Canon%20-%20EOS%20R5%20-%203%3A2.CR3 . The original’s metadata credits the creator and states CC0; the camera fixture manifest records the same license. SHA-256: `21430c36387efe65bd09ac0fcd724bfd959d93dd391ec811a1b741c8663becb5`. A disposable local copy was used with an isolated app library; no personal or client photographs are shown.


## Landing page — Ingest 0.8.5 (27)

Captured September 24, 2026 from the signed, notarized 0.8.5 release, in a separate temporary library using `INGEST_TEST_LIBRARY`. The twelve `*-0.8.5-retina.webp` files are genuine native window captures, without the cursor or window shadow. They retain native 2× Retina pixels; exact capture dimensions and logical display limits are recorded per image in `screenshots.json`. WebP encoding is lossless, with decoded RGBA pixels verified against each original PNG. No UI elements or photographic pixels were composited into the screenshots.

The download was verified before changing website links: Developer ID signature and Gatekeeper notarization checks passed. The DMG SHA-256 matches the public release asset digest: `5382709993d8863d7b8c8991f82aee7b7ba19935766c9bc25edc003d136d1330` (22,025,836 bytes). The Sparkle feed was left unchanged.

All photographs are public licensed demonstration material. Additional Unsplash photographs are used under the [Unsplash License](https://unsplash.com/license), checked at capture time:

- Francesca Tosolini — [Living room interior](https://unsplash.com/photos/living-room-interior-6japTIjUQoI)
- Francesca Tosolini — [Living room with fireplace](https://unsplash.com/photos/a-living-room-filled-with-furniture-and-a-fire-place-4TlrOY2IyUA)
- Olivia Bauso — [Bride and groom](https://unsplash.com/photos/sitting-bride-and-groom-kissing-WXCv0vowciQ)
- Wu Jianxiong — [Groom and bride holding hands](https://unsplash.com/photos/groom-and-bride-holding-hands-4TET084JWaA)
- Mark Zamora — [Bride and groom smiling](https://unsplash.com/photos/bride-and-groom-smiling-28FS3sjHQV8)
- Lauren Mitchell — [Bride and groom holding hands](https://unsplash.com/photos/a-bride-and-groom-holding-hands-and-smiling-glouLzM1PMg)
- Gary Bendig — [Deer](https://unsplash.com/photos/deer-looking-up-at-leaf-at-daytime-n72mzEO_3ds)

Personal and coastal landscape examples reuse the credited Paul Jarvis photographs above. The RAW viewer uses the unchanged CC0 Canon EOS R5 sample credited above; its SHA-256 was reverified. JPEG stock photographs are not presented as RAW samples.

Workspaces are example configurations. The real estate example preserves Brian’s address-based filename/folder tokens and originals/autohdr/final_exports structure, with private paths and client information replaced by temporary demo destinations and an illustrative address. Its two three-frame exposure stacks use exact-pixel copies of the stock interiors with synthetic exposure and capture-time metadata, solely to demonstrate grouping; they are not genuine camera bracket sequences or HDR outputs. Wedding keeper-review examples include an exact duplicate photograph and synthetic capture-time metadata. No quality or speed benchmark is implied.

Backup destinations are disposable directories demonstrating the configuration, not independent physical backup media. No real ingest or organization operation was run for these previews. Apple Photos was disabled in the isolated library; the page correctly describes its integration as a global setting, separately from workspace-specific Social Export visibility. No personal photo library or client imagery is included.

The site-wide documentation refresh uses the same signed 0.8.5 capture set. Older captures have been removed from active pages and retained at their existing URLs, with dimensions in `archivedImages` in the manifest. Their image integrity remains checked; active pages may only reference current captures.

## Ingest 0.9.0 focused captures — September 25, 2026

Five native Retina window captures from the signed, notarized 0.9.0 (29) release: `browse`, `workspaces`, `ingest`, `palette`, and `metadata-assist` with the `-0.9.0-retina.webp` suffix. The app used an isolated disposable demo library. No personal photographs, cards, or private paths are shown. Import destinations are demonstration folders; this is a setup view, not a claim of a completed backup.

Captured using `screencapture -x -o -a -l WINDOW_ID`, then encoded with `cwebp -lossless` without cropping, resizing, or compositing. Main windows: 2402 × 1646 pixels (1201 × 823 points). Settings: 1960 × 1400 pixels (980 × 700 points). Source PNGs and demo state remain local.

Demonstration photographs by Paul Jarvis, provided by Lorem Picsum from Unsplash; [Unsplash license](https://unsplash.com/license). Local filenames are Weekend-010, 011, 012, 015, 016, and 017.jpg, respectively:

- [Paul Jarvis, photo 10](https://unsplash.com/photos/6J--NXulQCs)
- [Paul Jarvis, photo 11](https://unsplash.com/photos/Cm7oKel-X2Q)
- [Paul Jarvis, photo 12](https://unsplash.com/photos/I_9ILwtsl_k)
- [Paul Jarvis, photo 15](https://unsplash.com/photos/NYDo21ssGao)
- [Paul Jarvis, photo 16](https://unsplash.com/photos/gkT4FfgHO5o)
- [Paul Jarvis, photo 17](https://unsplash.com/photos/Ven2CV8IJ5A)


## Ingest 0.9.2 (32) — varied collection refresh

Six homepage screenshots (`browse`, `workspaces`, `ingest`, `palette`, `metadata-assist`, and `assistance`, with `-0.9.2-retina.webp`) are native window captures from the signed, notarized release build 32. Captured September 25, 2026 using `screencapture -x -o -a -l`, without the cursor, window shadow, desktop, menu bar, or sharing overlays. Encoded with `cwebp -lossless -exact`; decoded RGBA pixels were checked against every original PNG. No resizing, compositing, fades, or photo edits were applied. Settings uses a taller native window to keep the destination tree and filename controls readable.

The isolated library contains 72 distinct, free Unsplash photographs, 12 per category. Visible collection names are Portfolio, Landscapes, Wildlife, Cityscapes, Coffee Shops, Weddings, and Birthdays. EOS R5 is a disposable ExFAT disk image with a camera-style DCIM folder, not a physical card. Primary and backup paths are disposable local folders, not independent backup devices. Metadata is staged only; keeper suggestions await approval, and no tags were applied. No personal or client photos are included. Photography is used under the [Unsplash License](https://unsplash.com/license); premium/Unsplash+ search results were excluded.

- Landscape / `01-Landscape.jpg` — [Alessio Soggetti: snow-covered mountain summit](https://unsplash.com/photos/snow-covered-mountain-summit-wH3POmZAsio)
- Landscape / `02-Landscape.jpg` — [Florian Schönbrunner: brown rocky mountain under white clouds and blue sky during daytime](https://unsplash.com/photos/brown-rocky-mountain-under-white-clouds-and-blue-sky-during-daytime-rj6P1M_fz6M)
- Landscape / `03-Landscape.jpg` — [Daniel J. Schwarz: snow covered mountain under cloudy sky during daytime](https://unsplash.com/photos/snow-covered-mountain-under-cloudy-sky-during-daytime-pfywsjCLzKQ)
- Landscape / `04-Landscape.jpg` — [Alessio Soggetti: black rocky mountain under white cloudy sky](https://unsplash.com/photos/black-rocky-mountain-under-white-cloudy-sky-zxcBR3zNc7I)
- Landscape / `05-Landscape.jpg` — [Daniel J. Schwarz: brown and gray rocky mountain under white cloudy sky during daytime](https://unsplash.com/photos/brown-and-gray-rocky-mountain-under-white-cloudy-sky-during-daytime-xQqhrScwpB4)
- Landscape / `06-Landscape.jpg` — [Joe Dudeck: green trees near mountain under white clouds during daytime](https://unsplash.com/photos/green-trees-near-mountain-under-white-clouds-during-daytime-7fIs0xMspSY)
- Landscape / `07-Landscape.jpg` — [Fabrizio Conti: bird's eye view of mountains](https://unsplash.com/photos/birds-eye-view-of-mountains-6uKNk9K0gcM)
- Landscape / `08-Landscape.jpg` — [Hoach Le Dinh: black and white mountains under white clouds](https://unsplash.com/photos/black-and-white-mountains-under-white-clouds-zB9CSwPBIPE)
- Landscape / `09-Landscape.jpg` — [Alexandru-Bogdan Ghita: a mountain with clouds in the sky](https://unsplash.com/photos/a-mountain-with-clouds-in-the-sky-AtAFwG5z1e4)
- Landscape / `10-Landscape.jpg` — [Daniel J. Schwarz: gray rocky mountain under white clouds during daytime](https://unsplash.com/photos/gray-rocky-mountain-under-white-clouds-during-daytime-REjuIrs2YaM)
- Landscape / `11-Landscape.jpg` — [Khashayar Kouchpeydeh: brown and black mountain under white clouds](https://unsplash.com/photos/brown-and-black-mountain-under-white-clouds-tvKwBlrhSAA)
- Landscape / `12-Landscape.jpg` — [Nikola Mihajloski: a view of a mountain range with a lake in the foreground](https://unsplash.com/photos/a-view-of-a-mountain-range-with-a-lake-in-the-foreground-AYctl-pOFME)
- Wildlife / `01-Wildlife.jpg` — [Scott Carroll: brown deer beside plants](https://unsplash.com/photos/brown-deer-beside-plants-favQn8WgRyk)
- Wildlife / `02-Wildlife.jpg` — [Alexander Andrews: orange and silver fox](https://unsplash.com/photos/orange-and-silver-fox-mEdKuPYJe1I)
- Wildlife / `03-Wildlife.jpg` — [Andreas Rasmussen: deer on brown grass field under gray cloudy sky](https://unsplash.com/photos/deer-on-brown-grass-field-under-gray-cloudy-sky-Iw12lY3koDk)
- Wildlife / `04-Wildlife.jpg` — [redcharlie: three rhinos walking on farm road](https://unsplash.com/photos/three-rhinos-walking-on-farm-road-xtvo0ffGKlI)
- Wildlife / `05-Wildlife.jpg` — [Geranimo: two lioness on green plants](https://unsplash.com/photos/two-lioness-on-green-plants-yKiLWMWquKE)
- Wildlife / `06-Wildlife.jpg` — [Maurits Bausenhart: brown leopard sleeping during daytime](https://unsplash.com/photos/brown-leopard-sleeping-during-daytime-42Ocfqp4FAY)
- Wildlife / `07-Wildlife.jpg` — [Geranimo: two zebras on grass field](https://unsplash.com/photos/two-zebras-on-grass-field-N9s3FjzsstM)
- Wildlife / `08-Wildlife.jpg` — [Donnie Ray Crisp: brown and black tiger in close up photography](https://unsplash.com/photos/brown-and-black-tiger-in-close-up-photography-66zrT0dJ7Mc)
- Wildlife / `09-Wildlife.jpg` — [Jessica Anderson: a couple of deer standing on top of a lush green field](https://unsplash.com/photos/a-couple-of-deer-standing-on-top-of-a-lush-green-field-jV2I-dXNvN8)
- Wildlife / `10-Wildlife.jpg` — [Bibhash (Polygon.Cafe) Banerjee: zebra on brown grass field during daytime](https://unsplash.com/photos/zebra-on-brown-grass-field-during-daytime-ZbJwMkhj_yI)
- Wildlife / `11-Wildlife.jpg` — [Kartik Iyer: tiger on brown grass during daytime](https://unsplash.com/photos/tiger-on-brown-grass-during-daytime-XCg1BQf-fso)
- Wildlife / `12-Wildlife.jpg` — [Y S: brown deer on green grass during daytime](https://unsplash.com/photos/brown-deer-on-green-grass-during-daytime-aJuv14zf-ZY)
- City / `01-City.jpg` — [Frans Ruiter: high rise buildings under gray sky](https://unsplash.com/photos/high-rise-buildings-under-gray-sky-x1Py2nXR-wc)
- City / `02-City.jpg` — [Redd Francisco: a city skyline with a bridge in the foreground](https://unsplash.com/photos/a-city-skyline-with-a-bridge-in-the-foreground-XfpSr1OBtio)
- City / `03-City.jpg` — [Reed Naliboff: white boat on sea near city buildings during daytime](https://unsplash.com/photos/white-boat-on-sea-near-city-buildings-during-daytime-8r96TZcaYk4)
- City / `04-City.jpg` — [Gabriel Zainescu: concrete buildings under cloudy sky](https://unsplash.com/photos/concrete-buildings-under-cloudy-sky-itnNSt8N15w)
- City / `05-City.jpg` — [Igor Kyryliuk & Tetiana Kravchenko: city skyline during day time](https://unsplash.com/photos/city-skyline-during-day-time-qikLzipOeXQ)
- City / `06-City.jpg` — [Fabio Fistarol: city skyline across body of water during night time](https://unsplash.com/photos/city-skyline-across-body-of-water-during-night-time-SsdNSIF2FaU)
- City / `07-City.jpg` — [Lerone Pieters: aerial photo of high rise buildings](https://unsplash.com/photos/aerial-photo-of-high-rise-buildings-GdJ9YBoB3Ts)
- City / `08-City.jpg` — [Nic Georgiou: A city at night with a lot of tall buildings](https://unsplash.com/photos/a-city-at-night-with-a-lot-of-tall-buildings-wAUDQAf45JI)
- City / `09-City.jpg` — [Rebecca Hankins: grey and brown building under grey sky](https://unsplash.com/photos/grey-and-brown-building-under-grey-sky-IgGPotkMq_A)
- City / `10-City.jpg` — [Ashim D’Silva: city skyline under blue sky during daytime](https://unsplash.com/photos/city-skyline-under-blue-sky-during-daytime-_FT8JRTgdrc)
- City / `11-City.jpg` — [Toni Tan: a view of a city from the water](https://unsplash.com/photos/a-view-of-a-city-from-the-water-BS2r4YivArk)
- City / `12-City.jpg` — [Alejandro Luengo: city buildings near body of water](https://unsplash.com/photos/city-buildings-near-body-of-water-MUt1cOgNn6M)
- Cafe / `01-Cafe.jpg` — [Steffan Mitchell: brown wooden framed menu board](https://unsplash.com/photos/brown-wooden-framed-menu-board-gHrgeeCCkYA)
- Cafe / `02-Cafe.jpg` — [Austin Park: man writing on wall](https://unsplash.com/photos/man-writing-on-wall-xAS8pWGMMGA)
- Cafe / `03-Cafe.jpg` — [K8: turned-on pendant lamp](https://unsplash.com/photos/turned-on-pendant-lamp-2WzYHsaWyHo)
- Cafe / `04-Cafe.jpg` — [Robert Bye: woman standing on food counter](https://unsplash.com/photos/woman-standing-on-food-counter-F2eHfMwIOxA)
- Cafe / `05-Cafe.jpg` — [RR Abrot: people sitting inside establishment](https://unsplash.com/photos/people-sitting-inside-establishment-pNIgH0y3upM)
- Cafe / `06-Cafe.jpg` — [99.films: round brown wooden tables beside black leather sofa](https://unsplash.com/photos/round-brown-wooden-tables-beside-black-leather-sofa-yr9l_xQPDL0)
- Cafe / `07-Cafe.jpg` — [Louis Hansel: a bar with lots of plants and hanging lights](https://unsplash.com/photos/a-bar-with-lots-of-plants-and-hanging-lights-qoPAjwEiUmg)
- Cafe / `08-Cafe.jpg` — [Fairuz Naufal Zaki: a bookshelf filled with lots of books in a room](https://unsplash.com/photos/a-bookshelf-filled-with-lots-of-books-in-a-room-nVZ81PW-pu8)
- Cafe / `09-Cafe.jpg` — [Daniel: a restaurant with tables and chairs and a painting on the wall](https://unsplash.com/photos/a-restaurant-with-tables-and-chairs-and-a-painting-on-the-wall-8BilbJReBqc)
- Cafe / `10-Cafe.jpg` — [Daniela Araya: containers on white wooden kitchen counter table](https://unsplash.com/photos/containers-on-white-wooden-kitchen-counter-table-BBK_MAfIJUI)
- Cafe / `11-Cafe.jpg` — [Andres Molina: a room with tables and chairs](https://unsplash.com/photos/a-room-with-tables-and-chairs-lzg4B4shScg)
- Cafe / `12-Cafe.jpg` — [Angela Bailey: empty chairs beside window](https://unsplash.com/photos/empty-chairs-beside-window-_uHBJNuKyk8)
- Wedding / `01-Wedding.jpg` — [Shardayyy Photography: selective focus photography white and pink isle flower arrangement](https://unsplash.com/photos/selective-focus-photography-white-and-pink-isle-flower-arrangement-fJzmPe-a0eU)
- Wedding / `02-Wedding.jpg` — [Jennifer Kalenberg: A bride and groom standing in front of a chandelier](https://unsplash.com/photos/a-bride-and-groom-standing-in-front-of-a-chandelier-SI3oKGfzMjk)
- Wedding / `03-Wedding.jpg` — [Matthew Essman: white folding chair in front of body of water](https://unsplash.com/photos/white-folding-chair-in-front-of-body-of-water-jTnipV64uLo)
- Wedding / `04-Wedding.jpg` — [Soulseeker - Creative Photography: A white floral archway over a path with gold chairs for a wedding](https://unsplash.com/photos/wedding-archway-with-white-flowers-aRQrz0fclB8)
- Wedding / `05-Wedding.jpg` — [Redd Francisco: wedding ceremony beside fall trees during daytime](https://unsplash.com/photos/wedding-ceremony-beside-fall-trees-during-daytime-y4bE8ST_CTg)
- Wedding / `06-Wedding.jpg` — [Jakob Owens: bride and groom standing on grass field during daytime](https://unsplash.com/photos/bride-and-groom-standing-on-grass-field-during-daytime-lR--zjgQRY0)
- Wedding / `07-Wedding.jpg` — [Rhamely: a table set up for a wedding reception](https://unsplash.com/photos/a-table-set-up-for-a-wedding-reception-kbOlsfQ5fPE)
- Wedding / `08-Wedding.jpg` — [Michael McAuliffe: bride and groom kissing on grass field during daytime](https://unsplash.com/photos/bride-and-groom-kissing-on-grass-field-during-daytime-YBzj70bym80)
- Wedding / `09-Wedding.jpg` — [fabio guntur: A wedding ceremony with a green carpet and white flowers](https://unsplash.com/photos/a-wedding-ceremony-with-a-green-carpet-and-white-flowers-qG2yK_iNspE)
- Wedding / `10-Wedding.jpg` — [Victoria Priessnitz: man in white dress shirt holding woman in white dress](https://unsplash.com/photos/man-in-white-dress-shirt-holding-woman-in-white-dress-R0B0AnOw0Kg)
- Wedding / `11-Wedding.jpg` — [Leonardo Miranda: people in white dress dancing on green grass field during daytime](https://unsplash.com/photos/people-in-white-dress-dancing-on-green-grass-field-during-daytime-riHGdvluDk8)
- Wedding / `12-Wedding.jpg` — [Tron Le: bride and groom standing beside taqble](https://unsplash.com/photos/bride-and-groom-standing-beside-taqble-PEnHcPYVeOA)
- Birthday / `01-Birthday.jpg` — [Storiès: cake with lit sparkling stick](https://unsplash.com/photos/cake-with-lit-sparkling-stick-ys8qztLjJyg)
- Birthday / `02-Birthday.jpg` — [Duncan Kidd: A chocolate cake with lit candles and chocolate toppings on a dark background](https://unsplash.com/photos/chocolate-birthday-cake-with-lit-candles-qSPxjNn7Uy8)
- Birthday / `03-Birthday.jpg` — [Aneta Pawlik: A hand lighting candles on a birthday cake with white frosting and berries](https://unsplash.com/photos/birthday-cake-with-lit-candles-d8s13D29QiE)
- Birthday / `04-Birthday.jpg` — [Diliara Garifullina: white and pink covered cake with lightened candle](https://unsplash.com/photos/white-and-pink-covered-cake-with-lightened-candle-gK297xpY6os)
- Birthday / `05-Birthday.jpg` — [Annie Spratt: round fondant cake with happy birthday candle](https://unsplash.com/photos/round-fondant-cake-with-happy-birthday-candle-M20ylqCzSZw)
- Birthday / `06-Birthday.jpg` — [Hamid Roshaan: lighted candles on brown wooden table](https://unsplash.com/photos/lighted-candles-on-brown-wooden-table-BQrzI0vi9x0)
- Birthday / `07-Birthday.jpg` — [prosha amiri: brown icing-covered cake with lighted candles](https://unsplash.com/photos/brown-icing-covered-cake-with-lighted-candles-LpnfAOXoGGE)
- Birthday / `08-Birthday.jpg` — [Lan Gao: lighted candles on brown cake](https://unsplash.com/photos/lighted-candles-on-brown-cake-mo28-RNn8j4)
- Birthday / `09-Birthday.jpg` — [Annie Spratt: sliced cake top with star raisins on cake stand](https://unsplash.com/photos/sliced-cake-top-with-star-raisins-on-cake-stand-6SHd7Q-l1UQ)
- Birthday / `10-Birthday.jpg` — [Imants Kaziļuns: happy birthday cake with candles](https://unsplash.com/photos/happy-birthday-cake-with-candles-Z30Jpgmx2UY)
- Birthday / `11-Birthday.jpg` — [Azizbek: A birthday cake with candles that says happy birthday](https://unsplash.com/photos/a-birthday-cake-with-candles-that-says-happy-birthday-Y1Pou755ygM)
- Birthday / `12-Birthday.jpg` — [Nathan Dumlao: boy and girl blowing candles](https://unsplash.com/photos/boy-and-girl-blowing-candles-As8zq82LBpw)

Portfolio display filenames use a curated sequence; the category collections retain the source filenames listed above. No photographic pixels were modified.
- `001-Alpine Light.jpg` → `09-Landscape.jpg`
- `002-Red Fox.jpg` → `02-Wildlife.jpg`
- `003-Waterfront Skyline.jpg` → `03-City.jpg`
- `004-Morning Coffee.jpg` → `09-Cafe.jpg`
- `005-Lakeside Ceremony.jpg` → `03-Wedding.jpg`
- `006-Birthday Layers.jpg` → `09-Birthday.jpg`
- `007-Zebras at Sunset.jpg` → `10-Wildlife.jpg`
- `008-Above the Clouds.jpg` → `10-Landscape.jpg`
- `009-City in Golden Light.jpg` → `04-City.jpg`
- `010-Garden Wedding.jpg` → `04-Wedding.jpg`
- `011-Neighborhood Cafe.jpg` → `10-Cafe.jpg`
- `012-Make a Wish.jpg` → `03-Birthday.jpg`
- `013-Dolomites.jpg` → `02-Landscape.jpg`
- `014-Woodland Deer.jpg` → `01-Wildlife.jpg`
- `015-Evening Skyline.jpg` → `12-City.jpg`
- `016-Books and Coffee.jpg` → `08-Cafe.jpg`
- `017-Wedding Portrait.jpg` → `08-Wedding.jpg`
- `018-Celebration.jpg` → `10-Birthday.jpg`
- `019-Rhinoceros Pair.jpg` → `04-Wildlife.jpg`
- `020-Mountain Valley.jpg` → `12-Landscape.jpg`
- `021-Downtown.jpg` → `07-City.jpg`
- `022-Coffee House.jpg` → `02-Cafe.jpg`
- `023-Just Married.jpg` → `11-Wedding.jpg`
- `024-Birthday Sparkles.jpg` → `01-Birthday.jpg`
- `025-01-Cafe.jpg` → `01-Cafe.jpg`
- `026-01-City.jpg` → `01-City.jpg`
- `027-01-Landscape.jpg` → `01-Landscape.jpg`
- `028-01-Wedding.jpg` → `01-Wedding.jpg`
- `029-02-Birthday.jpg` → `02-Birthday.jpg`
- `030-02-City.jpg` → `02-City.jpg`
- `031-02-Wedding.jpg` → `02-Wedding.jpg`
- `032-03-Cafe.jpg` → `03-Cafe.jpg`
- `033-03-Landscape.jpg` → `03-Landscape.jpg`
- `034-03-Wildlife.jpg` → `03-Wildlife.jpg`
- `035-04-Birthday.jpg` → `04-Birthday.jpg`
- `036-04-Cafe.jpg` → `04-Cafe.jpg`
- `037-04-Landscape.jpg` → `04-Landscape.jpg`
- `038-05-Birthday.jpg` → `05-Birthday.jpg`
- `039-05-Cafe.jpg` → `05-Cafe.jpg`
- `040-05-City.jpg` → `05-City.jpg`
- `041-05-Landscape.jpg` → `05-Landscape.jpg`
- `042-05-Wedding.jpg` → `05-Wedding.jpg`
- `043-05-Wildlife.jpg` → `05-Wildlife.jpg`
- `044-06-Birthday.jpg` → `06-Birthday.jpg`
- `045-06-Cafe.jpg` → `06-Cafe.jpg`
- `046-06-City.jpg` → `06-City.jpg`
- `047-06-Landscape.jpg` → `06-Landscape.jpg`
- `048-06-Wedding.jpg` → `06-Wedding.jpg`
- `049-06-Wildlife.jpg` → `06-Wildlife.jpg`
- `050-07-Birthday.jpg` → `07-Birthday.jpg`
- `051-07-Cafe.jpg` → `07-Cafe.jpg`
- `052-07-Landscape.jpg` → `07-Landscape.jpg`
- `053-07-Wedding.jpg` → `07-Wedding.jpg`
- `054-07-Wildlife.jpg` → `07-Wildlife.jpg`
- `055-08-Birthday.jpg` → `08-Birthday.jpg`
- `056-08-City.jpg` → `08-City.jpg`
- `057-08-Landscape.jpg` → `08-Landscape.jpg`
- `058-08-Wildlife.jpg` → `08-Wildlife.jpg`
- `059-09-City.jpg` → `09-City.jpg`
- `060-09-Wedding.jpg` → `09-Wedding.jpg`
- `061-09-Wildlife.jpg` → `09-Wildlife.jpg`
- `062-10-City.jpg` → `10-City.jpg`
- `063-10-Wedding.jpg` → `10-Wedding.jpg`
- `064-11-Birthday.jpg` → `11-Birthday.jpg`
- `065-11-Cafe.jpg` → `11-Cafe.jpg`
- `066-11-City.jpg` → `11-City.jpg`
- `067-11-Landscape.jpg` → `11-Landscape.jpg`
- `068-11-Wildlife.jpg` → `11-Wildlife.jpg`
- `069-12-Birthday.jpg` → `12-Birthday.jpg`
- `070-12-Cafe.jpg` → `12-Cafe.jpg`
- `071-12-Wedding.jpg` → `12-Wedding.jpg`
- `072-12-Wildlife.jpg` → `12-Wildlife.jpg`


## Ingest 0.9.2 (32) — complete documentation refresh

All active documentation screenshots now use the same signed and notarized build 32 as the homepage. The eleven additional native window captures are workspace-personal, workspace-real-estate, workspace-wedding, workspace-wildlife, organize, command-crop, command-workspaces, social-workspace, copy-metadata, paste-metadata, and shoot-details (each suffixed -0.9.2-retina.webp). All are 2428 × 1622, captured without cursor, shadow, desktop, menu bar, or sharing overlays. Lossless WebP decoding matches each original PNG pixel for pixel. No fades, resizing, or compositing were applied. The old documentation and source-view assets are archived and no longer linked by HTML.

The photos reuse the 72-image public collection credited above. Wedding Preview includes the app’s face close-ups. Social Export shows the actual app canvas with a white border and solid-color background; no export was performed. The EOS R5 source remains a disposable disk image. Personal shows an illustrative fixed date folder, 2026-09-20, since the downloaded photos do not carry their original capture dates. Destination folders are disposable local paths, not separate physical backup devices.

For Organize, category keywords were added only to disposable copies of the 72 photographs in Photo Archive, producing six groups of twelve and a group/sequence filename preview. No organize operation was applied. Copy/Paste Metadata was exercised only on the twelve disposable wedding copies; the final shared caption is “Moments from a wedding celebration.” with wedding and celebration keywords. The import shoot-details capture stages illustrative text only and was canceled. Photographic pixels were not changed by these metadata fixtures.

Real Estate uses two previously credited public interiors by Francesca Tosolini: [living room](https://unsplash.com/photos/living-room-interior-6japTIjUQoI) and [fireplace](https://unsplash.com/photos/a-living-room-filled-with-furniture-and-a-fire-place-4TlrOY2IyUA). Each image has three disposable copies with synthetic camera, timestamp, shutter-speed, and −2/0/+2 exposure metadata so the real app displays two bracket stacks. They are not genuine bracket exposures. The selected 123 Maple Ln address is an illustrative naming example and does not identify the photographed property. No import was performed.
