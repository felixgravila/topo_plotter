# %%

import matplotlib.pyplot as plt
import rasterio
import rasterio.mask
import numpy as np
import geopandas as gpd
from shapely.geometry import mapping
from math import ceil

PROCESSES = [
    ("Denmark", "Denmark-B", "europe.tif", 0, -1, 0, 2200, 1.8),
    ("Denmark", "Denmark+B", "europe.tif", 0, -1, 0, -1, 1.8),
    ("Romania", "Romania", "europe.tif", 0, -1, 0, -1, 1.5),
    ("United Kingdom", "United Kingdom", "europe.tif", 0, -1, 2630, -1, 1.7),
]

LITO_HEIGHT_WITHOUT_BASE = 10
LAYER_HEIGHT = 0.2

min_representable_value = ceil(255 / (LITO_HEIGHT_WITHOUT_BASE / LAYER_HEIGHT))

df = gpd.read_file("ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp")

for NAME, OUTNAME, FILE, B0, B1, B2, B3, ASPECT in PROCESSES:
    file = rasterio.open(f"topo/{FILE}")
    dataset = file.read()

    cbox = df.loc[df["ADMIN"] == NAME].iloc[0].geometry

    country_topography, clipped_transform = rasterio.mask.mask(
        file,
        [mapping(cbox)],
        crop=True,
        nodata=0,
    )

    # Make canvas and pad a bit
    edge = 5
    p_t = country_topography[0][B0:B1, B2:B3]
    p_t = np.maximum(0, p_t) / p_t.max()
    sea = np.where(p_t == 0)

    p_t = ((p_t * (255 - min_representable_value)) + min_representable_value).astype(
        np.uint8
    )
    p_t[sea] = 0
    canvas = np.zeros(
        (p_t.shape[0] + edge * 2, p_t.shape[1] + edge * 2),
        dtype=np.uint8,
    )
    canvas[edge:-edge, edge:-edge] = p_t

    x_dim = 50
    y_dim = x_dim * canvas.shape[0] / canvas.shape[1]

    plt.figure(figsize=(x_dim, y_dim))
    c = plt.imshow(canvas, cmap="gray", aspect=ASPECT)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{OUTNAME}.png", bbox_inches="tight", pad_inches=0)
    plt.show()

# %%
