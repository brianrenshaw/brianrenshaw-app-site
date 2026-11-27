# Decks website design audit

Reviewed November 27, 2026. The two entry points serve different readers. A photographer on the homepage needs to see what a Decks export looks like. Someone landing directly on the Aura page needs to know whether Decks can prepare pictures for their frame and how those pictures reach it.

| Finding | Change |
| --- | --- |
| Three overlapping devices introduced the software before visitors saw a finished photograph. The opening headline could have described a print service. | Open with Brian’s bridge photograph exported in the Spec Sheet design. Describe three things Decks can do to a photo, then offer the download. Keep native screenshots in the platform and feature sections. |
| The opening gallery, onboarding tour, and saved-template example made similar points in succession. | Remove the tour from the homepage. Keep the gallery for comparing output and the template example for seeing one design applied to different pictures. |
| Aura appeared alongside other export destinations. A gift recipient could miss it or assume Decks sets up the hardware. | Give Aura a prominent homepage invitation and retain its direct landing URL. Explain the Decks-to-Aura handoff in the introduction, show actual exports before the tutorial, and name the iPhone steps and Mac export route. |
| A blanket promise about cropping and frame compatibility obscured the choices buyers need to make. | Show the difference between a paired image, a border, a soft background, and a deliberate crop. Label the compatibility table as the presets in Decks 1.0 and identify the 13-inch Ink. |

## Reference decisions

- Cosmos gives one photograph most of the opening screen. Decks uses one genuine export at readable scale, with a caption identifying the design. [Cosmos on Mobbin](https://mobbin.com/sites/sections/b3994ca2-d26a-4d79-b1e9-fd4bc4c62410)
- Givingli labels example cards by occasion, making each image a way into the product. Artifact Uprising similarly gives holiday visitors a direct route to a finished photo gift. Decks uses a single seasonal invitation while keeping its main introduction useful year-round. [Givingli on Mobbin](https://mobbin.com/sites/sections/590a811c-27de-4b80-b59d-59456882261a) · [Artifact Uprising](https://www.artifactuprising.com/)
- Aura organizes frames by model and orientation. Its hardware catalog includes models beyond the presets in Decks 1.0. The landing page lists only presets found in the shipping app. [Aura Frames](https://auraframes.com/)

## Release and usability checks

App Store Connect reported iOS 1.0 build 171 and macOS 1.0 build 170 ready for sale. The US listing confirmed iOS and iPadOS 18+, macOS 15+ on Apple silicon, and Pro at $1.99 monthly, $9.99 annually, or $24.99 lifetime. Production already linked to the App Store. The install guide retains migration instructions for former TestFlight users. [US App Store listing](https://apps.apple.com/us/app/decks-photo-app/id6817408326)

The dedicated build checked 31 pages and their internal links, assets, canonical URLs, and fragments. Both landing pages fit 375, 768, and 1440 CSS-pixel viewports. The homepage invitation opened the Aura page, and the Aura app FAQ opened at all three widths. This review covered the purchase path through the store link. No purchase or physical frame upload was performed.

## Redesign after owner review

The first revision kept the existing page structure too visibly intact. The published redesign gives the homepage a dark contact sheet with three finished exports, a separate Aura feature, and an expandable toolkit. The platform walkthroughs and export details remain reachable by their original links.

The Aura page starts with the frame owner's task and frustration. A vertical photo zooms in, adjusting it means reopening Aura and pinching the crop, and uploading two separate photos leaves the pairing outside the owner's control. Visitors can compare a zoomed crop, a full-height single, and a finished pair. The crop and fit examples use the same woodland photograph, extracted from the genuine paired Decks export. They illustrate framing choices. The three-step plan follows that demonstration and ends with the handoff to the Aura app.
