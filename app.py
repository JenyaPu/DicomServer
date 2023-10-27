import os

from matplotlib import pyplot as plt
from pydicom import dcmread
from pydicom.filewriter import write_file_meta_info
from pynetdicom import AE, debug_logger, evt, AllStoragePresentationContexts, ALL_TRANSFER_SYNTAXES

# Enter the IP address of the server here
addr = "127.0.0.1"
port = 11112

folder_dicom = "data"
folder_processed = "data_processed"

debug_logger()


def handle_store(event):
    name_date = event.dataset.StudyDate
    name_time = event.dataset.StudyTime
    name_id = event.dataset.PatientID
    name_full = name_id + "_" + name_date + "_" + name_time
    storage_dir = os.path.join("data", name_date)
    os.makedirs(storage_dir, exist_ok=True)

    f_name = os.path.join(storage_dir, name_full + ".dcm")
    with open(f_name, 'wb') as f:
        f.write(b'\x00' * 128)
        f.write(b'DICM')
        # noinspection PyTypeChecker
        write_file_meta_info(f, event.file_meta)
        f.write(event.request.DataSet.getvalue())

    # extract metadata as txt file and image as png and save them in separate folders
    os.makedirs(os.path.join(folder_processed, name_date, "metadata"), exist_ok=True)
    os.makedirs(os.path.join(folder_processed, name_date, "images"), exist_ok=True)
    with open(os.path.join(folder_processed, name_date, "metadata", name_full + ".txt"), "w") as f2:
        f2.write(str(event.dataset))
    ds = dcmread(f_name)
    arr = ds.pixel_array
    if len(arr.shape) == 3:
        plt.imshow(arr)
    elif len(arr.shape) == 4:
        plt.imshow(arr[0])
    plt.savefig(os.path.join(folder_processed, name_date, "images", name_full + ".png"))
    return 0x0000


ae = AE()
handlers = [(evt.EVT_C_STORE, handle_store)]
storage_sop_classes = [cx.abstract_syntax for cx in AllStoragePresentationContexts]
for uid in storage_sop_classes:
    ae.add_supported_context(uid, ALL_TRANSFER_SYNTAXES)
ae.start_server((addr, port), block=True, evt_handlers=handlers)
