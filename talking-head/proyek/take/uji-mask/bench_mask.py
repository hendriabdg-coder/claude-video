"""Benchmark the claude-video-effects Tracker (MediaPipe mask + YuNet face) against an existing
HyperFrames remove-background matte. usage: python bench_mask.py REPO_SCRIPTS SEG.mp4 MATTE.mov OUTDIR"""
import os, sys, time, json, subprocess
import numpy as np, cv2

repo, seg, matte, out = sys.argv[1:5]
sys.path.insert(0, repo)
import fx  # noqa: E402  (read_frames, Tracker, smooth from the repo)

os.makedirs(out, exist_ok=True)
W, H = 1080, 1920


def alpha_frames(path):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'scale={W}:{H}', '-pix_fmt', 'rgba',
                          '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    n = W * H * 4
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 4)[..., 3].copy()
    p.wait()


ref = list(alpha_frames(matte))
res = {}
for aw in (540, 1080):
    ah = aw * 16 // 9
    frames = list(fx.read_frames(seg, aw, ah, '30'))
    trk = fx.Tracker(aw, ah)
    masks, faces = [], []
    t0 = time.perf_counter()
    for i, fr in enumerate(frames):
        m, f = trk(fr, int(i * 1000 / 30)); masks.append(m); faces.append(f)
    dt = time.perf_counter() - t0
    ious, maes, edge = [], [], []
    for i, m in enumerate(masks):
        mm = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255
        rr = ref[i].astype(np.float32) / 255
        a, b = mm > 0.5, rr > 0.5
        ious.append((a & b).sum() / max(1, (a | b).sum()))
        maes.append(np.abs(mm - rr).mean())
        band = cv2.dilate((b * 255).astype(np.uint8), np.ones((25, 25))) - cv2.erode((b * 255).astype(np.uint8), np.ones((25, 25)))
        edge.append(np.abs(mm - rr)[band > 0].mean())
        if aw == 540: np.save(os.path.join(out, f'mp_{i:03d}.npy'), m)
    res[aw] = dict(frames=len(frames), seconds=round(dt, 2), fps=round(len(frames) / dt, 1),
                   iou=round(float(np.mean(ious)), 4), mae=round(float(np.mean(maes)), 4),
                   edge_err=round(float(np.mean(edge)), 4), faces_found=sum(f is not None for f in faces))
    print(aw, res[aw], flush=True)
    if aw == 540:
        np.save(os.path.join(out, 'faces.npy'), np.array([f if f else (np.nan,) * 3 for f in faces], float))
json.dump(res, open(os.path.join(out, 'result.json'), 'w'), indent=1)

# side-by-side check frames: plate | remove-background on red | MediaPipe on red | difference
src = list(fx.read_frames(seg, W, H, '30'))
red = np.zeros((H, W, 3), np.float32); red[...] = (230, 40, 60)
for i in (5, 30, 55):
    img = src[i].astype(np.float32)
    rr = ref[i].astype(np.float32)[..., None] / 255
    mm = cv2.resize(np.load(os.path.join(out, f'mp_{i:03d}.npy')), (W, H)).astype(np.float32)[..., None] / 255
    A = img * rr + red * (1 - rr); B = img * mm + red * (1 - mm)
    D = np.repeat(np.abs(mm - rr) * 255, 3, 2)
    row = np.hstack([img, A, B, D]).clip(0, 255).astype(np.uint8)
    for k, lab in enumerate(['plate', 'remove-background', 'MediaPipe 540', 'beda']):
        cv2.putText(row, lab, (k * W + 30, 80), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 255), 6)
    cv2.imwrite(os.path.join(out, f'cmp_{i:03d}.jpg'), cv2.cvtColor(cv2.resize(row, (row.shape[1] // 3, row.shape[0] // 3)), cv2.COLOR_RGB2BGR))
    head = np.hstack([A[:760], B[:760]]).clip(0, 255).astype(np.uint8)  # the region the BEHIND overlay actually uses
    cv2.imwrite(os.path.join(out, f'head_{i:03d}.jpg'), cv2.cvtColor(cv2.resize(head, (head.shape[1] // 2, head.shape[0] // 2)), cv2.COLOR_RGB2BGR))
print('done')
