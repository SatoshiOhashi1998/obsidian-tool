import os
import re
import yaml
from typing import Optional

VAULT_PATH = r"C:\Users\user\OneDrive\Desktop\Obsidian\Clippings\Twitter"


def extract_author_from_title(title: str) -> Optional[str]:
    match = re.search(r"@(\w+)", title)
    return f"@{match.group(1)}" if match else None


def add_author_link_to_body(body: str, author: str) -> str:
    link = f"[[{author}]]"
    if link not in body:
        return body.rstrip() + f"\n\nLinked author: {link}\n"
    return body


def process_md_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        print(f"⚠️ スキップ（YAMLなし）: {file_path}")
        return

    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"⚠️ スキップ（不正なYAML）: {file_path}")
        return

    yaml_raw = parts[1]
    body = parts[2]
    metadata = yaml.safe_load(yaml_raw) or {}

    title = metadata.get("title", "")
    author = extract_author_from_title(title)

    if author:
        metadata["author"] = author
        body = add_author_link_to_body(body, author)
        print(f"✅ 処理済み: {file_path} → author: {author}")
    else:
        print(f"⚠️ 著者不明: {file_path}")

    # 本文の余計な改行削除
    body = body.lstrip("\n").rstrip("\n")

    new_yaml = yaml.dump(metadata, allow_unicode=True, sort_keys=False).strip()
    new_content = f"---\n{new_yaml}\n---\n{body}"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def process_vault(vault_path):
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                process_md_file(file_path)


def collect_links_by_tag(vault_path=VAULT_PATH, target_tag: str = "オカズ"):
    links = []

    for root, _, files in os.walk(vault_path):
        for file in files:
            if not file.endswith(".md"):
                continue

            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.startswith("---"):
                continue

            parts = content.split("---", 2)
            if len(parts) < 3:
                continue

            yaml_raw = parts[1]
            try:
                metadata = yaml.safe_load(yaml_raw)
            except yaml.YAMLError:
                continue

            if not metadata:
                continue

            tags = metadata.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]

            if not any(target_tag in tag for tag in tags):
                continue

            filename = os.path.splitext(file)[0]
            links.append(f"[[{filename}]]")

    return links


def main():
    process_vault(VAULT_PATH)


if __name__ == "__main__":
    main()
