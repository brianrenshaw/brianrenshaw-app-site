// Native Decks render of the homepage Instagram Story example (fall basketball on a soft background).
// Run in a Swift 6 executable package targeting macOS 15, depending on the local
// Packages/IngestSocialKit package (native commit recorded in the asset manifest).
// Arguments: Tutorial photo directory, isolated output directory.
// The title sits below the photo, not on it: the page is drawn once without text, the bottom of the
// photo's white border is found in that render, and the title is centered between it and the page edge.
import Foundation
import CoreGraphics
import ImageIO
import IngestSocialKit

@main struct Render {
  static func main() async throws {
    let args = CommandLine.arguments
    let tutorial = URL(fileURLWithPath: args[1]), out = URL(fileURLWithPath: args[2])
    try FileManager.default.createDirectory(at: out, withIntermediateDirectories: true)
    let store = try SocialStore(root: out.appendingPathComponent("DemoStore"))
    let renderer = SocialRenderService(assets: store.assets)
    let source = try store.assets.importImage(tutorial.appendingPathComponent("Example26.jpg"))
    let start = SocialStart.basics.first { $0.photos == 1 && !$0.details }!
    var choices = SocialStartChoices(size: .other(SocialRatio(9, 16)), background: .blur,
                                     details: SocialStartChoices.defaultDetails)
    choices.frameWidth = 0.012
    choices.frameColor = .white
    var story = SocialProject()
    story.sources = [source]
    story.frames = [SocialFrame(content: [SocialContent(sourceID: source.id)])]
    try start.template(choices).apply(to: &story)
    story.name = "Story"
    story.kept = true
    story.export.photoWidth = 1080

    let bare = try await renderer.render(project: story, frameID: story.frames[0].id, previewWidth: nil)
    // Walk up the center column from the bottom edge to the first row of the white border.
    let w = bare.width, h = bare.height
    var pixels = [UInt8](repeating: 0, count: w * h * 4)
    let context = CGContext(data: &pixels, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4,
                            space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    context.draw(bare, in: CGRect(x: 0, y: 0, width: w, height: h))
    func white(_ row: Int) -> Bool {  // CGContext rows run bottom-up in memory order here: row 0 is the top.
      let i = (row * w + w / 2) * 4
      return pixels[i] > 245 && pixels[i + 1] > 245 && pixels[i + 2] > 245
    }
    guard let border = (0..<h).reversed().first(where: white) else { throw SocialError("No border found") }
    let gapCenter = (Double(border + 1) + Double(h)) / 2 / Double(h)
    print("Border ends at row", border, "of", h, "; title y", gapCenter)

    var title = SocialText()
    title.text = "Saturday at the park."
    title.fontName = "Georgia-Italic"
    title.size = 0.038
    title.width = 0.9
    title.y = gapCenter
    story.frames[0].texts = [title]
    try store.save(story)
    let image = try await renderer.render(project: story, frameID: story.frames[0].id, previewWidth: nil)
    let target = out.appendingPathComponent("story.png")
    guard let writer = CGImageDestinationCreateWithURL(target as CFURL, "public.png" as CFString, 1, nil) else { throw SocialError("Could not encode") }
    CGImageDestinationAddImage(writer, image, nil)
    guard CGImageDestinationFinalize(writer) else { throw SocialError("Could not save") }
    try SocialCoding.encode(story).write(to: out.appendingPathComponent("story.json"))
    print("Rendered story", image.width, image.height)
  }
}
