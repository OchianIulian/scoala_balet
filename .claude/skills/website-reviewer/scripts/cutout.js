// osascript -l JavaScript cutout.js <in> <out.png> [idx,idx]
// Lifts the foreground subject(s) with Apple's Vision framework and writes a
// transparent PNG cropped to the subject.
ObjC.import('Foundation'); ObjC.import('Vision'); ObjC.import('CoreImage'); ObjC.import('AppKit');
function run(argv) {
  const url = $.NSURL.fileURLWithPath(argv[0]);
  const handler = $.VNImageRequestHandler.alloc.initWithURLOptions(url, $({}));
  const req = $.VNGenerateForegroundInstanceMaskRequest.alloc.init;
  const err = Ref();
  if (!handler.performRequestsError($([req]), err)) return 'perform failed';
  const obs = req.results.firstObject;
  if (!obs || obs.isNil()) return 'no subject';
  let inst = obs.allInstances;
  if (argv[2]) { const s = $.NSMutableIndexSet.indexSet; argv[2].split(',').forEach(i => s.addIndex(parseInt(i))); inst = s; }
  const buf = obs.generateMaskedImageOfInstancesFromRequestHandlerCroppedToInstancesExtentError(inst, handler, true, err);
  const ci = $.CIImage.imageWithCVPixelBuffer(buf);
  const rep = $.NSBitmapImageRep.alloc.initWithCIImage(ci);
  const png = rep.representationUsingTypeProperties($.NSBitmapImageFileTypePNG, $({}));
  png.writeToFileAtomically(argv[1], true);
  return 'instances ' + obs.allInstances.count + ' -> ' + rep.pixelsWide + 'x' + rep.pixelsHigh;
}
