// Finished-photo slides for the Decks social posts (social/decks/posts.json, each post's "renders").
//
// Every slide goes through Decks' own code: the start a person picks on Home (One Photo, Singles &
// Pairs, Panorama, Full-Screen Panorama, Wall Label, Gear Band, Fill Frame...), built into a project
// by SocialStartDraftBuilder exactly as the walkthrough does, edited the way the editor edits
// (Shadow switch, Date Stamp, Photo Details recipe name, My Gear lens rename), and rendered by
// SocialRenderService at the export plan's pixel size. Nothing is enlarged: the export plan's own
// no-enlarging rule sets the size, and any page it limits is reported.
//
// Run as a temporary Swift executable package targeting macOS 15 that depends on the local
// IngestSocialKit (keep the package outside both repos):
//
//   PKG=/private/tmp/claude-501/decks-posts-render
//   KIT=/Users/brianrenshaw/Projects/photo-importer-details
//   SITE=/Users/brianrenshaw/Projects/brianrenshaw-app-site
//   mkdir -p $PKG/Sources/RenderDecksPosts
//   cat > $PKG/Package.swift <<EOF
//   // swift-tools-version: 6.0
//   import PackageDescription
//   let package = Package(name: "RenderDecksPosts", platforms: [.macOS(.v15)],
//     dependencies: [.package(path: "$KIT/Packages/IngestSocialKit")],
//     targets: [.executableTarget(name: "RenderDecksPosts", dependencies: ["IngestSocialKit"])],
//     swiftLanguageModes: [.v5])
//   EOF
//   cp $SITE/scripts/render_decks_posts.swift $PKG/Sources/RenderDecksPosts/
//   swift run -c release --package-path $PKG RenderDecksPosts \
//     /Users/brianrenshaw/Downloads/Decks $SITE/social/decks/renders
//
// Arguments: originals directory, output directory, optionally posts.json (default: the output
// directory's parent/posts.json), --kit <repo> (default: the path above, for the commit) and
// --projects <dir> to keep each project's JSON.
// Originals are only read; the Decks store the import needs lives in a temporary directory.
import CoreGraphics
import CryptoKit
import Foundation
import ImageIO
import IngestSocialKit

struct RenderError: Error, CustomStringConvertible {
  var description: String
  init(_ text: String) { description = text }
}

@main struct RenderDecksPosts {
  static func main() async throws {
    var args = Array(CommandLine.arguments.dropFirst())
    var kitRepo = "/Users/brianrenshaw/Projects/photo-importer-details"
    var projects: URL?
    if let i = args.firstIndex(of: "--projects"), args.indices.contains(i + 1) {
      projects = URL(fileURLWithPath: args[i + 1])
      args.removeSubrange(i...(i + 1))
    }
    if let i = args.firstIndex(of: "--kit"), args.indices.contains(i + 1) {
      kitRepo = args[i + 1]
      args.removeSubrange(i...(i + 1))
    }
    guard args.count >= 2 else {
      throw RenderError("Usage: RenderDecksPosts <originals> <output> [posts.json] [--kit <repo>]")
    }
    let originals = URL(fileURLWithPath: args[0])
    let output = URL(fileURLWithPath: args[1])
    let specURL = args.count > 2
      ? URL(fileURLWithPath: args[2]) : output.deletingLastPathComponent().appendingPathComponent("posts.json")
    let runner = try Runner(originals: originals, output: output, spec: specURL, kitRepo: kitRepo)
    runner.projectsDirectory = projects
    try await runner.run()
  }
}

final class Runner {
  let originals: URL
  let output: URL
  let spec: [String: Any]
  let kitCommit: String
  let kitDirty: Bool
  let storeRoot: URL
  let store: SocialStore
  let renderer: SocialRenderService
  var manifest: [[String: Any]] = []
  var notes: [String] = []
  var problems: [String] = []
  var sources: [String: SocialSource] = [:]
  var hashes: [String: String] = [:]
  /// Where to keep each project's JSON (`--projects`), for opening or diffing later.
  var projectsDirectory: URL?

  init(originals: URL, output: URL, spec specURL: URL, kitRepo: String) throws {
    self.originals = originals
    self.output = output
    guard let object = try JSONSerialization.jsonObject(with: Data(contentsOf: specURL)) as? [String: Any] else {
      throw RenderError("posts.json is not an object")
    }
    spec = object
    kitCommit = try Self.git(kitRepo, ["rev-parse", "--short", "HEAD"])
    kitDirty = !(try Self.git(kitRepo, ["status", "--porcelain", "--", "Packages/IngestSocialKit"])).isEmpty
    storeRoot = FileManager.default.temporaryDirectory.appendingPathComponent("decks-posts-store-" + UUID().uuidString)
    store = try SocialStore(root: storeRoot)
    renderer = SocialRenderService(assets: store.assets)
  }
  deinit { try? FileManager.default.removeItem(at: storeRoot) }

  static func git(_ repo: String, _ arguments: [String]) throws -> String {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: "/usr/bin/git")
    process.arguments = ["-C", repo] + arguments
    let pipe = Pipe()
    process.standardOutput = pipe
    try process.run()
    process.waitUntilExit()
    let text = String(data: pipe.fileHandleForReading.readDataToEndOfFile(), encoding: .utf8) ?? ""
    return text.trimmingCharacters(in: .whitespacesAndNewlines)
  }

  // MARK: Photos

  /// Imports an original into the temporary Decks store, the way a picked photo arrives.
  func source(_ name: String) throws -> SocialSource {
    if let known = sources[name] { return known }
    let url = originals.appendingPathComponent(name)
    let data = try Data(contentsOf: url)
    hashes[name] = SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
    let value = try store.assets.importImage(url)
    sources[name] = value
    let facts = SocialGearMatcher.snapshotValues(value)
    print("  photo", name, "\(value.pixelWidth)x\(value.pixelHeight)",
      facts["exif.camera"] ?? "-", "|", facts["exif.lens"] ?? "-", "| fuji:", value.exif?.fuji != nil)
    return value
  }

  // MARK: Destinations and starts

  static func destination(id: String) -> SocialDestination { SocialDestination.named(id)! }
  /// The Home destination whose page is this shape: Instagram 4:5 for the feed, Stories for 9:16.
  func destination(ratio: [Double]) throws -> SocialDestination {
    switch (ratio.first ?? 0, ratio.last ?? 0) {
    case (4, 5): return Self.destination(id: "instagram-4x5")
    case (9, 16): return Self.destination(id: "stories")
    default: throw RenderError("No Home destination for ratio \(ratio)")
    }
  }
  static func start(_ id: String) -> SocialStart { SocialStart.all.first { $0.id == id }! }
  static func color(_ name: String?) -> SocialColor? {
    switch name {
    case "white": .white
    case "black": .black
    default: nil
    }
  }
  static func background(_ name: String?) -> SocialStartBackground? {
    switch name {
    case "white": .white
    case "black": .black
    case "blur": .blur
    default: nil
    }
  }

  /// The project the walkthrough would create from these photos, as `SocialStartFlow` builds it.
  func draft(_ kind: SocialStart, _ choices: SocialStartChoices, _ photos: [SocialSource],
    gear: [SocialGearItem] = []) throws -> SocialProject {
    try SocialStartDraftBuilder.build(
      sources: photos, kind: kind, choices: SocialStartChoiceSet(choices), defaults: SocialDefaults(),
      gear: gear, projectID: UUID(), previous: nil)
  }

  // MARK: Run

  func run() async throws {
    try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
    print("Kit", kitCommit, kitDirty ? "(IngestSocialKit has uncommitted changes)" : "(clean)")
    let posts = spec["posts"] as? [[String: Any]] ?? []
    for post in posts {
      let n = post["n"] as? Int ?? 0
      let size = (post["size"] as? [Int]) ?? []
      let renders = post["renders"] as? [[String: Any]] ?? []
      print("Post \(n) (\(post["slug"] as? String ?? "")): \(renders.count) render(s)")
      let folder = output.appendingPathComponent(String(format: "post-%02d", n))
      if !renders.isEmpty {
        try? FileManager.default.removeItem(at: folder)
        try FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
      }
      for render in renders {
        let id = render["id"] as? String ?? "render"
        let project = try build(post: n, render: render)
        if let projectsDirectory {
          try FileManager.default.createDirectory(at: projectsDirectory, withIntermediateDirectories: true)
          try SocialCoding.encode(project).write(
            to: projectsDirectory.appendingPathComponent(String(format: "post-%02d-", n) + id + ".json"))
        }
        try await export(project, post: n, id: id, folder: folder, expected: size)
      }
    }
    let document: [String: Any] = [
      "kitCommit": kitCommit,
      "kitDirty": kitDirty,
      "renderer": "IngestSocialKit SocialRenderService, export plan size (SocialPlanner.outputSize), PNG",
      "originals": originals.path,
      "notes": notes,
      "problems": problems,
      "files": manifest,
    ]
    let data = try JSONSerialization.data(withJSONObject: document, options: [.prettyPrinted, .sortedKeys])
    try data.write(to: output.appendingPathComponent("manifest.json"))
    print("\nWrote \(manifest.count) PNGs and manifest.json")
    for note in notes { print("NOTE:", note) }
    for problem in problems { print("PROBLEM:", problem) }
  }

  // MARK: Building each render the app's way

  func build(post: Int, render: [String: Any]) throws -> SocialProject {
    let id = render["id"] as? String ?? ""
    let photos = try (render["photos"] as? [String] ?? []).map(source)
    let ratio = (render["ratio"] as? [Double]) ?? (render["panelRatio"] as? [Double]) ?? [4, 5]
    let label = "post \(post) \(id)"

    // Smart Layout: Home's Singles & Pairs row (SocialStart.grouping[0]) at the destination's size,
    // with the walkthrough's own appearance defaults.
    if let smart = render["smartLayout"] as? String {
      guard smart == "singles-and-pairs" else { throw RenderError("\(label): unknown smart layout \(smart)") }
      let kind = SocialStart.grouping[0]
      let choices = kind.choices(for: try destination(ratio: ratio))
      return try draft(kind, choices, photos)
    }

    // Panoramas: Home's Panorama start for Instagram, Full-Screen Panorama for Threads. The panel
    // count is left at 0 so the walkthrough fits it to each photo's width.
    if let pano = render["panorama"] as? String {
      let (kind, destination): (SocialStart, SocialDestination) =
        switch pano {
        case "instagram": (Self.start("threads-panorama"), Self.destination(id: "instagram-4x5"))
        case "threads-full": (Self.start("threads-pano-full"), Self.destination(id: "threads"))
        default: throw RenderError("\(label): unknown panorama \(pano)")
        }
      let choices = kind.choices(for: destination)
      let project = try draft(kind, choices, photos)
      notes.append("\(label): \(kind.name) made \(project.frames.count) panels from a \(photos[0].pixelWidth)x\(photos[0].pixelHeight) photo (SocialStart.fittedPanels).")
      return project
    }

    // Post 4: one template, made once and saved the way Save as Template does, then applied to
    // every photo the way a saved template is picked from Home (SocialDefaults.makeProject).
    if render["template"] != nil {
      let kind = Self.start("one-details")
      var choices = kind.choices(for: try destination(ratio: ratio))
      choices.background = Self.background(render["background"] as? String) ?? .black
      choices.frameAppearance = .plain
      choices.frameWidth = render["border"] as? Double ?? choices.frameWidth
      choices.frameColor = Self.color(render["borderColor"] as? String)
      choices.cameraDetails = true
      let design = try draft(kind, choices, [photos[0]])
      var template = SocialTemplate(name: "Black Print", project: design)
      template.modified = Date(timeIntervalSince1970: 0)
      try store.save(template)
      var defaults = SocialDefaults()
      defaults.templateID = template.id
      var project = try defaults.makeProject(sources: photos, templates: [template])
      _ = SocialGearMatcher.apply([], to: &project)
      let missing = photos.filter { SocialGearMatcher.snapshotValues($0)["exif.camera"]?.isEmpty != false }
      if !missing.isEmpty {
        problems.append("\(label): \(missing.map(\.filename).joined(separator: ", ")) carry no camera metadata: the template's details are empty there, and the Kit (build 158) then also drops the white border and leaves the details' room blank on those pages.")
      }
      return project
    }

    // Lens renames go through My Gear, as "Rename this lens" in Photo Details does: one saved lens
    // matched by the file's own wording. Display only; the file is never written.
    var gear: [SocialGearItem] = []
    if let rename = render["lensRename"] as? String {
      for photo in photos {
        guard let exif = SocialGearMatcher.snapshotValues(photo)["exif.lens"], !exif.isEmpty else {
          problems.append("\(label): \(photo.filename) has no lens in its metadata to rename")
          continue
        }
        gear = SocialGearMatcher.rename(gear, kind: .lens, name: rename, exif: exif)
      }
    }

    var project: SocialProject
    if let look = render["details"] as? String {
      // Camera details designs, started from Home's Designs row on the page each was drawn for.
      let designID: String =
        switch look {
        case "Wall Label": "design-wall-label"
        case "Gear Band": "design-gear-band"
        // Film Box is the recipe look of Home's Film Strip design (SocialStart.detailDesigns).
        case "Film Box", "Film Strip": "design-film-strip"
        case "Spec Sheet": "design-spec-sheet"
        case "Details List": "design-list"
        case "Fujifilm recipe": Self.fujiDesign
        default: throw RenderError("\(label): unknown details design \(look)")
        }
      let kind = Self.start(designID)
      let choices = kind.choices(for: try destination(ratio: ratio))
      project = try draft(kind, choices, photos, gear: gear)
      if render["recipeName"] != nil {
        notes.append("\(label): Fujifilm recipe drawn with the \(kind.name) design (its \(String(describing: project.frames[0].metadataPlate?.design?.recipe?.look ?? .card)) recipe look).")
      }
    } else if render["fit"] as? String == "fill" {
      // Fill Frame: the no-bars layout, at the Instagram 4:5 size.
      let kind = Self.start("frame-full")
      project = try draft(kind, kind.choices(for: try destination(ratio: ratio)), photos, gear: gear)
    } else {
      // One Photo with the walkthrough's Background and Frame answers.
      let kind = Self.start("one-framed")
      var choices = kind.choices(for: try destination(ratio: ratio))
      if let background = Self.background(render["background"] as? String) { choices.background = background }
      if let border = render["border"] as? Double {
        choices.frameAppearance = border > 0 ? .plain : SocialFrameAppearance.none
        if border > 0 { choices.frameWidth = border }
      }
      choices.frameColor = Self.color(render["borderColor"] as? String)
      project = try draft(kind, choices, photos, gear: gear)
      if render["borderColor"] as? String == "white", render["background"] as? String == "white" {
        notes.append("\(label): white line on a white page, as posts.json asks; the line does not show, so the page reads as a white mat.")
      }
    }

    // Depth: the Shadow switch for All Pages (SocialEditorModel.setDepth with scope .all).
    if render["depth"] as? Bool == true {
      project.style.depth = SocialDepth(shadow: SocialDepth.tableShadow)
      for i in project.frames.indices { project.frames[i].overrides.depth = nil }
    }

    // Photo Details: the recipe name a person types (SocialFujiInspector's field editor + editFuji).
    if let name = render["recipeName"] as? String {
      for i in project.sources.indices {
        guard project.sources[i].exif?.fuji != nil else {
          problems.append("\(label): \(project.sources[i].filename) has no Fujifilm settings")
          continue
        }
        var details = project.sources[i].manualDetails ?? SocialPhotoDetails()
        details.setManual(SocialFujiDetails.manualKey("recipeName"), name)
        project.sources[i].manualDetails = details
        SocialFujiDetails.refreshPortableValues(&project.sources[i])
        print("  recipe:\n" + SocialFujiDetails.text(project.sources[i]).split(separator: "\n").map { "    " + $0 }.joined(separator: "\n"))
      }
    }

    // Date Stamp: switched on for every photo (SocialStampEditing.setStamps), Digital style, with
    // the place line in the photo's own wording.
    if let stampSpec = render["stamp"] as? [String: Any] {
      let style = SocialStampStyle.allCases.first { $0.title == stampSpec["style"] as? String } ?? .digital
      guard style != .film else { throw RenderError("\(label): Film stamps are not used in posts") }
      let lines = stampSpec["lines"] as? [String] ?? ["date"]
      var stamp = SocialDateStamp(style: style)
      stamp.showsDate = lines.contains("date")
      stamp.showsTime = lines.contains("time")
      stamp.showsPlace = lines.contains("place")
      stamp.place = stampSpec["place"] as? String
      for i in project.frames.indices {
        for j in project.frames[i].content.indices {
          var own = stamp.look(keeping: nil)
          own.place = stamp.place
          own.hidden = nil
          own.center = nil
          project.frames[i].content[j].dateStamp = own
        }
      }
    }
    return project
  }

  /// The design the Fujifilm recipe slide uses; see the note it leaves in the manifest.
  static let fujiDesign = "design-list"

  // MARK: Export

  func export(_ project: SocialProject, post: Int, id: String, folder: URL, expected: [Int]) async throws {
    // The export plan sets each page's size and refuses to enlarge (allowEnlarging is off).
    let plan = try SocialPlanner.plan(project, directory: storeRoot)
    let multiple = plan.entries.count > 1
    var panels: [CGImage] = []
    for (index, entry) in plan.entries.enumerated() {
      // A preview first, as the editor draws before export: designed details are measured from
      // the page as last drawn.
      _ = try await renderer.render(project: project, frameID: entry.frame.id, previewWidth: 540)
      let image = try await renderer.render(project: project, frameID: entry.frame.id)
      let name = id + (multiple ? "-page-\(index + 1)" : "") + ".png"
      let url = folder.appendingPathComponent(name)
      guard let writer = CGImageDestinationCreateWithURL(url as CFURL, "public.png" as CFString, 1, nil) else {
        throw RenderError("Could not create \(url.path)")
      }
      CGImageDestinationAddImage(writer, image, nil)
      guard CGImageDestinationFinalize(writer) else { throw RenderError("Could not write \(url.path)") }
      let names = entry.frame.content.compactMap { content in
        project.sources.first { $0.id == content.sourceID }?.filename
      }
      let files = names.map { name in sources.first { $0.value.filename == name }?.key ?? name }
      var row: [String: Any] = [
        "post": post, "id": id, "page": index + 1, "pages": plan.entries.count,
        "file": url.path.replacingOccurrences(of: output.path + "/", with: ""),
        "sources": files, "sourceSHA256": files.map { hashes[$0] ?? "" },
        "width": image.width, "height": image.height, "kitCommit": kitCommit,
      ]
      if let limited = entry.limitedBy { row["limitedBy"] = limited }
      manifest.append(row)
      let sizeOK = expected.count == 2 && image.width == expected[0] && image.height == expected[1]
      if !sizeOK {
        problems.append("post \(post) \(name): \(image.width)x\(image.height), expected \(expected.map(String.init).joined(separator: "x"))"
          + (entry.limitedBy.map { "; limited by \($0) (not enlarged)" } ?? ""))
      }
      print("  wrote", row["file"]!, "\(image.width)x\(image.height)", sizeOK ? "" : "SIZE MISMATCH")
      if entry.frame.spread != nil { panels.append(image) }
    }
    if panels.count > 1 { checkSeams(panels, label: "post \(post) \(id)") }
  }

  /// Neighboring panorama panels should continue each other: compare the last column of one panel
  /// with the first column of the next, against the variation inside a panel.
  func checkSeams(_ panels: [CGImage], label: String) {
    func column(_ image: CGImage, _ x: Int) -> [Double] {
      let h = image.height
      var pixels = [UInt8](repeating: 0, count: 4 * h)
      let context = CGContext(data: &pixels, width: 1, height: h, bitsPerComponent: 8, bytesPerRow: 4,
        space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
      context.draw(image, in: CGRect(x: -x, y: 0, width: image.width, height: h))
      return stride(from: 0, to: pixels.count, by: 4).map { Double(pixels[$0]) + Double(pixels[$0 + 1]) + Double(pixels[$0 + 2]) }
    }
    func difference(_ a: [Double], _ b: [Double]) -> Double {
      zip(a, b).map { abs($0 - $1) }.reduce(0, +) / Double(max(1, a.count)) / 3
    }
    for i in 0..<(panels.count - 1) {
      let a = panels[i], b = panels[i + 1]
      let across = difference(column(a, a.width - 1), column(b, 0))
      let inside = difference(column(a, a.width - 2), column(a, a.width - 1))
      let line = String(format: "%@ seam %d|%d: %.2f across vs %.2f inside a panel (mean 0-255)", label, i + 1, i + 2, across, inside)
      print("  " + line)
      notes.append(line)
      if across > max(6, inside * 4) { problems.append(line + " — seam may not line up") }
    }
  }
}
