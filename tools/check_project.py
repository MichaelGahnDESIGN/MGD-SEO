"""Prüft Syntax, relative Dokumentlinks und Versionskonsistenz ohne Fremdpakete."""
import ast
import json
from pathlib import Path
import re
import sys

root=Path(__file__).resolve().parents[1]
errors=[]
for path in root.rglob("*.py"):
    if ".tmp" not in path.parts:
        try: ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
        except SyntaxError as exc: errors.append(str(exc))
for path in root.rglob("*.md"):
    if ".tmp" in path.parts: continue
    for link in re.findall(r"\]\(([^)]+)\)",path.read_text(encoding="utf-8")):
        if "://" in link or link.startswith("#"): continue
        target=link.split("#",1)[0]
        if target and not (path.parent/target).exists(): errors.append(f"Fehlender Link: {path.relative_to(root)} → {target}")
version=(root/"VERSION").read_text().strip()
if not re.search(r'^version = "'+re.escape(version)+'"$',(root/"pyproject.toml").read_text(),re.M): errors.append("Paketversion weicht ab")
if new_version := re.search(r'"tool_version": "([^"]+)"',(root/"mgd_seo/crawl.py").read_text()):
    if new_version.group(1)!=version: errors.append("Berichtsversion weicht ab")
if version not in (root/"CHANGELOG.md").read_text(): errors.append("Changelog-Version fehlt")
for error in errors: print(error,file=sys.stderr)
print("Projektprüfung: " + ("FEHLER" if errors else "OK"))
raise SystemExit(bool(errors))
