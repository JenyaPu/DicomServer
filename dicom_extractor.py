import os

from matplotlib import pyplot as plt
from pydicom import dcmread
from pydicom.data import get_testdata_file

folder_all = "data"
folder_out = "data_extracted"
folders_dates = os.listdir(folder_all)
os.makedirs(folder_out, exist_ok=True)

for folder_date in folders_dates:
    images = os.listdir(os.path.join(folder_all, folder_date))
    for image in images:
        print(image)
        path = get_testdata_file(image)
        ds = dcmread(os.path.join(folder_all, folder_date, image))
        os.makedirs(os.path.join(folder_out, folder_date, "metadata"), exist_ok=True)
        os.makedirs(os.path.join(folder_out, folder_date, "images"), exist_ok=True)
        with open(os.path.join(folder_out, folder_date, "metadata", image + ".txt"), "w") as f:
            f.write(str(ds))
        arr = ds.pixel_array
        if len(arr.shape) == 3:
            plt.imshow(arr)
        elif len(arr.shape) == 4:
            plt.imshow(arr[0])
