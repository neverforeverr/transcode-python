import os
import ffmpeg
from ffmpeg import Error
import datetime as dt


INPATH = "/home/virgiawan/BINO/TRANSCODE__/raw"
TMPPATH = "/home/virgiawan/BINO/TRANSCODE__/tmp"
OUTPATH = "/home/virgiawan/BINO/TRANSCODE__/compressed"
LOGPATH = "/home/virgiawan/BINO/TRANSCODE__/log/tv"
PROCPATH = "/home/virgiawan/BINO/TRANSCODE__/tv/processed"
ANU = "/home/virgiawan/BINO/VIVIDEO"

PRESET = "faster"
CPUCORE = 1

VIDEOBITRATE = "512k"
AUDIOBITRATE = "128k"

# TMPMYMAP1 = {}
# TMPMYMAP2 = {}
# SORTFILES1 = {}
# FILES = {}

if not os.path.exists(INPATH):
    os.makedirs(INPATH)

elif not os.path.exists(TMPPATH):
    os.makedirs(TMPPATH)

elif not os.path.exists(OUTPATH):
    os.makedirs(OUTPATH)

elif not os.path.exists(LOGPATH):
    os.makedirs(LOGPATH)

elif not os.path.exists(PROCPATH):
    os.makedirs(PROCPATH)

else:
    print("== Dir sudah ada ==")


PATTERN = [".mp4", ".ts", ".mpg", ".TS", ".mkv"]


FILES1 = [file for file in os.listdir(ANU) if file.endswith(tuple(PATTERN))]


def run_proc():
    try:
        # for TMPFILE in FILES1:
        for VIDEO in FILES1:
            INFILE = ffmpeg.input(VIDEO)
            BASENAME = os.path.basename(VIDEO)
            OUTFILE = ffmpeg.output(
                INFILE,
                f"{OUTPATH}{BASENAME}",
                loglevel="quiet",
                vcodec="libx264",
                preset=f"{PRESET}",
                threads=f"{CPUCORE}",
                vb=f"{VIDEOBITRATE}",
                ab=f"{AUDIOBITRATE}",
                strict=2,
            )
            ffmpeg.run(OUTFILE, capture_stdout=True, capture_stderr=True)
            # print(dt.datetime.now(), "--- START ---")

    except Error as e:
        print(e.stderr)


run_proc()
