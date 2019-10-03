from multiprocessing import Process
from google_drive_downloader import GoogleDriveDownloader as gdd
from pathlib import Path

if not Path("data/model").exists():
    processes = []
    kwargs_list = [
        {
            "file_id": '1-J41m1vFJzmO32CPHShY9hk6b1NAvxNI',
            "dest_path": 'data/model/23919/config.json'
        },
        {
            "file_id": '11TmM1Bo-EHUflNWg83PDMLXcycmcIfTe',
            "dest_path": 'data/model/28919/config.json'
        }
    ]

    for d in kwargs_list:
        processes.append(
            Process(target=gdd.download_file_from_google_drive, kwargs=d))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    processes = []
    kwargs_list = [
        {
            "file_id": '1-Ih2nLJ8S9a30AKne_447v9Sy2qIGcVJ',
            "dest_path": 'data/model/23919/pytorch_model.bin'
        },
        {
            "file_id": '11bi0zW7CnDCIAwPHO8S7fAGC-_J59ZJn',
            "dest_path": 'data/model/28919/pytorch_model.bin'
        }
    ]

    for d in kwargs_list:
        processes.append(
            Process(target=gdd.download_file_from_google_drive, kwargs=d))

    for p in processes:
        p.start()

    for p in processes:
        p.join()
