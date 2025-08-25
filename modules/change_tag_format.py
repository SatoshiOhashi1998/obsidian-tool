"""
tag列挙のフォーマットを半角スペースからカンマ切りに変更する
"""

import os
import re
import yaml

# ==== 設定 ====
# VAULT_PATH = r"C:\Users\user\OneDrive\Desktop\container\Obsidian\Clippings"  # Vault のパス
VAULT_PATH = r"C:\Users\user\OneDrive\Desktop\Obsidian"  # Vault のパス


def fix_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # frontmatterを抽出
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        # frontmatter がない場合も本文の空行だけ削除
        new_body = content.lstrip("\n").rstrip("\n")
        if new_body != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_body)
            print(f"[Cleaned] {file_path} (no frontmatter)")
        return

    frontmatter_raw, body = match.groups()
    try:
        fm = yaml.safe_load(frontmatter_raw)
    except Exception as e:
        print(f"[YAML parse error] {file_path}: {e}")
        return

    if not isinstance(fm, dict):
        return

    tags = fm.get("tags", None)

    # --- タグ修正 ---
    changed_tags = False
    if tags:
        if isinstance(tags, str):
            tags = [tags]

        if isinstance(tags, list):
            fixed_tags = []
            for tag in tags:
                if not tag:
                    continue
                if isinstance(tag, str) and " " in tag:
                    parts = [t.strip() for t in tag.split(" ") if t.strip()]
                    fixed_tags.extend(parts)
                    changed_tags = True
                else:
                    fixed_tags.append(tag)
            fm["tags"] = fixed_tags

    # --- 本文の余計な改行削除 ---
    cleaned_body = body.lstrip("\n").rstrip("\n")
    changed_body = (cleaned_body != body)

    # --- 変更がある場合のみ書き込み ---
    if changed_tags or changed_body:
        new_frontmatter = yaml.dump(fm, allow_unicode=True, sort_keys=False).strip()
        new_content = f"---\n{new_frontmatter}\n---\n{cleaned_body}"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        status = []
        if changed_tags:
            status.append("tags fixed")
        if changed_body:
            status.append("body cleaned")
        print(f"[Updated] {file_path} ({', '.join(status)})")


def process_vault(vault_path):
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                fix_file(file_path)


if __name__ == "__main__":
    process_vault(VAULT_PATH)