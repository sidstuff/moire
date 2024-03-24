<h1 align="center">Animated Moiré patterns with Python <img src="https://github.com/sidstuff/moire/assets/160637304/3dec5574-d1f4-4a71-b5fd-85d89cafff17" width="32px"></h1>
<div align="center">
  <h3>Inspired by</h3>
  <video src="https://github.com/sidstuff/moire/assets/160637304/8f56fc9a-c4d6-49fa-b21c-6869a26d46f4"></video>
  Source: <a href="https://commons.wikimedia.org/wiki/File:ShadingNetMoiree.webm">Wikimedia Commons</a>
</div>
<hr>

We'll be using the $\ {\huge\mathtt{Python}}$ $\ {\huge\mathtt{Imaging}}$ $\ {\huge\mathtt{Library}}$ ${\huge\mathtt{(Pillow)}}$ to work with images.

Let's test it out by generating some colors.

```python
 1 ⏐ import numpy as np
 2 ⏐ from colorsys import hls_to_rgb, hsv_to_rgb
 3 ⏐ from PIL import Image
 4 ⏐
 5 ⏐ def func(x): return [[np.uint8(round(255*z)) for z in y] for y in x]
 6 ⏐
 7 ⏐ imgs = [['hsl.png',[]],['hsv.png',[]],['hs.png',[]]]
 8 ⏐ for m in [1-p/100 for p in range(101)]:
 9 ⏐     rows = [[],[],[]]
10 ⏐     for n in [h/360 for h in range(360)]:
11 ⏐         rows[0].append(hls_to_rgb(n,m,1))
12 ⏐         rows[1].append(hsv_to_rgb(n,1,m))
13 ⏐         rows[2].append(hls_to_rgb(n,0.5,m))
14 ⏐     for i in range(3): imgs[i][1].append(func(rows[i]))
15 ⏐
16 ⏐ for i in imgs: Image.fromarray(np.array(i[1]),'RGB').save(i[0])
```
<div align="center">
<img src="https://raw.githubusercontent.com/sidstuff/moire/master/hsl.png"><br>hsl.png<br><br>
<img src="https://raw.githubusercontent.com/sidstuff/moire/master/hsv.png"><br>hsv.png<br><br>
<img src="https://raw.githubusercontent.com/sidstuff/moire/master/hs.png"><br>hs.png<br><br>
</div>

The `colorsys` functions use RGB values in the unit interval, `func()` converts them into 8 bit unsigned integers. For `i` in `imgs`, `i[0]` is the filename and `i[1]` will become the image. Every $k^\text{th}$ iteration of the outermost loop, the $k^\text{th}$ rows of the 3 images are listed in `rows`, then appended to said images. Finally, we save the images.

> [!Tip]
> Lines 9–13 can be replaced with the following:
```python
rows = list(zip(*[[hls_to_rgb(n,m,1), hsv_to_rgb(n,1,m), hls_to_rgb(n,0.5,m)] for n in [h/360 for h in range(360)]]))
```
Now let's get to animating the Moiré patterns from the video.
> [!Note]
> Zoom in to see the fine detail. The animations may take a while to load.

First, we need a "net". `0` and `1` wil represent black and white pixels, respectively.

`[0 if n%8 in {1,2} else 1 for n in range(888)]` represents an 888 pixel row, with every 2nd and 3rd pixel out of 8, black.
```python
[[0]*888 if m%8 in {1,2} else [0 if n%8 in {1,2} else 1 for n in range(888)] for m in range(888)]
```
represents an 888x888 image made up of said rows, except every 2nd and 3rd row out of 8, which are black.

Map `0` and `1` to the unsigned 8 bit integers `0` and `255`, respectively, and save this image as a GIF, the format our animation will be.
```python
import numpy as np
from PIL import Image

img1 = np.array([[0]*888 if m%8 in {1,2} else [0 if n%8 in {1,2} else 1 for n in range(888)] for m in range(888)])*255
Image.fromarray(img1.astype(np.uint8)).save('img1.gif')
```
> [!Tip]
> I find ImageMagick to be the best for optimizing GIFs, `mogrify -type bilevel img1.gif` takes `img1.gif` from 6380B to 5303B. All images henceforth will be optimized thus.
<div align="center"><img src="https://github.com/sidstuff/moire/assets/160637304/9715907e-ad06-4070-a32e-cf7d83198ac2" width="50%"></div><br>

Now let's create another net but shifted, then overlay them by multiplying corresponding pixels. Only pixels white in both images will be white in the combined one.
```python
img1 = [[0]*888 if m%8 in {1,2} else [0 if n%8 in {1,2} else 1 for n in range(888)] for m in range(888)]
img2 = [[0]*888 if m%8 in {5,6} else [0 if n%8 in {5,6} else 1 for n in range(888)] for m in range(888)]
img = np.array(img1)*np.array(img2)*255

Image.fromarray(img.astype(np.uint8)).save('img.gif')
```
<div align="center"><img src="https://github.com/sidstuff/moire/assets/160637304/00b999ff-2085-41bd-b0c2-7e68b32cf853" width="50%"></div><br>

To create the Moiré effect, we need to warp the nets. <a href="https://www.desmos.com/calculator/jhrcc33755">Here</a> are a couple of functions that should do the job.
```python
def f1(x,t): return 20*(np.sin(x/100+t)**3+np.sin(np.pi*x/200))
def f2(x,t): return 20*(np.cos(x/100+t)**3+np.cos(np.pi*x/200))
```
The following function shifts a row `r` by `f` pixels (to the right if `f>0` and to the left otherwise).
```python
def s(r,f): return [1]*f+r[:(-f)] if f>0 else r[(-f):]+[1]*(-f)
```
Define `img1` and `img2` as before, and `imgs = []` to store the images. Then,
```python
for t in np.linspace(0,2*np.pi,75,endpoint=False):    # every timestep

    i1 = img1.copy()    # reset i1 and i2, but to a (shallow) copy of img1 and img2
    i2 = img2.copy()    # to avoid the latter pair changing when the former are changed

    for i,r in enumerate(i1): i1[i] = s(r,round(f1(i,t)))    # Shift i1 rows by f1
    i1 = [list(a) for a in zip(*i1)]                         # Transpose i1 so columns become rows
    for i,r in enumerate(i1): i1[i] = s(r,round(f2(i,t)))    # Shift i1 rows (actually cols) by f2
    i1 = [list(a) for a in zip(*i1)]                         # Transpose i1 back
    for i,r in enumerate(i2): i2[i] = s(r,round(f2(i,t)))    # Shift i2 rows by f2
    i2 = [list(a) for a in zip(*i2)]                         # Transpose i2 so columns become rows
    for i,r in enumerate(i2): i2[i] = s(r,round(f1(i,t)))    # Shift i2 rows (actually cols) by f1
    i2 = [list(a) for a in zip(*i2)]                         # Transpose i2 back

    i = np.array(i1)*np.array(i2)*255                        # Combine i1 and i2 into i
    imgs.append(Image.fromarray(i.astype(np.uint8)))         # Append i to imgs

imgs[0].save('moire.gif', save_all=True, append_images=imgs[1:], optimize=False, duration=120, loop=0)    # Save imgs as GIF
```
<div align="center"><img src="https://github.com/sidstuff/moire/assets/160637304/0c1828a4-3b05-4cbd-bc08-081736b7e3f6" width="50%"></div><br>

Due to shifting the rows first, then the columns, there are vertical striations, and the circular patterns all stretch horizontally. To fix this, let's shift the rows, then the columns, then the rows again, and then the columns again. Replace the `20` in `f1` and `f2` with `10` and enclose the middle block from before in `for _ in range(2)`. The final code is <a href="https://github.com/sidstuff/moire/blob/master/moire.py">here</a>. And here's our final result!

<div align="center"><img src="https://raw.githubusercontent.com/sidstuff/moire/master/moire.gif" width="50%"></div>
