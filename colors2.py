import numpy as np
from colorsys import hls_to_rgb, hsv_to_rgb
from PIL import Image

def func(x): return [[np.uint8(round(255*z)) for z in y] for y in x]

imgs = [['hsl.png',[]],['hsv.png',[]],['hs.png',[]]]
for m in [1-p/100 for p in range(101)]:
	rows = list(zip(*[[hls_to_rgb(n,m,1), hsv_to_rgb(n,1,m), hls_to_rgb(n,0.5,m)] for n in [h/360 for h in range(360)]]))
	for i in range(3): imgs[i][1].append(func(rows[i]))
 
for i in imgs: Image.fromarray(np.array(i[1]),'RGB').save(i[0])
