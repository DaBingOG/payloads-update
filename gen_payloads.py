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

    # 海外源 github.io
    gh_base_url = "https://dabingog.github.io/payloads-update/payloads/"
    # 国内源 JSDMirror
    china_base_url = "https://cdn.jsdmirror.com/gh/dabingog/payloads-update@main/payloads/"

    gh_list = []
    china_list = []

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
                    gh_item = item_template.copy()
                    gh_item["url"] = gh_base_url + rel_url
                    gh_list.append(gh_item)

                    china_item = item_template.copy()
                    china_item["url"] = china_base_url + rel_url
                    china_list.append(china_item)
    else:
        print(f"⚠️ 警告：目录 {payload_base_dir} 不存在！")

    out_dir = os.path.join(repo_root, "json")
    os.makedirs(out_dir, exist_ok=True)

    # 改名：payloads_og.json
    gh_json_path = os.path.join(out_dir, "payloads_og.json")
    with open(gh_json_path, "w", encoding="utf-8") as f:
        json.dump(gh_list, f, indent=2, ensure_ascii=False)

    # 改名：payloads_cn.json
    china_json_path = os.path.join(out_dir, "payloads_cn.json")
    with open(china_json_path, "w", encoding="utf-8") as f:
        json.dump(china_list, f, indent=2, ensure_ascii=False)

    print(f"✅ 原版OG清单：{gh_json_path}，共 {len(gh_list)}")
    print(f"✅ 国内CN清单：{china_json_path}，共 {len(china_list)}")

if __name__ == "__main__":
    main()
