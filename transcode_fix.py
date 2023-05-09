import os, glob
import ffmpeg
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

TMPMYMAP1 = {}
TMPMYMAP2 = {}
SORTFILES1 = {}
FILES = {}


# line 37-49
# if OUTPATH is not None:
#     os.mkdir(OUTPATH)

# elif TMPPATH is not None:
#     os.mkdir(TMPPATH)

# else:
#     pass

FILES1 = (os.listdir(anu), glob.glob("*.mp4"))


def run_proc():
    try:
        for TMPFILE in FILES1:
            for VIDEO in TMPFILE:
                INFILE = ffmpeg.input(VIDEO)
                BASENAME = os.path.basename(VIDEO)
                OUTFILE = ffmpeg.output(
                    INFILE,
                    # OUTPATH,
                    f"{OUTPATH}{BASENAME}",
                    loglevel="quiet",
                    vcodec="libx264",
                    preset=f"{PRESET}",
                    threads=f"{CPUCORE}",
                    vb=f"{VIDEOBITRATE}",
                    ab=f"{AUDIOBITRATE}",
                    strict=2,
                )
                # print(BASENAME)

                ffmpeg.run(OUTFILE)
                print(dt.datetime.now(), "--- START ---")

    except ffmpeg.Error as e:
        print("stdout FFMpeg Error")
        print(e.stdout)
        print("stderr FFMpeg Error")
        print(e.stderr)


run_proc()
