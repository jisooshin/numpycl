import npcl
from npcl import to_device
import numpy as np
import cv2

convolve = npcl.ops.convolve.convolve2d

img = cv2.imread('lake.tif', 0)
img = to_device(img)

# noise will be added
noise = 5*np.random.normal(size=img.shape)
noise = to_device(noise)

# 5 x 5 box kernel
kernel = np.ones((5, 5))/25.
kernel = to_device(kernel)

blurry = convolve(img, kernel)+noise

cv2.imshow('blurry', np.clip(blurry.get(), 0, 255).astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()

deblurred, iter = npcl.solvers.deconv.deconv_fbstv(
    blurry, kernel, mu=1e-1, verbose=True,
    )

cv2.imshow('deblurred', np.clip(deblurred.get(), 0, 255).astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()