from os import path, listdir, makedirs
import ffmpeg
import shutil
import contextlib

# from filelock import FileLock

# from multiprocessing.pool import ThreadPool
# from concurrent.futures import ThreadPoolExecutor
import time, logging, fcntl
from threading import Thread
from queue import Queue


inpath = "/home/virgiawan/BINO/TRANSCODE/raw"
tmppath = "/home/virgiawan/BINO/TRANSCODE/tmp"
outpath = "/home/virgiawan/BINO/TRANSCODE/compressed"
logpath = "/home/virgiawan/BINO/TRANSCODE/log"
procpath = "/home/virgiawan/BINO/TRANSCODE/tv/processed"

preset = "faster"
cpucore = 2


videobitrate = "512k"
audibitrate = "128k"

# lockfile = open(f"{logpath}/transcoding", "w")

if not path.exists(inpath):
    makedirs(inpath)

elif not path.exists(tmppath):
    makedirs(tmppath)

elif not path.exists(outpath):
    makedirs(outpath)

elif not path.exists(logpath):
    makedirs(logpath)

elif not path.exists(procpath):
    makedirs(procpath)


pattern = [".mp4", ".ts", ".mpg", ".TS", ".mkv"]

files1 = [file for file in listdir(inpath) if file.endswith(tuple(pattern))]

# logging.basicConfig(level=logging.DEBUG, format="%(process)d-%(levelname)s-%(message)s")

# q = Queue(maxsize=2)


def checkInpath(rawIn, rawTmp):
    with contextlib.suppress(FileNotFoundError):
        while True:
            check_size1 = path.getsize(rawIn)
            time.sleep(1)
            check_size2 = path.getsize(rawIn)
            if check_size1 == check_size2:
                shutil.move(rawIn, rawTmp)
                print(f"{rawIn} berhasil dipindah")
                break

            else:
                print(f"{rawIn} sedang proses copy")


def proc():
    for raw in files1:
        rawIn = path.join(inpath, raw)
        rawTmp = path.join(tmppath, raw)
        # rawIn = [path.join(inpath, raw) for raw in files1]
        # rawTmp = [path.join(tmppath, raw) for raw in files1]

        trInpath = Thread(
            target=checkInpath, args=(rawIn, rawTmp), name="Proses Moving Raw"
        )
        trTranscoding = Thread(target=transcoding, name="Transcoding")
        trStoredFile = Thread(target=storedFile, name="Stored File To Directory")

        trInpath.start()
        trInpath.join()

        time.sleep(5)

        trTranscoding.start()
        trTranscoding.join()

        time.sleep(5)

        trStoredFile.start()
        trStoredFile.join()


def transcoding():
    try:
        for tmp in listdir(tmppath):
            tmp = path.join(tmppath, tmp)

            infile = ffmpeg.input(tmp)
            basename = path.basename(tmp)
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
                f="mp4",
            )
            ffmpeg.run(
                outfile, overwrite_output=True, capture_stdout=True, capture_stderr=True
            )

    except ffmpeg.Error:
        with open(f"{logpath}/logError.txt", "w+", encoding="utf-8") as f:
            f.writelines()
            f.close()


#     # finally:
#     #     lockfile.release()


def storedFile():
    # [files for files in sorted(listdir(outpath)) if files.endswith(".mp4")]
    for files in sorted(listdir(outpath)):
        if files.endswith(".mp4"):
            outPath = path.join(outpath, files)
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
                        pspath = str(f"{outpath}/unknown")

                with contextlib.suppress(Exception):
                    if not path.exists(pspath):
                        makedirs(pspath)

                try:
                    shutil.move(outPath, path.join(pspath, files))

                except shutil.Error as e:
                    print(e)
                    # if path.exists(path.join(pspath, files)):
                    #     move(outPath, path.join(pspath, files))


proc()

## lockfile buat lock pid
## .running lock filename untuk diproses
