"""Make free plan rejects files over 5 MB (tested 2026-10-08: MaxFileSizeExceededError).
For lane=make rows still 'planned', re-encode any file over LIMIT into '<name>-make.mp4'
sized to fit, and point the row at it (original kept in 'file_original')."""
import json, os, subprocess

LIMIT = 4_500_000          # bytes, safety margin under Make's 5 MB
TARGET = 4_100_000
AUDIO_K = 96

def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip())

def fit(src, dst):
    vk = int(TARGET * 8 / duration(src) / 1000) - AUDIO_K
    for k in (vk, int(vk * 0.85), int(vk * 0.7)):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-c:v", "libx264", "-preset", "slow",
                        "-b:v", f"{k}k", "-maxrate", f"{k}k", "-bufsize", f"{2*k}k", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", f"{AUDIO_K}k", "-ar", "48000", "-movflags", "+faststart", dst], check=True)
        if os.path.getsize(dst) <= LIMIT:
            return True
    return False

def main():
    led = json.load(open("yt/ledger.json"))
    changed = False
    for it in led["items"]:
        f = it.get("file", "")
        if it.get("lane") != "make" or it.get("status") != "planned" or not os.path.exists(f):
            continue
        if os.path.getsize(f) <= LIMIT:
            continue
        dst = f[:-4] + "-make.mp4"
        if fit(f, dst):
            it["file_original"], it["file"] = f, dst
            print("fitted", it["id"], os.path.getsize(dst))
        else:
            it["status"] = "paused-toolarge"
            it["note"] = "Could not fit under Make's 5 MB limit; upload in YouTube Studio"
        changed = True
    if changed:
        with open("yt/ledger.json", "w") as fh:
            json.dump(led, fh, indent=1, ensure_ascii=False)
            fh.write("\n")

if __name__ == "__main__":
    main()
