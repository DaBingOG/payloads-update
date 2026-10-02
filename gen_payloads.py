import os
import hashlib
import json

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    repo_root = os.getcwd()
    payload_base_dir = os.path.join(repo_root, "payloads")

gh_base_url = "https://dabingog.github.io/payloads-update/payloads/"
china_base_url = "https://cdn.jsdmirror.com/gh/dabingog/payloads-update@main/payloads/"

    gh_list = []
    gitee_list = []

    if os.path.exists(payload_base_dir):
        for root, _, files in os.walk(payload_base_dir):
            for fname in files:
                if fname.lower().endswith(".elf"):
                    full_path = os.path.join(root, fname)
                    rel_path = os.path.relpath(full_path, payload_base_dir)
                    rel_url = rel_path.replace("\\", "/")
                    sha = get_sha256(full_path)

                    # 提取版本号
                    version = "v1.0.0"
                    if "_v" in fname:
                        ver_str = fname.split("_v")[-1].replace(".elf","")
                        version = f"v{ver_str}"

                    item_template = {
                        "name": fname,
                        "filename": fname,
                        "description": "",
                        "version": version,
                        "category": "Payloads",
                        "checksum": sha
                    }
                    # Github源，填入github url
                    gh_item = item_template.copy()
                    gh_item["url"] = gh_base_url + rel_url
                    gh_list.append(gh_item)

                    # Gitee源，填入gitee url
                    gitee_item = item_template.copy()
                    gitee_item["url"] = gitee_base_url + rel_url
                    gitee_list.append(gitee_item)
    else:
        print(f"⚠️ 警告：目录 {payload_base_dir} 不存在！")

    # 自动创建json目录
    out_dir = os.path.join(repo_root, "json")
    os.makedirs(out_dir, exist_ok=True)

    # 输出github版本json
    gh_json_path = os.path.join(out_dir, "github_payloads.json")
    with open(gh_json_path, "w", encoding="utf-8") as f:
        json.dump(gh_list, f, indent=2, ensure_ascii=False)

    # 输出gitee版本json
    gitee_json_path = os.path.join(out_dir, "gitee_payloads.json")
    with open(gitee_json_path, "w", encoding="utf-8") as f:
        json.dump(gitee_list, f, indent=2, ensure_ascii=False)

    print(f"✅ Github清单生成完成，共 {len(gh_list)} 个payload: {gh_json_path}")
    print(f"✅ Gitee清单生成完成，共 {len(gitee_list)} 个payload: {gitee_json_path}")

if __name__ == "__main__":
    main()
