from pathlib import Path

import cv2

DATA_DIR = Path.cwd() / "data"
for filename in ("ocean.mkv", "ocean.mp4"):
    print(filename)
    path = DATA_DIR / filename
    cap = cv2.VideoCapture(str(path))
    print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    ok, img = cap.read()
    assert ok
    print(img.shape)
