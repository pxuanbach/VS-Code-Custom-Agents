#!/usr/bin/env python3
"""
Wiki CLI Tool for Material Writer Wiki Skill
Manages wiki index, search, and cross-references.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

WIKI_DIR = Path("wiki")
SCHEMA_PATH = Path(__file__).parent.parent / "references" / "SCHEMA.md"


def ensure_wiki_dir():
    """Ensure wiki directory exists."""
    if not WIKI_DIR.exists():
        print("Error: wiki/ directory not found. Run 'wiki init' first.", file=sys.stderr)
        sys.exit(1)


def get_feature_id_from_path(file_path: Path) -> Optional[str]:
    """Parse YYYY-MM-NNN from parent folder name."""
    parent_name = file_path.parent.name
    match = re.match(r"(\d{4}-\d{2}-\d{3}-[\w-]+)", parent_name)
    return match.group(1) if match else None


def get_doc_type_from_filename(filename: str) -> str:
    """Detect document type from filename."""
    filename_lower = filename.lower()
    if "-prd" in filename_lower or filename_lower.endswith("-prd.md"):
        return "prd"
    if "-arch" in filename_lower or filename_lower.endswith("-arch.md"):
        return "arch"
    if "-plan" in filename_lower or filename_lower.endswith("-plan.md"):
        return "plan"
    if "-report" in filename_lower or filename_lower.endswith("-report.md"):
        return "report"
    if "-notes" in filename_lower or filename_lower.endswith("-notes.md"):
        return "notes"
    return "doc"


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from markdown content. Returns (frontmatter_dict, body)."""
    if not content.startswith("---"):
        return {}, content
    
    end_match = content.find("\n---", 3)
    if end_match == -1:
        return {}, content
    
    fm_text = content[4:end_match]
    body = content[end_match + 4:].lstrip("\n")
    
    fm = {}
    for line in fm_text.strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):
                # Simple list parsing
                items = value[1:-1].split(",")
                fm[key] = [item.strip() for item in items]
            elif value.startswith("-"):
                # List format
                fm[key] = [v.strip() for v in fm_text.split("\n") if v.strip().startswith("-")]
            else:
                fm[key] = value
    return fm, body


def extract_summary(content: str, max_length: int = 200) -> str:
    """Extract summary: first non-empty line after frontmatter, stripped of markdown."""
    fm, body = extract_frontmatter(content)
    
    if "summary" in fm:
        return fm["summary"][:max_length]
    
    lines = body.split("\n")
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("!"):
            # Strip common markdown
            line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)  # [text](url) -> text
            line = re.sub(r"\*\*([^*]+)\*\*", r"\1", line)  # **bold** -> text
            line = re.sub(r"\*([^*]+)\*", r"\1", line)  # *italic* -> text
            line = re.sub(r"`([^`]+)`", r"\1", line)  # `code` -> text
            return line[:max_length]
    return ""


def extract_title(content: str, filename: str = "") -> str:
    """Extract title from frontmatter or first heading."""
    fm, body = extract_frontmatter(content)
    
    if "title" in fm:
        return fm["title"]
    
    # First heading
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    # Filename-based
    if filename:
        name = Path(filename).stem
        name = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)  # Remove date prefix
        name = re.sub(r"-[a-z]+$", "", name)  # Remove type suffix
        return name.replace("-", " ").title()
    
    return "Untitled"


def load_master_index() -> dict:
    """Load master wiki/index.json."""
    ensure_wiki_dir()
    index_path = WIKI_DIR / "index.json"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": "1.0", "generated_at": "", "features": [], "topics": [], "documents": []}


def save_master_index(index: dict):
    """Save master wiki/index.json."""
    index["generated_at"] = datetime.utcnow().isoformat() + "Z"
    with open(WIKI_DIR / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


def load_feature_index(feature_id: str) -> dict:
    """Load feature-local index.json."""
    for feature_dir in (WIKI_DIR / "features").glob("*"):
        if feature_dir.name == feature_id:
            idx_path = feature_dir / "index.json"
            if idx_path.exists():
                with open(idx_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            break
    return {"feature": {"id": feature_id, "title": "", "created_at": "", "updated_at": ""}, "documents": []}


def save_feature_index(feature_id: str, feature_index: dict):
    """Save feature-local index.json."""
    feature_dir = WIKI_DIR / "features" / feature_id
    feature_dir.mkdir(parents=True, exist_ok=True)
    with open(feature_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(feature_index, f, indent=2)


def cmd_init():
    """Initialize wiki structure."""
    if WIKI_DIR.exists():
        print(f"Warning: {WIKI_DIR}/ already exists. Skipping init.")
        return
    
    print(f"Creating {WIKI_DIR}/ structure...")
    
    WIKI_DIR.mkdir(parents=True)
    (WIKI_DIR / "features").mkdir()
    (WIKI_DIR / "topics").mkdir()
    
    # Copy SCHEMA.md from references
    if SCHEMA_PATH.exists():
        import shutil
        shutil.copy(SCHEMA_PATH, WIKI_DIR / "SCHEMA.md")
    
    # Create empty index.json
    master_index = {
        "version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "features": [],
        "topics": [],
        "documents": []
    }
    save_master_index(master_index)
    
    # Create empty log.md
    with open(WIKI_DIR / "log.md", "w", encoding="utf-8") as f:
        f.write("# Wiki Log\n\n")
        f.write("Append-only chronological log of wiki operations.\n\n")
        f.write("Format: `## [YYYY-MM-DD] <action> | <title>`\n\n")
    
    print(f"Wiki initialized at {WIKI_DIR}/")
    print("Run 'wiki add <file>' to add documents to the wiki.")


def cmd_add(file_path: str):
    """Add a document to the wiki index."""
    ensure_wiki_dir()
    
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Detect feature
    feature_id = get_feature_id_from_path(path)
    if not feature_id:
        print(f"Error: Cannot determine feature ID from path: {path}", file=sys.stderr)
        print("Expected path like: wiki/features/YYYY-MM-NNN-slug/doc-type.md")
        sys.exit(1)
    
    # Ensure feature dir exists
    feature_dir = WIKI_DIR / "features" / feature_id
    feature_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy file to wiki if not already there
    wiki_dest = feature_dir / path.name
    if str(path.resolve()) != str(wiki_dest.resolve()):
        import shutil
        shutil.copy(path, wiki_dest)
        path = wiki_dest
    
    # Parse existing or generate frontmatter
    fm, _ = extract_frontmatter(content)
    
    if not fm:
        # Generate frontmatter
        today = datetime.now().strftime("%Y-%m-%d")
        title = extract_title(content, path.name)
        summary = extract_summary(content)
        doc_type = get_doc_type_from_filename(path.name)
        
        fm = {
            "id": f"{feature_id}/{doc_type}",
            "type": doc_type,
            "title": title,
            "summary": summary,
            "tags": [],
            "status": "draft",
            "created_at": today,
            "updated_at": today,
            "related": []
        }
        
        # Prepend frontmatter
        fm_text = "---\n"
        for key, value in fm.items():
            if isinstance(value, list):
                fm_text += f"{key}: [{', '.join(value)}]\n"
            else:
                fm_text += f"{key}: {value}\n"
        fm_text += "---\n\n"
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(fm_text + content)
        
        content = fm_text + content
    
    # Update feature-local index
    feature_index = load_feature_index(feature_id)
    
    doc_entry = {
        "id": fm.get("id", f"{feature_id}/{get_doc_type_from_filename(path.name)}"),
        "path": str(path.relative_to(WIKI_DIR)),
        "type": fm.get("type", get_doc_type_from_filename(path.name)),
        "title": fm.get("title", extract_title(content, path.name)),
        "summary": fm.get("summary", extract_summary(content)),
        "tags": fm.get("tags", []),
        "status": fm.get("status", "draft"),
        "created_at": fm.get("created_at", datetime.now().strftime("%Y-%m-%d")),
        "updated_at": fm.get("updated_at", datetime.now().strftime("%Y-%m-%d")),
        "related": fm.get("related", [])
    }
    
    # Update or add document entry
    doc_found = False
    for i, doc in enumerate(feature_index.get("documents", [])):
        if doc["id"] == doc_entry["id"]:
            feature_index["documents"][i] = doc_entry
            doc_found = True
            break
    
    if not doc_found:
        feature_index.setdefault("documents", []).append(doc_entry)
    
    feature_index["feature"] = {
        "id": feature_id,
        "title": fm.get("title", feature_id),
        "created_at": fm.get("created_at", datetime.now().strftime("%Y-%m-%d")),
        "updated_at": datetime.now().strftime("%Y-%m-%d")
    }
    
    save_feature_index(feature_id, feature_index)
    
    # Update master index
    master_index = load_master_index()
    
    # Add to features if new
    feature_found = any(f["id"] == feature_id for f in master_index["features"])
    if not feature_found:
        master_index["features"].append({
            "id": feature_id,
            "title": feature_index["feature"]["title"],
            "path": f"features/{feature_id}",
            "created_at": feature_index["feature"]["created_at"],
            "updated_at": feature_index["feature"]["updated_at"],
            "documents": [path.name for path in feature_dir.glob("*.md") if path.name != "index.json"]
        })
    
    # Add to documents
    doc_found = False
    for i, doc in enumerate(master_index["documents"]):
        if doc["id"] == doc_entry["id"]:
            master_index["documents"][i] = doc_entry
            doc_found = True
            break
    
    if not doc_found:
        master_index["documents"].append(doc_entry)
    
    save_master_index(master_index)
    
    # Append to log
    today = datetime.now().strftime("%Y-%m-%d")
    with open(WIKI_DIR / "log.md", "a", encoding="utf-8") as f:
        f.write(f"## [{today}] ingest | {doc_entry['title']}\n")
    
    print(f"Added: {doc_entry['title']} ({doc_entry['id']})")


def cmd_list(type_filter: Optional[str] = None, tag_filter: Optional[str] = None,
             status_filter: Optional[str] = None, feature_filter: Optional[str] = None):
    """List documents from the wiki index."""
    ensure_wiki_dir()
    
    index = load_master_index()
    results = index.get("documents", [])
    
    if type_filter:
        results = [d for d in results if d.get("type") == type_filter]
    if tag_filter:
        results = [d for d in results if tag_filter in d.get("tags", [])]
    if status_filter:
        results = [d for d in results if d.get("status") == status_filter]
    if feature_filter:
        results = [d for d in results if d.get("id", "").startswith(feature_filter)]
    
    if not results:
        print("No documents found matching criteria.")
        return
    
    for doc in results:
        print(f"[{doc.get('type', '?')}] {doc.get('title', 'Untitled')}")
        print(f"  ID: {doc.get('id')}")
        print(f"  Path: {doc.get('path')}")
        print(f"  Status: {doc.get('status', 'unknown')}")
        if doc.get("tags"):
            print(f"  Tags: {', '.join(doc['tags'])}")
        print()


def cmd_search(query: str):
    """Search documents by query string."""
    ensure_wiki_dir()
    
    index = load_master_index()
    query_lower = query.lower()
    
    results = []
    for doc in index.get("documents", []):
        title = doc.get("title", "").lower()
        summary = doc.get("summary", "").lower()
        tags = " ".join(doc.get("tags", [])).lower()
        
        if query_lower in title or query_lower in summary or query_lower in tags:
            results.append(doc)
    
    if not results:
        print(f"No documents found matching: {query}")
        return
    
    print(f"Found {len(results)} result(s) for: {query}\n")
    for doc in results:
        print(f"[{doc.get('type', '?')}] {doc.get('title', 'Untitled')}")
        print(f"  {doc.get('summary', 'No summary')[:100]}...")
        print(f"  Path: {doc.get('path')}")
        print()


def cmd_related(file_path: str):
    """Find related documents."""
    ensure_wiki_dir()
    
    path = Path(file_path)
    if not path.exists():
        # Try relative to wiki
        path = WIKI_DIR / file_path
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    fm, _ = extract_frontmatter(content)
    related_paths = fm.get("related", [])
    
    if not related_paths:
        print("No related documents found.")
        return
    
    print(f"Related documents for: {fm.get('title', path.name)}\n")
    for rel_path in related_paths:
        rel_abs = WIKI_DIR / rel_path if not Path(rel_path).is_absolute() else Path(rel_path)
        if rel_abs.exists():
            with open(rel_abs, "r", encoding="utf-8") as f:
                rel_content = f.read()
            rel_fm, _ = extract_frontmatter(rel_content)
            print(f"- {rel_fm.get('title', rel_path)}")
            print(f"  [{rel_fm.get('type', 'doc')}] {rel_path}")
        else:
            print(f"- [MISSING] {rel_path}")
    print()


def cmd_reindex():
    """Rebuild master index from all feature-local indexes."""
    ensure_wiki_dir()
    
    master_index = {
        "version": "1.0",
        "generated_at": "",
        "features": [],
        "topics": []
    }
    all_docs = []
    
    features_dir = WIKI_DIR / "features"
    if not features_dir.exists():
        print("No features directory found.")
        save_master_index(master_index)
        print("Reindex complete (empty).")
        return
    
    for feature_dir in features_dir.iterdir():
        if not feature_dir.is_dir():
            continue
        
        idx_path = feature_dir / "index.json"
        if not idx_path.exists():
            continue
        
        with open(idx_path, "r", encoding="utf-8") as f:
            feature_index = json.load(f)
        
        feature_info = feature_index.get("feature", {})
        docs = feature_index.get("documents", [])
        
        master_index["features"].append({
            "id": feature_info.get("id", feature_dir.name),
            "title": feature_info.get("title", feature_dir.name),
            "path": f"features/{feature_dir.name}",
            "created_at": feature_info.get("created_at", ""),
            "updated_at": feature_info.get("updated_at", ""),
            "documents": [d["path"].split("/")[-1] for d in docs]
        })
        
        all_docs.extend(docs)
    
    # Load existing topics
    topics_dir = WIKI_DIR / "topics"
    topics = []
    if topics_dir.exists():
        for topic_file in topics_dir.glob("*.md"):
            with open(topic_file, "r", encoding="utf-8") as f:
                content = f.read()
            fm, _ = extract_frontmatter(content)
            topics.append({
                "id": topic_file.stem,
                "title": fm.get("title", topic_file.stem),
                "path": f"topics/{topic_file.name}",
                "created_at": fm.get("created_at", ""),
                "updated_at": fm.get("updated_at", ""),
                "tags": fm.get("tags", []),
                "related": fm.get("related", [])
            })
    
    master_index["topics"] = topics
    master_index["documents"] = all_docs
    save_master_index(master_index)
    
    print(f"Reindex complete: {len(master_index['features'])} features, {len(all_docs)} documents, {len(topics)} topics.")


def main():
    parser = argparse.ArgumentParser(description="Material Writer Wiki CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # init
    subparsers.add_parser("init", help="Initialize wiki structure")
    
    # add
    add_parser = subparsers.add_parser("add", help="Add document to wiki")
    add_parser.add_argument("file", help="Path to document to add")
    
    # list
    list_parser = subparsers.add_parser("list", help="List documents")
    list_parser.add_argument("--type", "-t", help="Filter by document type")
    list_parser.add_argument("--tag", help="Filter by tag")
    list_parser.add_argument("--status", "-s", help="Filter by status")
    list_parser.add_argument("--feature", "-f", help="Filter by feature ID")
    
    # search
    search_parser = subparsers.add_parser("search", help="Search documents")
    search_parser.add_argument("query", help="Search query")
    
    # related
    related_parser = subparsers.add_parser("related", help="Find related documents")
    related_parser.add_argument("file", help="Path to document")
    
    # reindex
    subparsers.add_parser("reindex", help="Rebuild master index from features")
    
    args = parser.parse_args()
    
    if args.command == "init":
        cmd_init()
    elif args.command == "add":
        cmd_add(args.file)
    elif args.command == "list":
        cmd_list(args.type, args.tag, args.status, args.feature)
    elif args.command == "search":
        cmd_search(args.query)
    elif args.command == "related":
        cmd_related(args.file)
    elif args.command == "reindex":
        cmd_reindex()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
