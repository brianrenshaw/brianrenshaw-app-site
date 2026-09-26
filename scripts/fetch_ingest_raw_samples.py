#!/usr/bin/env python3
"""Rebuild or verify Ingest's licensed demonstration RAW collection (about 3 GB).

Usage: python3 scripts/fetch_ingest_raw_samples.py /path/to/RAW-originals
Files are downloaded from their original sources, not hosted by this website.
See each manifest entry's licenseUrl and originalFilename for credits and terms.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('destination', type=Path)
args = parser.parse_args()
manifest = Path(__file__).resolve().parents[1] / 'site/ingest/assets/raw-samples.json'
samples = json.loads(manifest.read_text())['samples']
args.destination.mkdir(parents=True, exist_ok=True)
licenses = {
    'CC0-1.0': None,
    'Signature-Edits-Free-RAW': 'https://www.signatureedits.com/free-raw-license-terms/',
}


def digest(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def fetch(sample):
    license_id = sample['license']
    if license_id not in licenses:
        raise ValueError(f'Unreviewed license: {license_id}')
    if licenses[license_id] and sample.get('licenseUrl') != licenses[license_id]:
        raise ValueError(f'Missing license provenance: {sample["filename"]}')
    filename = sample['filename']
    if Path(filename).name != filename or filename in ('.', '..'):
        raise ValueError(f'Invalid filename: {filename}')
    target = args.destination / filename
    if target.exists():
        if digest(target) != sample['sha256']:
            raise ValueError(f'Existing file differs from the original: {target}')
        return filename
    # Download outside the final path: failures never leave an apparently valid RAW.
    with tempfile.TemporaryDirectory(prefix='.ingest-raw-', dir=args.destination) as temp:
        download = Path(temp) / filename
        subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                        '--retry', '2', '--max-time', '240', '--proto', '=https',
                        '--proto-redir', '=https', sample['url'], '--output', str(download)], check=True)
        if digest(download) != sample['sha256']:
            raise ValueError(f'Download checksum mismatch: {filename}')
        # An exclusive hard link publishes atomically and protects concurrent files.
        target.hardlink_to(download)
    return filename


with ThreadPoolExecutor(max_workers=4) as pool:
    for filename in pool.map(fetch, samples):
        print(f'Verified {filename}', flush=True)
print(f'{len(samples)} verified RAW files in {args.destination}')
