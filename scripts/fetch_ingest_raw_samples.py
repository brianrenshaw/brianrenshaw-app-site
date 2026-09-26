#!/usr/bin/env python3
"""Download the website's CC0 RAW collection and verify every source hash.

Usage: python3 scripts/fetch_ingest_raw_samples.py /path/to/Public-RAW
RAW originals remain outside the website repository (about 2 GB).
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('destination', type=Path)
args = parser.parse_args()
manifest = Path(__file__).resolve().parents[1] / 'site/ingest/assets/raw-samples.json'
samples = json.loads(manifest.read_text())['samples']
args.destination.mkdir(parents=True, exist_ok=True)


def fetch(sample):
    assert sample['license'] == 'CC0-1.0'
    filename = sample['filename']
    assert Path(filename).name == filename
    target = args.destination / filename
    if target.exists():
        data = target.read_bytes()
        if hashlib.sha256(data).hexdigest() != sample['sha256']:
            raise ValueError(f'Existing file differs from the original: {target}')
    else:
        url = urllib.parse.quote(sample['url'], safe=':/')
        with urllib.request.urlopen(url, timeout=120) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != sample['sha256']:
            raise ValueError(f'Download checksum mismatch: {filename}')
        # Exclusive creation protects any file created while downloading.
        with target.open('xb') as output:
            output.write(data)
    return filename


with ThreadPoolExecutor(max_workers=4) as pool:
    for filename in pool.map(fetch, samples):
        print(f'Verified {filename}', flush=True)
print(f'{len(samples)} verified RAW files in {args.destination}')
