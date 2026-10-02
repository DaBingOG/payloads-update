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
    gh_user = "DaBingOG"
    gh_repo = "payloads-update"
    base_url = f"https://{gh_user}.github.io/{gh_repo}/payloads/"

    payload_list = []

    # 递归遍历payloads目录所有elf
    if os.path.exists(payload_base_dir):
        for root, _, files in os.walk(payload_base_dir):
            for fname in files:
                if fname.lower().endswith(".elf"):
                    full_path = os.path.join(root, fname)
                    rel_path = os.path.relpath(full_path, payload_base_dir)
                    remote_url = base_url + rel_path.replace("\\", "/")
                    sha = get_sha256(full_path)

                    # 提取版本
                    version = "v1.0.0"
                    if "_v" in fname:
                        ver_str = fname.split("_v")[-1].replace(".elf","")
                        version = f"v{ver_str}"

                    item = {
                        "name": fname,
                        "filename": fname,
                        "url": remote_url,
                        "description": "",
                        "version": version,
                        "category": "Payloads",
                        "checksum": sha
                    }
                    payload_list.append(item)
    else:
        print(f"⚠️ 警告：目录 {payload_base_dir} 不存在！")

    # ========== 自动创建json目录 ==========
    out_dir = os.path.join(repo_root, "json")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "payloads.json")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload_list, f, indent=2, ensure_ascii=False)
    print(f"✅ 生成完成，共 {len(payload_list)} 个payload，输出到 {out_file}")

if __name__ == "__main__":
    main()
