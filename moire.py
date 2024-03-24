import numpy as np
from PIL import Image

def f1(x,t): return 10*(np.sin(x/100+t)**3+np.sin(np.pi*x/200))
def f2(x,t): return 10*(np.cos(x/100+t)**3+np.cos(np.pi*x/200))

def s(r,f): return [1]*f+r[:(-f)] if f>0 else r[(-f):]+[1]*(-f)

img1 = [[0]*888 if m%8 in {1,2} else [0 if n%8 in {1,2} else 1 for n in range(888)] for m in range(888)]
img2 = [[0]*888 if m%8 in {5,6} else [0 if n%8 in {5,6} else 1 for n in range(888)] for m in range(888)]

imgs = []

for t in np.linspace(0,2*np.pi,75,endpoint=False):

    i1 = img1.copy()
    i2 = img2.copy()

    for _ in range(2):
        for i,r in enumerate(i1): i1[i] = s(r,round(f1(i,t)))
        i1 = [list(a) for a in zip(*i1)]
        for i,r in enumerate(i1): i1[i] = s(r,round(f2(i,t)))
        i1 = [list(a) for a in zip(*i1)]
        for i,r in enumerate(i2): i2[i] = s(r,round(f2(i,t)))
        i2 = [list(a) for a in zip(*i2)]
        for i,r in enumerate(i2): i2[i] = s(r,round(f1(i,t)))
        i2 = [list(a) for a in zip(*i2)]

    i = np.array(i1)*np.array(i2)*255
    imgs.append(Image.fromarray(i.astype(np.uint8)))

imgs[0].save('moire.gif', save_all=True, append_images=imgs[1:], optimize=False, duration=120, loop=0)
