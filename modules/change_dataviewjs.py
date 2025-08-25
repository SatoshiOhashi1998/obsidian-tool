import os
import re

# === 設定 ===
VAULT_PATH = r"C:\Users\user\OneDrive\Desktop\container\日記"  # Vault のパス
DAILY_NOTE_PATTERN = r"\d{4}-\d{2}-\d{2}\.md"  # ファイル名が日付の場合

# 新しい統合 dataviewjs コード（置換先）
NEW_CODE = """```dataviewjs
const noteDate = dv.current().file.name;

// created を YYYY-MM-DD 文字列として比較
const todaysFiles = dv.pages()
    .filter(p => p.created && p.created.toString().slice(0,10) === noteDate);

// カテゴリ定義
const categories = [
    { title: "Twitter, YouTube関連", tags: ["#twitter", "#youtube"] },
    { title: "ChatGPT", tags: ["#chatgpt"] },
    { title: "その他", tags: [] }
];

// 全タグリスト（その他除外用）
const allTags = categories.flatMap(c => c.tags);

// カテゴリごとにリスト表示
for (let cat of categories) {
    dv.header(3, cat.title);

    let matched;
    if (cat.tags.length > 0) {
        matched = todaysFiles.filter(p =>
            (p.file?.tags ?? []).some(tag => cat.tags.includes(tag))
        );
    } else {
        matched = todaysFiles.filter(p =>
            !(p.file?.tags ?? []).some(tag => allTags.includes(tag))
        );
    }

    if (matched.length === 0) {
        dv.paragraph(`${cat.title} に該当するノートはありません。`);
    } else {
        dv.list(matched.map(p => dv.fileLink(p.file.path)));
    }
}
```"""

def replace_old_blocks(content):
    """
    既存の dataviewjs ブロックをすべて新しい統合版ブロックに置換
    """
    return re.sub(r"```dataviewjs.*?```", NEW_CODE, content, flags=re.DOTALL)

def clean_body_whitespace(content):
    """
    YAML frontmatter の下の本文とファイル末尾の余分な改行を削除
    """
    match = re.match(r"^(---\n.*?\n---\n)(.*)$", content, flags=re.DOTALL)
    if match:
        frontmatter, body = match.groups()
        body = body.strip("\n")  # 先頭・末尾の改行削除
        return frontmatter + body
    else:
        # frontmatter がない場合
        return content.strip("\n")

def process_vault(vault_path):
    for root, _, files in os.walk(vault_path):
        for file in files:
            if re.match(DAILY_NOTE_PATTERN, file):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = replace_old_blocks(content)
                new_content = clean_body_whitespace(new_content)

                if content != new_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"[Updated] {file_path}")

if __name__ == "__main__":
    process_vault(VAULT_PATH)
