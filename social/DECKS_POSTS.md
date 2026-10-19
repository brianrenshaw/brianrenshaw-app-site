# Decks feature posts

Ten organic posts for Instagram feed, Instagram Stories and Threads. Audience: photographers posting their own work. Copy follows `MESSAGING.md` (October 8 standard and the Decks sections): no em dashes, no slogans, vertical and horizontal for orientation, Decks prepares files and never posts them, nothing about Pro or paid features.

**Before posting:** public TestFlight was build 132 when these were drafted. These posts show features from builds 138 to 158 (Home, Threads panoramas, Date Stamp, camera details as one print). Get a build with them to External testers first.

**How the images are made**
- Finished pages: `scripts/render_decks_posts.swift`, through Decks' own renderer, from the originals listed in `social/decks/posts.json`.
- Screens: `SocialFeaturePostsUITests` in photo-importer-details, exported to `social/decks/captures/`.
- Slides: `python3 scripts/build_decks_posts.py`, written to `social/decks/post-NN/slide-N.png`.

Every photo is Brian's. Instagram captions are not clickable, so the link goes in the bio or on a Story link sticker: https://decksphotoapp.com/

Feed captions end with:

> Decks is in public beta on TestFlight for iPhone, iPad and Mac. Link in bio.

Hashtags: `#decksphotoapp #photography #iosapp #indieapp` (post 8 adds `#fujifilm`).

---

## 1. What Decks is (Instagram feed)

Slides: finished page · Home · pages screen with the Layout panel · three finished pages from one layout.

> Decks makes frames and layouts for your photos.
>
> Choose a layout on Home, choose your photos, and review every page on one screen before you create the project. Decks prepares the files for Instagram posts, Stories and carousels, Threads, and digital photo frames.
>
> Save the layout as a template, and your next set gets the same presentation.

## 2. Smart Layout (Instagram feed)

Slides: the pages Smart Layout made · pages strip · Split Page and Join with Next.

> Smart Layout arranges a mixed batch by photo shape.
>
> On a vertical page, each vertical photo gets its own page and horizontal photos are stacked two to a page. On a sideways page, such as a digital frame, it works the other way around. Swap photos between pages, split a shared page, or join a page with the next one. Turn on "Only if taken within 10 minutes" to pair only photos from the same moment.
>
> Choose Singles & Pairs, Threes or Fours, or build your own.

## 3. Fill Frame, borders and depth (Instagram feed)

Slides: Fill Frame · White Border · Black Border · Depth · Frame panel.

> One photo, four ways.
>
> Fill Frame uses the whole page with no bars. White Border and Black Border set the photo inside a margin. Depth adds a soft shadow under the print. Margins, spacing, border and depth apply to the photo and its details together.

## 4. Templates (Instagram feed)

Slides: one template on three photos · Save as Template · Templates.

> Save a layout as a template and use it on the next set.
>
> A template keeps the page shape, border, margins and text placement. You can also copy one page's look and paste it onto another, or apply it to every page in the project.

## 5. Panorama carousel (Instagram feed)

Slides: the panorama panels, in order · the panorama screen. Post the panels as the carousel so they line up as people swipe.

> A wide photo split into a carousel that lines up as you swipe.
>
> Decks picks the number of panels from the photo's width, from two to six, and you can change it. Each panel is saved as its own 4:5 image, in order.

## 6. Panoramas for Threads (Threads)

Images: the Full-Screen Panorama panels · Home on Threads.

> Threads shows photos up to 3:4 in the feed and the whole image when someone taps it. Decks has two panorama shapes for that: Full-Screen Panorama at 9:19.5 and Tall Panorama at 9:16. Choose Threads on Home and they are the first row.
>
> Decks is in public beta on TestFlight for iPhone, iPad and Mac: https://decksphotoapp.com/

## 7. Stories (Instagram Stories)

Frames: the finished Story · IG Story on Home · Background. Add a link sticker to https://decksphotoapp.com/ on the last frame. The plain line on each screen frame is the only text.

## 8. Camera details (Instagram feed)

Slides: Wall Label · Gear Band · Fujifilm recipe · Camera panel · lens rename.

> Camera details, laid out as part of the print.
>
> Decks reads the camera, lens and exposure from the photo's metadata. Place them under the photo, above it, beside it, or on it, and the photo and details scale together.
>
> For Fujifilm JPEGs, Decks reads the recipe settings saved in the file, and you name the recipe. Rename a lens once and every photo taken with it uses the new name. The photo and its EXIF data are not changed.

## 9. Date Stamp (Instagram Stories)

Frames: the stamped photo · Stamp panel · Place editor. Link sticker on the last frame.

On-frame lines name the control. Optional text sticker on the first frame:

> Date Stamp prints the capture date on the photo. A custom date or place changes only the stamp, never the photo.

## 10. iPhone, iPad and Mac (Threads)

Images: Mac · iPad · iPhone, the same project.

> Decks runs on iPhone, iPad and Mac. With iCloud turned on, your projects, templates and their photos appear on each device, so you can lay out a set on the Mac and save it from your phone. iCloud is optional.
>
> Photos picked in Ingest on the Mac can be sent to Decks.
>
> Decks is in public beta on TestFlight: https://decksphotoapp.com/
