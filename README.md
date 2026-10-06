# IDVB Android replay evidence

Public test-account emulator evidence, authorized by the owner. No new replay or algorithm test was executed during export.

Start with probe-manifest.json and probe.b64, then manifest.json. Each pack manifest lists ordered independently encoded base64 chunks. Remove ASCII whitespace, decode each chunk, concatenate decoded bytes, verify archive SHA256, and extract the ZIP. Every ZIP contains objects/<sha256>. Inventory indexes map original archive member paths to objects; reconstruct any member byte-for-byte by copying its object. Original ZIP/TAR container bytes are not published; their sizes and SHA256 are in inventory/sources.json.

88 original frames (54 previous resolution, 34 changed resolution), 84 independently annotated frames, references and intermediate raw buffers, expectations, prior summaries and provenance are preserved. Existing recorded replay outputs are included for investigation, not a new verification claim. Additional selected alignment failure and recognition evidence is included.

Read transport-report.json for locally verified roundtrip and limits.
