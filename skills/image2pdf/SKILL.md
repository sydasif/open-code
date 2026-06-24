---
name: Dynamic Image to PDF Converter
description: Automatically transcribes, structures, and compiles images or text drafts into professional, print-ready vector A4 PDFs using WeasyPrint. Universal - handles any content type: badges, code blocks, tables, blockquotes, RTL text, images, and more.
dependencies: python>=3.10, weasyprint>=61.0
---

# Dependency Management

**Important:** Use `uv` for all package and environment management. Do NOT use `pip` directly. Refer to global standards in `~/.claude/docs/tooling/package-management.md`.

# Supported Markdown + HTML Features

The compiler supports a rich set of Markdown extensions and raw HTML:

| Feature           | Syntax              | Example                                            |
| ----------------- | ------------------- | -------------------------------------------------- |
| Badges/Chips      | Raw HTML `<span>`   | `<span class="badge orange">REACT</span>`          |
| Code blocks       | Fenced code         | ` ```python ... ``` `                              |
| Project trees     | Fenced code (text)  | ` ```text ... ``` `                                |
| Tables            | Markdown pipes      | `\| Col1 \| Col2 \|`                               |
| Blockquotes       | `>` prefix          | `> quoted text`                                    |
| RTL text          | HTML wrapper        | `<div class="urdu-text">...</div>`                 |
| Images            | Markdown/HTML       | `![alt](url)` or `<img>`                           |
| Horizontal rules  | `---`               | `---`                                              |
| Lists             | `-` or `1.`         | Unordered / ordered                                |
| Table of Contents | HTML `<a>` + `.toc` | `<div class="toc"><a href="#sec1">Title</a></div>` |
| Repeating Headers | `<thead>` in HTML   | `<table><thead>...</thead></table>`                |
| Section Headers   | `.section-header`   | `<div class="section-header">My Section</div>`     |

**Available badge classes:** `orange`, `grey`, `purple`, `pink`, `blue-purple`, `blue`, `light-blue`, `green`, `red`, `yellow`, `teal`, `indigo`, `cyan`, `rose`, `slate`, `amber`, `lime`, `emerald`, `sky`, `violet`, `fuchsia`

**Utility classes:** `text-center`, `text-left`, `text-right`, `text-sm`, `text-lg`, `mt-0`, `mb-0`, `page-break`

# Process Workflow

When a user provides images or text to convert into a professional PDF, execute this sequence:

1. **Analysis & Structure Extraction**
   - Read and extract text from the images.
   - **Visual Audit**: Analyze the source image for non-text elements:
     - **Badges/Chips**: Identify labels and assign the closest color class.
     - **Code Blocks/Trees**: Identify project structures or code snippets.
     - **Tables**: Identify tabular data with headers and rows.
     - **Layout**: Note specific alignments (centered headers, justified text).
   - Separate content logically into sections using Markdown headers (`# Title`), metadata, and bullet points.
   - For multilingual content (e.g., Urdu), wrap in `<div class="urdu-text">` for RTL support.

2. **Payload Generation**
   - Write the extracted content into a `.md` file using Markdown + inline HTML where needed.
   - **Styling rules**:
     - Badges: `<div class="badge-container"><span class="badge color">TEXT</span></div>`
     - Code/trees: Use fenced code blocks (`text ... `) to preserve formatting.
     - Tables: Use standard Markdown pipe syntax.
     - Blockquotes: Use `>` prefix.
   - Call: `python scripts/compile_pdf.py <input_file.md> <output_file.pdf>`

3. **Verification & Iterative Refinement**
   - Confirm the output is a professional vector PDF.
   - Check for: tree alignment, header spacing, badge colors, table formatting.
   - If layout issues exist, refine the CSS in `scripts/compile_pdf.py` and re-compile.

# Customization

To add new badge colors or utility classes, edit `scripts/compile_pdf.py` and add CSS rules under the `/* ---- Badges ---- */` or `/* ---- Utility ---- */` sections. The compiler auto-bootstraps its venv on first run.
