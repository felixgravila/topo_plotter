# %%

import matplotlib.pyplot as plt
import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import mapping

PROCESSES = [
    ("Denmark", "Denmark-B", "50N000E_20101117_gmted_mea075.tif", 0, -1, 0, 2200, 1.8),
    ("Denmark", "Denmark+B", "50N000E_20101117_gmted_mea075.tif", 0, -1, 0, -1, 1.8),
    ("Romania", "Romania", "30N000E_20101117_gmted_mea075.tif", 0, -1, 0, -1, 1.5),
]

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
    edge = 50
    p_t = country_topography[0][B0:B1, B2:B3]
    canvas = np.zeros((p_t.shape[0] + edge * 2, p_t.shape[1] + edge * 2))
    canvas[edge:-edge, edge:-edge] = p_t
    canvas = np.maximum(canvas, 0) / canvas.max()

    x_dim = 30
    y_dim = x_dim * canvas.shape[0] / canvas.shape[1]

    plt.figure(figsize=(x_dim, y_dim))
    c = plt.imshow(canvas, cmap="gray", aspect=ASPECT)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{OUTNAME}.png", bbox_inches="tight", pad_inches=0)
    plt.show()

# %%
