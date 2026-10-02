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
    # ========= 修改这里！填你的github用户名、仓库名 =========
    gh_user = "你的github用户名"
    gh_repo = "你的仓库名"
    base_url = f"https://{gh_user}.github.io/{gh_repo}/payloads/"

    payload_list = []

    # 递归遍历所有 .elf
    for root, _, files in os.walk(payload_base_dir):
        for fname in files:
            if fname.lower().endswith(".elf"):
                full_path = os.path.join(root, fname)
                rel_path = os.path.relpath(full_path, payload_base_dir)
                # url路径统一换成 / 分隔（windows自动转义）
                remote_url = base_url + rel_path.replace("\\", "/")
                sha = get_sha256(full_path)

                # 从文件名自动提取版本号，例如 ps5_overlay_v1.0.15.elf → v1.0.15
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

    out_file = os.path.join(repo_root, "json", "payloads.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload_list, f, indent=2, ensure_ascii=False)
    print(f"✅ 生成完成，共 {len(payload_list)} 个payload，输出到 {out_file}")

if __name__ == "__main__":
    main()
