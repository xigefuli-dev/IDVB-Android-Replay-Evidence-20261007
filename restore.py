"""Reconstruct and validate transport ZIPs and member objects using Python stdlib.
Usage: python restore.py REPOSITORY_DIRECTORY OUTPUT_DIRECTORY
ZIP/TAR source container bytes are not part of this deduplicated export.
"""
import base64, hashlib, io, json, pathlib, sys, zipfile
root, output = map(pathlib.Path, sys.argv[1:3])
def read(name):
    return json.loads((root / name).read_text(encoding='utf-8'))
def check(data, size, digest):
    assert len(data) == size and hashlib.sha256(data).hexdigest() == digest
catalog = read('manifest.json')
output.mkdir(parents=True, exist_ok=True)
for pack in catalog['packs']:
    manifest = read(pack['manifest'])
    parts = []
    for chunk in manifest['chunks']:
        encoded = (root / chunk['path']).read_bytes()
        check(encoded, chunk['encodedBytes'], chunk['encodedSha256'])
        decoded = base64.b64decode(b''.join(encoded.split()), validate=True)
        check(decoded, chunk['decodedBytes'], chunk['decodedSha256'])
        parts.append(decoded)
    archive = b''.join(parts)
    check(archive, manifest['archive']['bytes'], manifest['archive']['sha256'])
    expected = {x['path']: x for n in manifest['fileIndexes'] for x in read(n)}
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        assert z.testzip() is None
        for name in z.namelist():
            data = z.read(name)
            item = expected[name]
            check(data, item['bytes'], item['sha256'])
            assert name == 'objects/' + item['sha256']
            target = output / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
print('All transport archives and member hashes verified. Use case indexes to map objects to original archive members.')
