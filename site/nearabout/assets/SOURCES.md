# Nearabout imagery

All app screens come from native Nearabout UI acceptance captures in the sibling
`NearMe/build/qa` directory, using the isolated Louisville demo library. No app UI
has been generated or recreated. `screenshots.json` records original paths, hashes,
dimensions, and transformations. The source desktop capture is deliberately not
copied into this public repository.

- iPhone: build 23 list, `build23-iphone-initial/E8A7D057-F3EE-4E40-8346-BE80AA62829C.png`.
- iPad: native landscape list/map/place inspector from `redesign-ipad-final-images`;
  EXIF orientation applied before lossless WebP encoding.
- Mac: the isolated native demo window from `mac-drag-during.png`, October 16.
  Cropped to the app window at (805, 505, 3294, 2095), excluding other windows and
  the desktop. This earlier beta capture differs from the current app typography.
- Icon: native `Assets.xcassets/AppIcon.appiconset/AppIcon.png`, resized to 256px.
- Newsreader font: existing repository asset; SIL Open Font License bundled beside it.

The device bezels are simple CSS presentation frames, not photographs or Apple
hardware assets. App screen proportions are retained. The background SVG is a
fictional decorative street pattern, not a navigable map. The share image combines
the genuine phone screen with typeset website copy. Apple Maps attribution remains
visible in the original map captures.

All WebP screenshots retain their original decoded pixel dimensions and use
lossless encoding. The Mac derivative is a window crop, not a reconstructed UI.
