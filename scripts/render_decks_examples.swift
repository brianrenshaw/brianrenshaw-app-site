// Run as a temporary Swift executable depending on Decks's IngestSocialKit.
// Arguments: tutorial photograph directory, PNG output directory.
// Website examples use the native build 77 renderer and original photo metadata.
import Foundation
import CoreGraphics
import ImageIO
import IngestSocialKit

@main struct Gallery {
  static func main() async throws {
    let input = URL(fileURLWithPath: CommandLine.arguments[1])
    let output = URL(fileURLWithPath: CommandLine.arguments[2])
    try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
    let assets = try SocialAssetStore(root: output.appendingPathComponent("working-assets"))
    let renderer = SocialRenderService(assets: assets)
    var sources: [String: SocialSource] = [:]
    for name in ["Burger", "Example40", "Example26", "Example29", "Example24", "Example27", "Example14", "Example25", "Example19", "Sunset", "Example37", "Example38"] {
      sources[name] = try assets.importImage(input.appendingPathComponent(name + ".jpg"))
      let source = sources[name]!
      print(name, source.exif?.values ?? [:])
    }
    func project(_ names: [String], background: SocialStartBackground, details: Bool = false,
                 ratio: SocialRatio = SocialRatio(4, 5), border: Double = 0.012,
                 color: SocialColor = .white, film: Bool = false) throws -> SocialProject {
      let start = SocialStart.basics.first { $0.photos == names.count && $0.details == details }!
      var choices = SocialStartChoices(size: .other(ratio), background: background,
                                      details: SocialStartChoices.defaultDetails)
      choices.frameWidth = border
      choices.frameColor = color
      choices.frameAppearance = film ? .film : .plain
      choices.stock = .triX
      var p = SocialProject()
      p.sources = names.map { sources[$0]! }
      p.frames = [SocialFrame(content: p.sources.map { SocialContent(sourceID: $0.id) })]
      try start.template(choices).apply(to: &p)
      return p
    }
    func save(_ name: String, _ p: SocialProject) async throws {
      let image = try await renderer.render(project: p, frameID: p.frames[0].id, previewWidth: 1200)
      let target = output.appendingPathComponent(name + ".png")
      guard let writer = CGImageDestinationCreateWithURL(target as CFURL, "public.png" as CFString, 1, nil) else { throw SocialError("Could not encode example") }
      CGImageDestinationAddImage(writer, image, nil)
      guard CGImageDestinationFinalize(writer) else { throw SocialError("Could not save example") }
      let data = try SocialCoding.encode(p)
      try data.write(to: output.appendingPathComponent(name + ".json"))
      print("Rendered",name,image.width,image.height)
    }
    try await save("frame-white", project(["Burger"], background: .white))
    try await save("frame-black", project(["Example40"], background: .black, details: true))
    try await save("frame-blur", project(["Example26"], background: .blur))
    try await save("frame-black-border", project(["Example29"], background: .white, border: 0.018, color: .black))
    try await save("frame-blur-pair", project(["Example24", "Example27"], background: .blur))
    try await save("frame-film", project(["Example14"], background: .white, film: true))
    var beside = try project(["Example25"], background: .white, details: true, ratio: SocialRatio(3,2))
    beside.style.fit = .fill
    beside.frames[0].metadataPlate?.opacity = 0
    beside.frames[0].metadataPlate?.textColor = .black
    beside.frames[0].metadataPlate?.showIcons = false
    beside.frames[0].metadataPlate?.size = 0.035
    beside.frames[0] = try SocialQuickArrange.arrange(project: beside, frameID: beside.frames[0].id, direction: .left)
    try await save("camera-beside", beside)
    var below = try project(["Sunset"], background: .black, details: true)
    below.frames[0] = try SocialQuickArrange.arrange(project: below, frameID: below.frames[0].id, direction: .top)
    try await save("camera-below", below)
    try await save("camera-per-photo", project(["Example37", "Example38"], background: .white, details: true))
    var over = try project(["Example19"], background: .black, ratio: SocialRatio(3,2), border: 0)
    over.style.margins = SocialMargins(0)
    over.style.fit = .fill
    var card = SocialMetadataPlate.card(details: SocialStartChoices.defaultDetails)
    card.showIcons = false
    card.size = 0.034
    card.maxWidth = 0.85
    card.position = "Bottom"
    over.frames[0].metadataPlate = card
    try await save("camera-on-photo", over)
  }
}
