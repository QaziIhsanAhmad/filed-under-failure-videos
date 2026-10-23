"""Xenova Solutions Reel/Short builder (free: Playwright frames + Kokoro TTS + ffmpeg + generated music).

Usage: python3 xreel.py <spec.json> <outDir> [--voice bm_george]
Needs kokoro-v1.0.onnx and voices-v1.0.bin next to this script or in $KOKORO_DIR, and $CHROMIUM if Playwright's own
browser is missing. Output: <id>.mp4 (1080x1920, 30 fps, H.264, AAC 48 kHz), <id>.srt, <id>-cover.jpg.
Each scene: the frame stays on screen while its "say" line is spoken, plus a short pause.
Background music is a quiet pad synthesised here (original, no licence needed).
"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 24000


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"FAILED: {' '.join(cmd[:4])}...\n{r.stderr[-1500:]}")


def pad_music(seconds):
    t = np.arange(int(seconds * SR)) / SR
    chords = [(220.0, 277.18, 329.63), (196.0, 246.94, 293.66), (174.61, 220.0, 261.63), (196.0, 246.94, 329.63)]
    out = np.zeros_like(t)
    for i, ch in enumerate(chords * int(seconds // 16 + 1)):
        s, e = i * 4.0, i * 4.0 + 4.6
        m = (t >= s) & (t < e)
        if not m.any(): break
        tt = t[m] - s
        env = np.minimum(1, tt / 1.2) * np.minimum(1, (4.6 - tt) / 1.2)
        for f in ch:
            out[m] += env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 2 * tt)) / 3
    fade = np.minimum(1, np.minimum(t / 1.5, (seconds - t) / 2.0))
    return out / (np.abs(out).max() + 1e-9) * 0.05 * fade


def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"


def main():
    spec_path, out = sys.argv[1], os.path.abspath(sys.argv[2])
    voice = sys.argv[sys.argv.index("--voice") + 1] if "--voice" in sys.argv else "bm_george"
    spec = json.load(open(spec_path)); vid = spec["id"]
    frames = os.path.join(out, "frames"); os.makedirs(frames, exist_ok=True)
    run(["node", os.path.join(HERE, "xreel.js"), spec_path, frames])

    from kokoro_onnx import Kokoro
    kd = os.environ.get("KOKORO_DIR", HERE)
    tts = Kokoro(os.path.join(kd, "kokoro-v1.0.onnx"), os.path.join(kd, "voices-v1.0.bin"))
    voice_track, durs, srt = [], [], []
    clock = 0.0
    for i, s in enumerate(spec["scenes"]):
        audio, sr = tts.create(s["say"], voice=voice, speed=s.get("speed", 1.0), lang="en-gb")
        assert sr == SR
        lead, tail = 0.25, (0.6 if i < len(spec["scenes"]) - 1 else 1.2)
        seg = np.concatenate([np.zeros(int(lead * SR)), audio, np.zeros(int(tail * SR))])
        d = len(seg) / SR
        srt.append(f"{i + 1}\n{ts(clock + lead)} --> {ts(clock + lead + len(audio) / SR)}\n{s.get('sub', s['say'])}\n")
        voice_track.append(seg); durs.append(d); clock += d
    voice = np.concatenate(voice_track)
    mix = voice * 0.95 + pad_music(len(voice) / SR)
    sf.write(os.path.join(out, "mix.wav"), np.clip(mix, -1, 1), SR)
    open(os.path.join(out, f"{vid}.srt"), "w").write("\n".join(srt))

    # one still clip per scene with a short fade, then concat
    lst = []
    for i, d in enumerate(durs):
        clip = os.path.join(out, f"c{i + 1:02d}.mp4")
        run(["ffmpeg", "-y", "-loop", "1", "-framerate", "30", "-i", os.path.join(frames, f"s{i + 1:02d}.png"), "-t", f"{d:.3f}",
             "-vf", f"scale=1188:2112,zoompan=z='min(zoom+0.00035,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(d * 30) + 2}:s=1080x1920:fps=30,"
                   f"fade=in:st=0:d=0.25,fade=out:st={max(0, d - 0.2):.3f}:d=0.2,format=yuv420p",
             "-c:v", "libx264", "-preset", "medium", "-crf", "27", "-r", "30", clip])
        lst.append(f"file '{clip}'")
    open(os.path.join(out, "list.txt"), "w").write("\n".join(lst))
    final = os.path.join(out, f"{vid}.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(out, "list.txt"), "-i", os.path.join(out, "mix.wav"),
         "-c:v", "copy", "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "160k", "-af", "loudnorm=I=-15:TP=-1.5:LRA=11",
         "-shortest", "-movflags", "+faststart", final])
    run(["ffmpeg", "-y", "-i", os.path.join(frames, "s01.png"), "-q:v", "3", os.path.join(out, f"{vid}-cover.jpg")])
    print(final, f"{sum(durs):.1f}s")


if __name__ == "__main__":
    main()
