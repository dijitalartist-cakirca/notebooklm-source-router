# YouTube research: recommendations and exact quotes

Illustrative fixture, not a report about a real video.

**Request:** “Using this video in my notebook, identify the retry advice. Give an exact quote and timestamp; retrieve at most 900 tokens.”

1. Confirm the provided notebook/video identity and adapter capabilities. The notebook contains the supplied YouTube source; query that source rather than importing or uploading anything automatically.
2. Allocate roughly 600 tokens to discovery and 300 to verification. Ask for the retry recommendation and its locator, not the full transcript.
3. Fixture response: “Use exponential backoff”; no timestamp or resolvable passage. Record this as an unverified lead, not an exact quote. One narrower query may seek the missing locator only if budget remains.
4. Use a permitted original video or timestamped transcript to verify the exact words and alignment. If a transcript excerpt at 02:14 actually says “Increase the delay after each failed attempt,” quote those inspected words and cite the real video URL with its verified timestamp. Do not substitute the notebook paraphrase inside quotation marks.
5. If the video/transcript is inaccessible, answer: “The notebook summary recommends exponential backoff. I could not verify an exact quotation or timestamp.” Keep the recommendation attributed to the notebook summary.

For a question about an on-screen chart, transcript text alone is insufficient; inspect the visual evidence or report that gap. Caption availability, source eligibility and adapter support must be checked at runtime. Do not promise every video can be imported or queried. Unsupported/private/deleted videos and missing captions require permitted original-source alternatives, not repeated import attempts.

**Pass criteria:** no invented timestamp/quote; video-specific scope disclosed; fallback shares the 900-token cap; no complete transcript loading; unavailable evidence stays unavailable.
