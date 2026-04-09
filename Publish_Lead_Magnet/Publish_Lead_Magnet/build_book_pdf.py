# -*- coding: utf-8 -*-
"""Ghép HTML thành một tài liệu và xuất PDF bằng Playwright (Chromium)."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Cần cài: pip install beautifulsoup4 playwright", file=sys.stderr)
    print("Sau đó: playwright install chromium", file=sys.stderr)
    sys.exit(1)


ROOT = Path(__file__).resolve().parent
OUT_HTML = ROOT / "The-Product-Book-Full-print.html"
OUT_PDF = ROOT / "The-Product-Book-Ban-tom-tat.pdf"

SOURCES: list[tuple[str, str | None]] = [
    ("Book.html", "cover"),
    ("Loi_noi_dau.html", None),
    ("Chapter_01_The_Product_Book.html", None),
    ("Chapter_02_The_Product_Book.html", None),
    ("Chapter_03_The_Product_Book.html", None),
    ("Chapter_04_The_Product_Book.html", None),
    ("Chapter_05_The_Product_Book.html", None),
    ("Chapter_06_The_Product_Book.html", None),
    ("Chapter_07_The_Product_Book.html", None),
    ("Chapter_08_The_Product_Book.html", None),
    ("Chapter_09_The_Product_Book.html", None),
    ("trang_cuoi.html", None),
]


def read_html(name: str) -> str:
    p = ROOT / name
    return p.read_text(encoding="utf-8")


def strip_scripts(soup: BeautifulSoup) -> None:
    for tag in soup.find_all("script"):
        tag.decompose()


def extract_cover_fragment(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    cover = soup.find(id="cover")
    if not cover:
        raise RuntimeError("Không tìm thấy #cover trong Book.html")
    strip_scripts(soup)
    return str(cover)


def extract_body_inner(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    strip_scripts(soup)
    body = soup.body
    if not body:
        raise RuntimeError("Không có <body>")
    inner = "".join(str(c) for c in body.children)
    return inner


PRINT_CSS = """
@media print {
  .no-print { display: none !important; }
  .pdf-section { break-inside: auto; page-break-inside: auto; }
  .pdf-section + .pdf-section { page-break-before: always; }
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
@media screen {
  .pdf-wrap { max-width: 860px; margin: 0 auto; padding: 24px; }
}
"""


def build_merged_html() -> str:
    parts: list[str] = []
    for filename, kind in SOURCES:
        raw = read_html(filename)
        if kind == "cover":
            frag = extract_cover_fragment(raw)
            parts.append(f'<section class="pdf-section pdf-cover">{frag}</section>')
        else:
            inner = extract_body_inner(raw)
            parts.append(f'<section class="pdf-section">{inner}</section>')

    body = "\n".join(parts)
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Product Book — Bản tóm tắt (PDF)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Montserrat:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: Inter, system-ui, sans-serif; background: #e2e8f0; }}
    {PRINT_CSS}
  </style>
</head>
<body>
  <p class="no-print pdf-wrap text-sm text-slate-600 mb-4">Bản xem trước — In hoặc đã xuất file PDF. Đóng thông báo này khi in (ẩn khi in).</p>
  <div class="pdf-wrap space-y-0">
    {body}
  </div>
</body>
</html>
"""


def write_html() -> None:
    html = build_merged_html()
    OUT_HTML.write_text(html, encoding="utf-8")


def export_pdf_playwright() -> None:
    from playwright.sync_api import sync_playwright

    url = OUT_HTML.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=120_000)
        page.wait_for_timeout(2500)
        page.pdf(
            path=str(OUT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "12mm", "right": "12mm", "bottom": "14mm", "left": "12mm"},
        )
        browser.close()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    write_html()
    print("Đã ghi:", OUT_HTML)
    try:
        export_pdf_playwright()
    except Exception as e:
        print("Playwright lỗi:", e, file=sys.stderr)
        print(
            "Đã tạo file HTML in. Mở trong Chrome: The-Product-Book-Full-print.html → Ctrl+P → Lưu dạng PDF.",
            file=sys.stderr,
        )
        sys.exit(1)
    print("Đã xuất PDF:", OUT_PDF, f"({OUT_PDF.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
