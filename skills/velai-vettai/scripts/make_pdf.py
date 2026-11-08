#!/usr/bin/env python3
"""Render an HTML resume to PDF with Playwright.
Usage: make_pdf.py in.html out.pdf [--format A4|Letter]
Needs: pip install playwright && playwright install chromium"""
import argparse
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("src"); p.add_argument("dst")
p.add_argument("--format", default="A4", choices=["A4", "Letter"])
a = p.parse_args()
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto(Path(a.src).resolve().as_uri())
    pg.pdf(path=a.dst, format=a.format, print_background=True)
    b.close()
print("wrote", a.dst)
