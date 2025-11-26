import json
import os
import sys

def pecah_json(file_path, max_size_kb=100):
    if not os.path.exists(file_path):
        print(f"❌ File '{file_path}' tidak ditemukan.")
        return

    # Baca isi JSON
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("❌ File JSON harus berupa array (list).")
        return

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    folder_name = base_name
    os.makedirs(folder_name, exist_ok=True)

    part = 0
    temp = []

    for i, item in enumerate(data):
        temp.append(item)
        json_str = json.dumps(temp, ensure_ascii=False, separators=(",", ":"))
        size_kb = len(json_str.encode("utf-8")) / 1024

        if size_kb > max_size_kb:
            # Hapus item terakhir dan simpan bagian sebelumnya
            last_item = temp.pop()
            out_file = os.path.join(folder_name, f"{base_name}_{part}.json")
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(temp, f, ensure_ascii=False, separators=(",", ":"))
            print(f"✅ Disimpan: {out_file} ({len(temp)} item, urutan {i - len(temp)}–{i-1})")

            part += 1
            temp = [last_item]

    # Simpan sisa terakhir
    if temp:
        out_file = os.path.join(folder_name, f"{base_name}_{part}.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(temp, f, ensure_ascii=False, separators=(",", ":"))
        print(f"✅ Disimpan: {out_file} ({len(temp)} item, urutan terakhir)")

    print("✅ Selesai memecah file secara berurutan (mode shrink).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("📘 Contoh penggunaan:")
        print("    python3 pecah.py atin.json")
        print("    python3 pecah.py atin.json 200  # (opsional: ubah batas 200KB)")
    else:
        file_path = sys.argv[1]
        max_size = int(sys.argv[2]) if len(sys.argv) >= 3 else 100
        pecah_json(file_path, max_size)