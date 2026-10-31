import sys, numpy as np
from PIL import Image, ImageFilter
im = Image.open(sys.argv[1]).convert("RGB"); a = np.asarray(im).astype(float) / 255
lum = a.mean(2, keepdims=True); bright = np.clip((lum - 0.62) / 0.38, 0, 1) * a
glow = np.asarray(Image.fromarray((bright * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(28))).astype(float) / 255
glow2 = np.asarray(Image.fromarray((bright * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(90))).astype(float) / 255
a = 1 - (1 - a) * (1 - glow * 0.55) * (1 - glow2 * 0.45)          # screen-blend bloom
h, w, _ = a.shape; sh = 3                                          # chromatic aberration toward edges
a[:, sh:, 0] = a[:, :-sh, 0] * 0.6 + a[:, sh:, 0] * 0.4; a[:, :-sh, 2] = a[:, sh:, 2] * 0.6 + a[:, :-sh, 2] * 0.4
yy, xx = np.mgrid[0:h, 0:w]; v = ((xx / w - 0.5) ** 2 + (yy / h - 0.5) ** 2); a *= (1 - 0.55 * v)[..., None]
rs = np.random.default_rng(3); a += rs.normal(0, 0.035, (h, w, 1))
Image.fromarray((np.clip(a, 0, 1) * 255).astype("uint8")).save(sys.argv[2], quality=95); print("post ok")
