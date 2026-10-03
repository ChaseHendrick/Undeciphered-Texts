// Local Apple Vision OCR helper. No image bytes leave this process.
// API reference: https://developer.apple.com/documentation/vision/vnrecognizetextrequest
// Tutorial: https://developer.apple.com/documentation/vision/recognizing-text-in-images

import Foundation
import Vision
import Darwin

func fail(_ message: String, code: Int32 = 1) -> Never {
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(code)
}

guard CommandLine.arguments.count == 2 else {
    fail("usage: vision-ocr LOCAL_IMAGE", code: 2)
}

if #available(macOS 10.15, *) {
    let image = URL(fileURLWithPath: CommandLine.arguments[1])
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["en-US"]
    // Do not replace observed cipher words with dictionary suggestions.
    request.usesLanguageCorrection = false
    request.preferBackgroundProcessing = true
    request.usesCPUOnly = true

    do {
        let handler = VNImageRequestHandler(url: image, options: [:])
        try handler.perform([request])
        let observations = request.results ?? []
        let text = observations.compactMap { $0.topCandidates(1).first?.string }
            .joined(separator: "\n")
        FileHandle.standardOutput.write(Data((text + "\n").utf8))
    } catch {
        fail("Apple Vision could not recognize the image: \(error.localizedDescription)")
    }
} else {
    fail("Apple Vision text recognition requires macOS 10.15 or newer.")
}
