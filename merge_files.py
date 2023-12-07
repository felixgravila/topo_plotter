# %%

from rasterio.merge import merge
import rasterio
import matplotlib.pyplot as plt

output_path = "topo/europe.tif"

raster_files = [
    "topo/50N000E_20101117_gmted_mea075.tif",
    "topo/50N030W_20101117_gmted_mea075.tif",
    "topo/30N000E_20101117_gmted_mea075.tif",
    "topo/30N030W_20101117_gmted_mea075.tif",
]

raster_to_mosiac = []
for p in raster_files:
    raster = rasterio.open(p)
    raster_to_mosiac.append(raster)


mosaic, output = merge(raster_to_mosiac)

output_meta = raster.meta.copy()
output_meta.update(
    {
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": output,
    }
)

plt.imshow(mosaic[0, ::4, ::4], cmap="gray")

# %%

with rasterio.open(output_path, "w", **output_meta) as m:
    m.write(mosaic)

# %%
