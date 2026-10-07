// Run as a temporary Swift executable depending on Decks's IngestSocialKit.
// Arguments: tutorial photograph directory, PNG output directory.
// Website examples use the current IngestSocialKit renderer and original photo metadata.
import Foundation
import CoreGraphics
import ImageIO
import IngestSocialKit

@main struct Gallery {
  static func main() async throws {
    let input = URL(fileURLWithPath: CommandLine.arguments[1])
    let output = URL(fileURLWithPath: CommandLine.arguments[2])
    try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
    let store = try SocialStore(root: output.appendingPathComponent("DemoStore"))
    let assets = store.assets
    let renderer = SocialRenderService(assets: assets)
    var sources: [String: SocialSource] = [:]
    for name in ["Burger", "Example40", "Example26", "Example29", "Example24", "Example27", "Example14", "Example25", "Example19", "Sunset", "Example37", "Example38", "Bridge", "Mamiya", "Coastline", "Coffee"] {
      sources[name] = try assets.importImage(input.appendingPathComponent(name + ".jpg"))
      let source = sources[name]!
      print(name, source.exif?.values ?? [:], "FUJI", source.exif?.fuji?.text ?? "none")
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
    func save(_ name: String, _ original: SocialProject) async throws {
      var p = original
      p.name = name.replacingOccurrences(of: "-", with: " ").capitalized
      p.kept = true
      let auraPass = CommandLine.arguments.contains("--aura-pass")
      if auraPass {
        p.export.photoWidth = p.style.ratio.aspect > 1.5 ? 1280 : p.style.ratio.aspect > 1 ? 1600 : 1080
      }
      try store.save(p)
      let image = try await renderer.render(project: p, frameID: p.frames[0].id, previewWidth: auraPass ? nil : 1200)
      let target = output.appendingPathComponent(name + ".png")
      guard let writer = CGImageDestinationCreateWithURL(target as CFURL, "public.png" as CFString, 1, nil) else { throw SocialError("Could not encode example") }
      CGImageDestinationAddImage(writer, image, nil)
      guard CGImageDestinationFinalize(writer) else { throw SocialError("Could not save example") }
      let data = try SocialCoding.encode(p)
      try data.write(to: output.appendingPathComponent(name + ".json"))
      print("Rendered",name,image.width,image.height)
    }
    // Use the released renderer snapshot for the Aura website pass, without
    // rebuilding the historical October 6 assets or touching personal libraries.
    if CommandLine.arguments.contains("--aura-pass") {
      var pair = try project(["Example24", "Example27"], background: .white, ratio: SocialRatio(16,10), border: 0)
      pair.style.margins = SocialMargins(0.025)
      pair.style.spacing = 0.02
      pair.style.fit = .fill
      pair.frames[0].verticalPair = false
      try await save("aura-pair", pair)
      var soft = try project(["Example26"], background: .blur, ratio: SocialRatio(16,10), border: 0)
      soft.style.margins = SocialMargins(0.04)
      try await save("aura-soft", soft)
      var full = try project(["Coastline"], background: .white, ratio: SocialRatio(4,3), border: 0)
      full.style.margins = SocialMargins(0)
      full.style.fit = .fill
      try await save("aura-full", full)
      var thin = try project(["Sunset"], background: .white, ratio: SocialRatio(4,3), border: 0)
      thin.style.margins = SocialMargins(0.018)
      thin.style.fit = .fill
      try await save("aura-thin", thin)
      try await save("threads-single", project(["Example29"], background: .white))
      return
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

    try await save("hero-pair", project(["Mamiya", "Coastline"], background: .white))
    var story = try project(["Example26"], background: .blur, ratio: SocialRatio(9,16))
    var title = SocialText(); title.text = "October, in color."; title.size = 0.05; title.y = 0.85
    story.frames[0].texts = [title]
    try await save("story", story)
    try await save("aura", project(["Example29"], background: .white, ratio: SocialRatio(16,10)))
    var youtube = try project(["Mamiya"], background: .black, ratio: SocialRatio(16,9))
    youtube.style.margins.bottom = 0.16
    title.text = "A slower way to see."; title.y = 0.92; title.size = 0.035
    youtube.frames[0].texts = [title]
    try await save("youtube", youtube)
    try await save("threads", project(["Example24", "Example27"], background: .white, ratio: SocialRatio(3,2)))
    var panorama = try project(["Coastline"], background: .white)
    panorama.frames = panorama.frames[0].spreadFrames(count: 3, seamless: true)
    for index in panorama.frames.indices {
      var page = panorama; page.frames = [panorama.frames[index]]
      try await save("panorama-\(index + 1)", page)
    }
    let base = try project(["Coffee"], background: .white)
    let template = SocialTemplate(name: "Everyday Frame", project: base, includeText: true)
    try store.save(template)
    for (index, name) in ["Coffee", "Burger", "Example29"].enumerated() {
      var p = SocialProject(); p.sources = [sources[name]!]
      p.frames = [SocialFrame(content: [.init(sourceID: p.sources[0].id)])]
      try template.apply(to: &p)
      precondition(p.style == base.style, "Saved template must reproduce its style")
      try await save("reuse-\(index + 1)", p)
    }
    var fujiSource: SocialSource?
    for name in ["fuji_5963.jpg", "fuji_5924.jpg", "fuji_5063.jpg", "DSCF0205.JPG"] {
      let url = FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent("Downloads/Decks/" + name)
      if FileManager.default.fileExists(atPath: url.path) {
        let source = try assets.importImage(url)
        print("Original Fuji", name, source.exif?.fuji?.text ?? "none")
        if fujiSource == nil, source.exif?.fuji != nil { fujiSource = source }
      }
    }
    if var source = fujiSource {
      SocialFujiDetails.refreshPortableValues(&source)
      var p = SocialProject(); p.sources = [source]
      p.frames = [SocialFrame(content: [.init(sourceID: source.id)])]
      p.style.background = .color; p.style.backgroundColor = .white
      p.style.margins = .init(0.06); p.style.margins.bottom = 0.28
      var card = SocialText(); card.text = "{photo.1.custom.fuji_details}"
      card.color = .black; card.size = 0.025; card.width = 0.86; card.y = 0.86
      card.fujiCard = SocialFujiCard(sourceID: source.id, contentID: p.frames[0].content[0].id)
      card.fujiCard?.fields = ["simulation", "dynamicRange", "highlight", "shadow", "color"]
      card.fujiCard?.slot = 0; card.fujiCard?.usesAvailableFields = false
      p.frames[0].texts = [card]
      try await save("fuji", p)
      print("FUJI EVIDENCE", SocialFujiDetails.text(source, fields: card.fujiCard?.fields))
    } else { throw SocialError("No original photograph retained Fujifilm settings") }
    let clipURL = output.appendingPathComponent("source-clip.mp4")
    if FileManager.default.fileExists(atPath: clipURL.path) {
      let source = try await assets.importVideo(clipURL)
      var p = SocialProject(); p.sources = [source]
      p.frames = [SocialFrame(content: [.init(sourceID: source.id)])]
      p.style.background = .color; p.style.backgroundColor = .black
      p.style.ratio = SocialRatio(4,5); p.export.width = 1080
      let plan = try await renderer.videoPlan(project: p, frameID: p.frames[0].id)
      try await SocialVideoExporter.export(plan: plan, clipURL: assets.url(source.assetID), settings: SocialVideoSettings(), to: output.appendingPathComponent("framed-video.mp4"))
      try await save("video-poster", p)
    }
    print("PASS: template reapplied to three distinct photographs with matching design")
  }
}
