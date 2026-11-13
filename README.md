# The World Today: Friday 13 November 2026

An entry for make.fun's `news-image-01` competition: one image that sums up the
world's news of Friday 13 November 2026.

## What the program does

`main.py` (Python 3.13, standard library only) reads `entry.png` from this
repository, checks it against the competition limits and writes the same bytes
to `/output/entry.png`. Set `MAKEFUN_OUTPUT_DIR` to write somewhere else:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The checks need no third-party library:

- the first bytes are a PNG or a JPEG signature (the file here is a JPEG; the
  competition keeps the name `entry.png` either way);
- the file is at most 1,048,576 bytes;
- the picture is at most 1024 by 1024 pixels, read from the PNG `IHDR` chunk or
  the JPEG start-of-frame segment.

There is no network access, clock or randomness in it, so every run writes the
same bytes.

## The image

A front-page style infographic, 1024 by 1024 pixels, dated in its header and
footer. One lead story sits across the top; twelve panels follow in a four by
three grid. Each panel has a section tag, a drawn picture, a headline and one
detail line. There are no faces of real people: flags, maps, buildings and
icons carry the stories.

| Section | Headline on the image |
| --- | --- |
| Tech (lead) | Microsoft outage hits the world: Outlook and Teams down for a second day |
| Europe | Ukraine: Europe seeks seat at peace talks |
| Middle East | Iran says it hit US radar in Bahrain; US denies |
| Business | Senate asks Nvidia ex-CEO Huang to testify |
| Asia | India: Assam bus crash kills at least 24 |
| Climate | COP31 climate talks in Antalya |
| Americas | Pope Leo XIV in Peru |
| Africa | Ebola spreads in DR Congo |
| US politics | US Senate: Van Hollen challenges Schumer |
| South Asia | Pakistan army says 74 militants killed |
| Nuclear | IAEA warns on uninspected Iran site |
| Russia | Russia: second car bomb in two days |
| Germany | Germany widens spy agency powers |

## How the stories were selected

The stories were collected on 13 November 2026 from the RSS feeds and front
pages of international outlets. A story went on the image only if it was dated
13 November and carried by at least two outlets. Disputed claims stay
attributed on the image ("Iran says ... US denies", "Pakistan army says",
"Moscow blames Kyiv"). Three figures appear: the Assam toll, given as "at
least 24" as the wire reports agreed; the Pakistan army's own count, attributed
to the army; and the "nearly 1,200" drones Kyiv fired at Russia, as AP and
France 24 reported.

The layout was chosen by comparing candidate images in pairs against the
competition's published judging criteria: the day's specific events first,
then breadth across regions and fields, then readability, faithfulness and
craft. Wider coverage with short labels beat more decorative layouts.

The image was generated with an AI image model from the verified story list,
then fitted to 1024 pixels and saved as a JPEG (922,725 bytes). Stories that
could not be confirmed in a second outlet were left off. The news was checked
again on the evening of 13 November before this repository was committed.

## Sources

AP and Reuters (through ABC News and CBC), BBC, The Guardian, The New York
Times, NPR, Al Jazeera, France 24, Deutsche Welle and Euronews, all as
published on 13 November 2026.

## Licence

MIT, see `LICENSE`.
