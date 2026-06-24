#!/usr/bin/env python3
"""Universal Document Compiler.

Compiles Markdown/HTML into professional A4 PDFs using a themed component system.
Supports various themes: 'professional' (default), 'minimal', 'modern'.
"""

import os
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_DIR = os.path.join(SKILL_DIR, "venv")
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")

THEMES = {
    "professional": {
        "body_font": "'Times New Roman', serif",
        "h_color": "#1a365d",
        "accent_color": "#2b6cb0",
        "bg_color": "#f8fafc",
        "border_color": "#dee2e6",
        "h1_style": "text-align: center; font-size: 26pt; text-transform: uppercase; border-bottom: 2px solid #1a365d; padding-bottom: 10px;",
        "h2_style": "font-size: 18pt; border-left: 5px solid #2b6cb0; padding-left: 12px; background-color: #f8fafc; padding-top: 6px; padding-bottom: 6px;",
    },
    "minimal": {
        "body_font": "Arial, sans-serif",
        "h_color": "#000",
        "accent_color": "#444",
        "bg_color": "#fff",
        "border_color": "#eee",
        "h1_style": "text-align: left; font-size: 24pt; font-weight: bold; margin-bottom: 20px;",
        "h2_style": "font-size: 16pt; font-weight: bold; margin-top: 25px; border-bottom: 1px solid #eee; padding-bottom: 5px;",
    },
    "modern": {
        "body_font": "'Inter', 'Segoe UI', Roboto, sans-serif",
        "h_color": "#4f46e5",
        "accent_color": "#6366f1",
        "bg_color": "#fdfdff",
        "border_color": "#e0e7ff",
        "h1_style": "text-align: center; font-size: 28pt; font-weight: 800; letter-spacing: -1px; margin-bottom: 20px;",
        "h2_style": "font-size: 18pt; font-weight: 700; color: #4f46e5; margin-top: 30px; display: flex; align-items: center;",
    },
}


def bootstrap_venv():
    if not os.path.exists(VENV_DIR):
        subprocess.run(["uv", "venv", VENV_DIR], check=True)
        subprocess.run(
            ["uv", "pip", "install", "--python", VENV_PYTHON, "weasyprint", "markdown"], check=True
        )


def run_dynamic_compilation(content_string, output_name, theme_name="professional"):
    bootstrap_venv()
    t = THEMES.get(theme_name, THEMES["professional"])

    css_styles = f"""
    <style>
        @page {{ size: A4; margin: 20mm 15mm; @bottom-right {{ content: counter(page); font-size: 10pt; color: #555; }} }}
        body {{ font-family: {t["body_font"]}; color: #222; line-height: 1.6; margin: 0; font-size: 12pt; }}

        h1 {{ {t["h1_style"]} color: {t["h_color"]}; }}
        h2 {{ {t["h2_style"]} color: {t["accent_color"]}; }}
        h3 {{ font-size: 14pt; color: #333; margin-top: 20px; font-weight: bold; }}

        .badge-container {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 20px; justify-content: center; }}
        .badge {{ padding: 4px 10px; border-radius: 4px; font-size: 9pt; font-weight: bold; color: white; text-transform: uppercase; font-family: sans-serif; border: 1px solid rgba(0,0,0,0.1); }}
        .badge.orange {{ background-color: #ff6b35; }} .badge.grey {{ background-color: #555; }}
        .badge.purple {{ background-color: #a855f7; }} .badge.blue {{ background-color: #3b82f6; }}
        .badge.green {{ background-color: #10b981; }} .badge.red {{ background-color: #ef4444; }}

        pre {{ background-color: {t["bg_color"]}; border: 1px solid {t["border_color"]}; border-radius: 6px; padding: 12px; font-family: "Cascadia Code", monospace; font-size: 8.5pt; white-space: pre; margin: 15px 0; display: block; }}
        pre code {{ font-family: inherit; font-size: inherit; background: none; padding: 0; border: none; white-space: pre; }}
        code {{ font-family: "Cascadia Code", monospace; background-color: {t["bg_color"]}; padding: 2px 4px; border-radius: 3px; font-size: 0.9em; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            page-break-inside: auto;
        }}
        thead {{
            display: table-header-group;
            background-color: #edf2f7;
            font-weight: bold;
        }}
        tr {{
            page-break-inside: avoid;
        }}
        th, td {{ border: 1px solid {t["border_color"]}; padding: 10px 15px; text-align: left; }}
        th {{ background-color: {t["bg_color"]}; font-weight: bold; }}

        /* ---- Table of Contents ---- */
        .toc {{
            margin: 20px 0;
            padding: 15px;
            background-color: {t["bg_color"]};
            border: 1px solid {t["border_color"]};
            border-radius: 6px;
        }}
        .toc a {{
            display: flex;
            justify-content: space-between;
            text-decoration: none;
            color: {t["accent_color"]};
            font-family: sans-serif;
            margin-bottom: 5px;
        }}
        .toc a::after {{
            content: target-counter(attr(href), page);
        }}

        /* ---- Section Headers (Running Elements) ---- */
        .section-header {{
            position: running(header_main);
            text-align: center;
            font-size: 9pt;
            color: #666;
            font-family: sans-serif;
        }}
        @page {{
            @top-center {{
                content: element(header_main);
            }}
        }}


        blockquote {{ border-left: 4px solid {t["accent_color"]}; margin: 15px 0; padding: 10px 20px; background-color: {t["bg_color"]}; font-style: italic; }}
        hr {{ border: none; border-top: 2px solid {t["border_color"]}; margin: 25px 0; }}
        .urdu-text {{ font-family: "Noto Nastaliq Urdu", sans-serif; font-size: 14pt; text-align: right; direction: rtl; }}
        .page-break {{ page-break-before: always; }}
        p {{ text-align: justify; margin-bottom: 1em; }}
    </style>
    """

    temp_html = os.path.join(SKILL_DIR, "dynamic_temp.html")
    inline_code = f"""import markdown
import os
raw_body = {repr(content_string)}
body_html = markdown.markdown(raw_body, extensions=['tables', 'fenced_code', 'attr_list', 'md_in_html'])
css = {repr(css_styles)}
full_html = '<!DOCTYPE html><html><head><meta charset="UTF-8">' + css + '</head><body>' + body_html + '</body></html>'
with open('{temp_html}', 'w', encoding='utf-8') as f:
    f.write(full_html)
from weasyprint import HTML
HTML('{temp_html}').write_pdf('{output_name}')
"""
    subprocess.run([VENV_PYTHON, "-c", inline_code], check=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    input_path, out_file = sys.argv[1], sys.argv[2]
    theme = sys.argv[3] if len(sys.argv) > 3 else "professional"
    out_file = os.path.abspath(os.path.join(SKILL_DIR, "../../../", os.path.basename(out_file)))
    with open(input_path, encoding="utf-8") as f:
        content = f.read()
    run_dynamic_compilation(content, out_file, theme)
