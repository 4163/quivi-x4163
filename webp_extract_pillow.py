from __future__ import print_function

import os
import sys
import time

from PIL import Image


def main(argv):
    if len(argv) != 3:
        print("usage: webp_extract_pillow.py INPUT_ANIMATION OUTPUT_DIR", file=sys.stderr)
        return 2
    src, out_dir = argv[1], argv[2]
    profile = os.environ.get("QUIVI_ANIM_PROFILE")
    t0 = time.time()
    seek_time = 0.0
    convert_time = 0.0
    save_time = 0.0
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    im = Image.open(src)
    frame_count = getattr(im, "n_frames", 1)
    delays = []
    for idx in range(frame_count):
        t = time.time()
        im.seek(idx)
        seek_time += time.time() - t
        delay = int(im.info.get("duration", 100) or 100)
        if delay < 20:
            delay = 100
        delays.append(delay)
        t = time.time()
        frame = im.convert("RGB")
        convert_time += time.time() - t
        t = time.time()
        frame.save(os.path.join(out_dir, "frame_%04d.bmp" % idx))
        save_time += time.time() - t
    with open(os.path.join(out_dir, "delays.txt"), "w") as f:
        for delay in delays:
            f.write("%d\n" % delay)
    if profile:
        with open(os.path.join(out_dir, "profile.txt"), "w") as f:
            f.write("frames=%d\n" % frame_count)
            f.write("total=%.6f\n" % (time.time() - t0))
            f.write("seek=%.6f\n" % seek_time)
            f.write("convert=%.6f\n" % convert_time)
            f.write("save=%.6f\n" % save_time)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
