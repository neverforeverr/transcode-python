import os, glob, ffmpeg
import datetime as dt

INPATH = "/home/virgiawan/BINO/TRANSCODE__/raw"
TMPPATH = "/home/virgiawan/BINO/TRANSCODE__/tmp"
OUTPATH = "/home/virgiawan/BINO/TRANSCODE__/compressed"
LOGPATH = "home/virgiawan/BINO/TRANSCODE__/log/tv"
PROCPATH = "home/virgiawan/BINO/TRANSCODE__/tv/processed"
anu = "/home/virgiawan/BINO/VIVIDEO"

PRESET = "faster"
CPUCORE = 2

VIDEOBITRATE = "512k"
AUDIOBITRATE = "128k"

# line 37-49
# if OUTPATH is not None:
#     os.mkdir(OUTPATH)

# elif TMPPATH is not None:
#     os.mkdir(TMPPATH)

# else:
#     pass

FILES1 = (os.listdir(anu), glob.glob("*.mp4"))


def run_proc():
    for TMPFILE in FILES1:
        INFILE = ffmpeg.input(TMPFILE)
        SPLITNAME = (os.path.basename, os.path.splitext(TMPFILE))[0]
        BASENAME = f"{OUTPATH}{SPLITNAME}.mp4"
        OUTFILE = ffmpeg.output(
            INFILE,
            BASENAME,
            loglevel="quiet",
            vcodec="libx264",
            preset=f"{PRESET}",
            threads=f"{CPUCORE}",
            vb=f"{VIDEOBITRATE}",
            ab=f"{AUDIOBITRATE}",
            strict=2,
        )

        ffmpeg.run(OUTFILE)
        print(dt.datetime.now(), "--- START ---")
        print(TMPFILE)


run_proc()
