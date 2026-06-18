---
name: new-jysk-pptx
description: Use this skill whenever the user wants to generate, edit, format, or work with JYSK-branded PowerPoint (PPTX) presentations. This skill enforces the official JYSK PowerPoint brand guidelines (Verdana font, Dark Grey color #565655, sentence case for headlines, and specific layout rules). Make sure to use this skill proactively for any JYSK presentation request.
---

# JYSK PowerPoint (PPTX) Skill

A specialized skill for programmatically generating and working with PowerPoint presentations that strictly adhere to the official JYSK PowerPoint Guidelines and brand manual.

## Core Brand Guidelines & Constraints

Always adhere to these official JYSK PowerPoint styling rules:

1.  **Typography**:
    *   **Font**: The default corporate font is **Verdana**. It must be used for all slide texts, titles, sub-headlines, and body copy.
    *   **Text Casing**: Headlines must always be written in **Sentence case** (*Uppercase* letter at the start of a sentence, and otherwise *lowercase*). Do not use ALL CAPS for headlines, unless referring to an official exception brand (e.g., *WELLPUR*, *KRONBORG*, *JYSK*).
2.  **Color Palette**:
    *   **Main Font Color**: **Dark Grey** (RGB: `86, 86, 85` / Hex: `#565655`).
3.  **Slide Master Layout Formatting Rules**:
    *   **Title Slide**: Headline size `28` (Bold), Sub-headline size `18`.
    *   **Agenda Slide**: Headline size `40` (Bold). Body size `20` (Bullet indents are reduced by `2pt` for each level, down to a minimum of `12pt` at Level 5).
    *   **Standard Slide**: Headline size `28` (Bold). Body size `20` (Bullet indents are reduced by `2pt` for each level, down to a minimum of `12pt` at Level 5).
    *   **Breakers / Section Dividers**: Headline size `28` (Bold), Sub-headline size `18`.

## Resources & Assets

The skill bundles official, clean PowerPoint templates inside the `assets/` directory:
*   **Indoor Template**: `/Users/mojoaar/AI/skills/new-jysk-pptx/assets/jysk_indoor.pptx` (Default, represents latest Indoor master)
*   **Outdoor Template**: `/Users/mojoaar/AI/skills/new-jysk-pptx/assets/jysk_outdoor.pptx` (Represents latest Outdoor master)

*Note: These files contain pre-configured master slides with the JYSK logo, correct aspect ratios (16:9), and background artwork. Slide generation must always build on top of these templates rather than starting from blank slides.*

## Slide Layout Selection

Use the matching slide master layouts:
*   `Title page` for the deck cover.
*   `Agenda ` for index/agenda slides.
*   `Standard slide` for standard text and bullets.
*   `1_Breaker Large Placeholder White` or `1_Breaker Large Placeholder Blue` for section breakers.

---

## Workflow: How to Generate JYSK Presentations

When requested to create or update a JYSK presentation, do not write a complex slide builder from scratch. Instead, utilize the pre-built Python generator tool.

### Method 1: Using JSON Configuration (Recommended)

Write a structured JSON configuration of your slides and call the generator script.

#### 1. Define the Slide JSON (`slides.json`)
```json
{
  "template": "indoor", 
  "output_path": "output.pptx",
  "slides": [
    {
      "type": "title",
      "title": "My Title Slide",
      "subtitle": "Created with new-jysk-pptx skill"
    },
    {
      "type": "agenda",
      "title": "Agenda",
      "items": [
        "First Section",
        "Second Section"
      ]
    },
    {
      "type": "standard",
      "title": "My Content Slide",
      "body": [
        "First-level bullet point",
        "  - Second-level indent point (automatically uses size 18)",
        "  - Another sub-point",
        "Back to top-level bullet point"
      ]
    },
    {
      "type": "breaker",
      "title": "Section Divider Title",
      "subtitle": "Optional subtitle"
    }
  ]
}
```

#### 2. Run the Generator Command
Run the Python script via Bash:
```bash
python3 /Users/mojoaar/AI/skills/new-jysk-pptx/scripts/generate_jysk_pptx.py --input /path/to/slides.json
```

### Method 2: Using the Fast CLI Command (for simple decks)
For simple presentations, you can invoke the script directly from bash without writing a JSON file:
```bash
python3 /Users/mojoaar/AI/skills/new-jysk-pptx/scripts/generate_jysk_pptx.py \
  --template "indoor" \
  --output "simple_deck.pptx" \
  --title "My Simple Title" \
  --subtitle "Simple Subtitle" \
  --slides "First Slide Title|Bullet A|Bullet B;Second Slide Title|  - Sub-Bullet 1|  - Sub-Bullet 2"
```

## Best Practices
*   Keep bullet points concise. Long blocks of text will overflow.
*   Always structure hierarchical bullets using exactly two spaces (`  `) for nested indentation. The python helper will automatically parse this and format the font size (e.g. 20pt -> 18pt -> 16pt) per the brand guidelines.
*   Ensure that all titles use sentence-casing to match JYSK standards.

## Syncing & Updating JYSK Templates
Since JYSK updates its PowerPoint templates twice a year (Indoor in mid-August, Outdoor in mid-February), a script is included to automatically verify, compare, and pull down the latest official masters from JYSK Blue Line:

*   **Check for new versions online**:
    ```bash
    python3 /Users/mojoaar/AI/skills/new-jysk-pptx/scripts/update_templates.py --check
    ```
*   **Sync and download latest versions**:
    ```bash
    python3 /Users/mojoaar/AI/skills/new-jysk-pptx/scripts/update_templates.py --update
    ```
*   **Force full re-download of templates**:
    ```bash
    python3 /Users/mojoaar/AI/skills/new-jysk-pptx/scripts/update_templates.py --force
    ```
