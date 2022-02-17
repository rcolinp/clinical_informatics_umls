#! /usr/bin/env python

import argparse
import os

import requests
from lxml import html as lhtml
from tqdm import tqdm


def download_umls_full(__doc__):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=None, required=True)
    parser.add_argument("--apikey", default=None, required=True)
    args = parser.parse_args()

    # Obtain a Ticket Granting Ticket - (TGT)
    session = requests.session()
    response = requests.post(
        "https://utslogin.nlm.nih.gov/cas/v1/api-key", data={"apikey": args.apikey}
    )

    # Extract the TGT
    doc = lhtml.fromstring(response.text)
    print(doc)
    TGT = doc.xpath("//form/@action")[0]

    # Obtain a Service Ticket (ST)
    r = session.post(TGT, data={"service": args.url})
    ST = r.text

    print(f"Ticket Granting Ticket - TGT: {TGT}")
    print(f"Service Ticket (ST):          {ST}")
    print(f"URL: {args.url}")

    # Step 3 - Download release file
    r = session.get(f"{args.url}?ticket={ST}", stream=True)
    size = int(r.headers.get("length", 0))
    print(f"Total size {size/1e+9:2.2f} GB")

    with open(os.path.basename(args.url), "wb") as outfile:
        with tqdm(
            total=size / (512 * 1024.0), unit="B", unit_scale=True, unit_divisor=1024
        ) as progress_bar:
            for chunk in r.iter_content(chunk_size=512 * 1024):
                if chunk:  # filter out keep-alive new chunks
                    outfile.write(chunk)
                    progress_bar.update(len(chunk))


if __name__ == "__main__":
    download_umls_full(__doc__)
