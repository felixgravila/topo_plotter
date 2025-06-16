# %%

import matplotlib.pyplot as plt
import rasterio
import rasterio.mask
import numpy as np
import shapely
from shapely.geometry import mapping

file = rasterio.open(f"topo/europe.tif")
dataset = file.read()

cbox = shapely.Polygon([(10, 56.3), (10.4, 56.3), (10.4, 56), (10, 56)])

# %%

country_topography, clipped_transform = rasterio.mask.mask(
    file,
    [mapping(cbox)],
    crop=True,
    nodata=0,
)

canvas = country_topography[0]
canvas = np.maximum(0, canvas) / canvas.max()

x_dim = 20
y_dim = x_dim * canvas.shape[0] / canvas.shape[1]

plt.figure(figsize=(x_dim, y_dim))
c = plt.imshow(canvas, cmap="gray", aspect=1.5, interpolation="lanczos")
plt.axis("off")
plt.tight_layout()
plt.savefig("aarhus.png", bbox_inches="tight", pad_inches=0)
plt.show()

# %%
