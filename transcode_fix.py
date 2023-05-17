import os
import ffmpeg
from ffmpeg import Error
import datetime as dt
import time
import shutil
import contextlib


inpath = "/home/virgiawan/BINO/TRANSCODE/raw"
tmppath = "/home/virgiawan/BINO/TRANSCODE/tmp"
outpath = "/home/virgiawan/BINO/TRANSCODE/compressed"
logpath = "/home/virgiawan/BINO/TRANSCODE/log/tv"
procpath = "/home/virgiawan/BINO/TRANSCODE/tv/processed"

preset = "faster"
cpucore = 1

videobitrate = "512k"
audibitrate = "128k"

# TMPMYMAP1 = {}
# TMPMYMAP2 = {}
# SORTFILES1 = {}
# FILES = {}

if not os.path.exists(inpath):
    os.makedirs(inpath)

elif not os.path.exists(tmppath):
    os.makedirs(tmppath)

elif not os.path.exists(outpath):
    os.makedirs(outpath)

elif not os.path.exists(logpath):
    os.makedirs(logpath)

elif not os.path.exists(procpath):
    os.makedirs(procpath)

else:
    print("== Dir sudah ada ==")


pattern = [".mp4", ".ts", ".mpg", ".TS", ".mkv"]


files1 = [file for file in os.listdir(inpath) if file.endswith(tuple(pattern))]


def checkFile():
    for raw in files1:
        with contextlib.suppress(FileNotFoundError):
            while True:
                check_size1 = os.path.getsize(os.path.join(inpath, raw))

                time.sleep(3)

                check_size2 = os.path.getsize(os.path.join(inpath, raw))

                # with contextlib.suppress(shutil.Error):
                if check_size1 == check_size2:
                    shutil.move(os.path.join(inpath, raw), tmppath)
                else:
                    print(f"File {raw} masih dalam proses copy")

    print("selesai")


def run_proc():
    try:
        for tmp in os.listdir(tmppath):
            tmp = os.path.join(tmppath, tmp)

            infile = ffmpeg.input(tmp)
            basename = os.path.basename(tmp)
            outfile = ffmpeg.output(
                infile,
                f"{outpath}/{basename}",
                loglevel="quiet",
                vcodec="libx264",
                preset=f"{preset}",
                threads=f"{cpucore}",
                vb=f"{videobitrate}",
                ab=f"{audibitrate}",
                strict=2,
                t=10,
            )
            print(f"File {tmp} dalam proses transcoding...")
            ffmpeg.run(outfile, capture_stdout=True, capture_stderr=True)
            print(f"File {tmp} selesai proses transcoding")

    except Error as e:
        print(e.stderr)


def storedFile():
    for files in sorted(os.listdir(outpath)):
        basename = files[:-18].lower()
        year = files[-17:-13]
        month = files[-13:-11]
        day = files[-11:-9]

        with contextlib.suppress(FileExistsError):
            match basename:
                case "antv":
                    pspath = f"{outpath}/antv/{year}/{month}/{day}"
                case "bali_tv":
                    pspath = f"{outpath}/bali_tv/{year}/{month}/{day}"
                case "beritasatu":
                    pspath = f"{outpath}/beritasatu/{year}/{month}/{day}"
                case "bn_channel":
                    pspath = f"{outpath}/bn_channel/{year}/{month}/{day}"
                case "btv":
                    pspath = f"{outpath}/btv/{year}/{month}/{day}"
                case "cnbc_indonesia":
                    pspath = f"{outpath}/cnbc_indonesia/{year}/{month}/{day}"
                case "cnn_indonesia":
                    pspath = f"{outpath}/cnn_indonesia/{year}/{month}/{day}"
                case "daai_tv":
                    pspath = f"{outpath}/daai_tv/{year}/{month}/{day}"
                case "garuda_tv":
                    pspath = f"{outpath}/garuda_tv/{year}/{month}/{day}"
                case "global_tv":
                    pspath = f"{outpath}/global_tv/{year}/{month}/{day}"
                case "idx_channel":
                    pspath = f"{outpath}/idx_channel/{year}/{month}/{day}"
                case "indosiar":
                    pspath = f"{outpath}/indosiar/{year}/{month}/{day}"
                case "inewstv":
                    pspath = f"{outpath}/inewstv/{year}/{month}/{day}"
                case "jaktv":
                    pspath = f"{outpath}/jaktv/{year}/{month}/{day}"
                case "jtv":
                    pspath = f"{outpath}/jtv/{year}/{month}/{day}"
                case "kompastv":
                    pspath = f"{outpath}/kompastv/{year}/{month}/{day}"
                case "metrotv":
                    pspath = f"{outpath}/metrotv/{year}/{month}/{day}"
                case "mncnews":
                    pspath = f"{outpath}/mncnews/{year}/{month}/{day}"
                case "mnctv":
                    pspath = f"{outpath}/mnctv/{year}/{month}/{day}"
                case "nettv":
                    pspath = f"{outpath}/nettv/{year}/{month}/{day}"
                case "rcti":
                    pspath = f"{outpath}/rcti/{year}/{month}/{day}"
                case "rtv":
                    pspath = f"{outpath}/rtv/{year}/{month}/{day}"
                case "sctv":
                    pspath = f"{outpath}/sctv/{year}/{month}/{day}"
                case "sea_today":
                    pspath = f"{outpath}/sea_today/{year}/{month}/{day}"
                case "trans7":
                    pspath = f"{outpath}/trans7/{year}/{month}/{day}"
                case "transtv":
                    pspath = f"{outpath}/transtv/{year}/{month}/{day}"
                case "tvone":
                    pspath = f"{outpath}/tvone/{year}/{month}/{day}"
                case "tvrinasional":
                    pspath = f"{outpath}/tvrinasional/{year}/{month}/{day}"
                case _:
                    pspath = f"{outpath}/unknown"

            if not os.path.exists(pspath):
                os.makedirs(pspath)

            shutil.move(os.path.join(outpath, files), pspath)


checkFile()
run_proc()
storedFile()
