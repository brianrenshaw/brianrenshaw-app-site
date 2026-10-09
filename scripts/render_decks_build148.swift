// Native Decks website examples for build 148: date stamps and camera details designs.
// Run in a Swift 6 executable package targeting macOS 15, depending on the local
// Packages/IngestSocialKit package at native commit 42c30ae (recorded in the asset manifest).
// Arguments: Tutorial photo directory, original DSCF0205.JPG path, isolated output directory.
// Writes one PNG and one project JSON per example. Originals are only read.
import Foundation
import CoreGraphics
import ImageIO
import IngestSocialKit

@main struct Render {
  static func main() async throws {
    let args = CommandLine.arguments
    let tutorial = URL(fileURLWithPath: args[1]), fuji = URL(fileURLWithPath: args[2])
    let out = URL(fileURLWithPath: args[3])
    try FileManager.default.createDirectory(at: out, withIntermediateDirectories: true)
    let store = try SocialStore(root: out.appendingPathComponent("DemoStore"))
    let renderer = SocialRenderService(assets: store.assets)
    func source(_ name: String) throws -> SocialSource {
      let url = name.hasPrefix("/") ? URL(fileURLWithPath: name) : tutorial.appendingPathComponent(name)
      let value = try store.assets.importImage(url)
      print(name, value.exif?.values["exif.model"] ?? "", "FUJI:", value.exif?.fuji?.text ?? "none")
      return value
    }
    func project(_ value: SocialSource) -> SocialProject {
      var p = SocialProject()
      p.sources = [value]
      p.frames = [SocialFrame(content: [SocialContent(sourceID: value.id)])]
      return p
    }
    func save(_ name: String, _ p: SocialProject) async throws {
      let image = try await renderer.render(project: p, frameID: p.frames[0].id, previewWidth: nil)
      let url = out.appendingPathComponent(name + ".png")
      let writer = CGImageDestinationCreateWithURL(url as CFURL, "public.png" as CFString, 1, nil)!
      CGImageDestinationAddImage(writer, image, nil)
      guard CGImageDestinationFinalize(writer) else { throw SocialError("PNG failed") }
      try SocialCoding.encode(p).write(to: out.appendingPathComponent(name + ".json"))
      print("Rendered", name, image.width, image.height)
    }
    let post = SocialStartSize.instagram[0]

    // Date stamps: a single photo with a thin white frame on a white 4:5 page, stamped with the
    // photo's own capture date. Film is left out on purpose.
    func stamped(_ file: String, _ style: SocialStampStyle, time: Bool = false, sideways: Bool = false,
      background: SocialStartBackground = .white) async throws -> SocialProject {
      var p = project(try source(file))
      let start = SocialStart.basics.first { $0.photos == 1 && !$0.details }!
      try start.template(SocialStartChoices(size: post, background: background, details: SocialStartChoices.defaultDetails)).apply(to: &p)
      var stamp = SocialDateStamp(style: style)
      stamp.showsTime = time
      stamp.sideways = sideways ? true : nil
      p.frames[0].content[0].dateStamp = stamp
      p.export.width = 1080
      return p
    }
    try await save("stamp-digital", try await stamped("Example40.jpg", .digital))
    try await save("stamp-clean", try await stamped("Coffee.jpg", .clean, time: true))
    try await save("stamp-typewriter-sideways", try await stamped("Burger.jpg", .typewriter, sideways: true))

    // Camera details designs, each started the way Home starts it, on the page it was drawn for.
    let paper = SocialColor(0.957, 0.949, 0.933), wall = SocialColor(0.11, 0.106, 0.098)
    let designs: [(String, String, SocialStartBackground)] = [
      ("design-gear-band", "Example27.jpg", .white),
      ("design-wall-label", "Example29.jpg", .color(wall)),
      ("design-spec-sheet", fuji.path, .black),
      ("design-spine", "Example24.jpg", .color(paper)),
    ]
    for (id, file, background) in designs {
      let design = SocialStart.detailDesigns.first { $0.id == id }!
      var p = project(try source(file))
      if file == fuji.path { SocialFujiDetails.refreshPortableValues(&p.sources[0]) }
      try design.template(SocialStartChoices(size: post, background: background, details: SocialStartChoices.defaultDetails)).apply(to: &p)
      p.export.width = 1080
      try await save(id, p)
    }
  }
}
