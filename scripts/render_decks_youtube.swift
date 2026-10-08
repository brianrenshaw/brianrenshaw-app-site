// Native Decks website example. Run in a Swift 6 executable package targeting macOS 15,
// depending on the local Packages/IngestSocialKit package (source commit in asset manifest).
// Arguments: source JPEG path, isolated output directory. Writes PNG and project JSON.
import Foundation
import CoreGraphics
import ImageIO
import IngestSocialKit
@main struct Render {
 static func main() async throws {
  let out=URL(fileURLWithPath:CommandLine.arguments[2]);try FileManager.default.createDirectory(at:out,withIntermediateDirectories:true)
  let store=try SocialStore(root:out.appendingPathComponent("DemoStore"))
  let source=try store.assets.importImage(URL(fileURLWithPath:CommandLine.arguments[1]))
  var project=SocialProject();project.sources=[source];project.frames=[SocialFrame(content:[SocialContent(sourceID:source.id)])]
  let start=SocialStart.basics.first { $0.photos == 1 && !$0.details }!
  var choices=SocialStartChoices(size:.other(SocialRatio(16,9)),background:.blur,details:SocialStartChoices.defaultDetails)
  choices.frameAppearance = .plain;choices.frameWidth=0.006;choices.frameColor = .white
  try start.template(choices).apply(to:&project)
  project.style.fit = .fit
  project.export.photoWidth=1920
  let renderer=SocialRenderService(assets:store.assets)
  let image=try await renderer.render(project:project,frameID:project.frames[0].id,previewWidth:nil)
  let url=out.appendingPathComponent("youtube-autumn-soft.png")
  let writer=CGImageDestinationCreateWithURL(url as CFURL,"public.png" as CFString,1,nil)!
  CGImageDestinationAddImage(writer,image,nil);guard CGImageDestinationFinalize(writer) else {throw SocialError("PNG failed")}
  try SocialCoding.encode(project).write(to:out.appendingPathComponent("youtube-autumn-soft.json"))
  print("Rendered",image.width,image.height)
 }
}
