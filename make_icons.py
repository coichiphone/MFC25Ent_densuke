#!/usr/bin/env python3
"""出欠管理アプリのアイコンを作る。
緑の角丸 + 白いサッカーボール + チェックマーク。
  python3 make_icons.py   →  icons/favicon.png (32px) / icons/apple-touch-icon.png (180px)
"""
from PIL import Image, ImageDraw
import math, os

GREEN = (46, 125, 50)
WHITE = (255, 255, 255)
DARK = (27, 77, 32)

def ball(d, cx, cy, r):
    """白いサッカーボール（中央の五角形＋周りの切れ込み）"""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    # 中央の五角形
    pent = [(cx + r * 0.42 * math.sin(math.radians(a)),
             cy - r * 0.42 * math.cos(math.radians(a))) for a in range(0, 360, 72)]
    d.polygon(pent, fill=DARK)
    # 五角形の各頂点から外へ伸びる縫い目
    for (px, py) in pent:
        vx, vy = px - cx, py - cy
        n = math.hypot(vx, vy) or 1
        ex, ey = cx + vx / n * r, cy + vy / n * r
        d.line([(px, py), (ex, ey)], fill=DARK, width=max(1, int(r * 0.11)))

def check(d, size):
    """右下のチェックマーク。ボールと重なるので緑のフチを先に敷く"""
    s = size
    pts = [(s * 0.50, s * 0.70), (s * 0.64, s * 0.84), (s * 0.88, s * 0.50)]
    d.line(pts, fill=GREEN, width=int(s * 0.22), joint="curve")
    d.line(pts, fill=WHITE, width=int(s * 0.12), joint="curve")

def make(size, with_check=True):
    ss = size * 4  # 4倍で描いて縮小（なめらかに）
    img = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, ss - 1, ss - 1], radius=int(ss * 0.22), fill=GREEN)
    if with_check:
        ball(d, ss * 0.44, ss * 0.42, ss * 0.30)
        check(d, ss)
    else:
        # 小さく表示される用: ボールを大きく中央に置く
        ball(d, ss * 0.5, ss * 0.5, ss * 0.38)
    return img.resize((size, size), Image.LANCZOS)

if __name__ == "__main__":
    os.makedirs("icons", exist_ok=True)
    # 16pxではチェックが潰れるので、小さい方はボールだけ
    make(32, with_check=False).save("icons/favicon.png")
    make(180).save("icons/apple-touch-icon.png")
    print("icons/favicon.png, icons/apple-touch-icon.png を作成しました")
