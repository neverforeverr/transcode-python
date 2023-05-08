import shutil
import ffmpeg
import glob
import os 


dir_raw = "/home/virgiawan/Video/1_RAW/*.mp4"
list_raw = glob.glob(dir_raw)

dir_tmp = "/home/virgiawan/Video/2_TMP/"
dir_tmp_file = "/home/virgiawan/Video/2_TMP/*.mp4"
list_tmp = glob.glob(dir_tmp_file)  

dir_hasil = "/home/virgiawan/Video/3_HASIL/"  
list_hasil = os.listdir(dir_hasil)


for i in list_raw:
  shutil.copy(i, dir_tmp)
  file_masuk = ffmpeg.input(i)
  basename = os.path.basename(i)
  generate_filename = os.path.splitext(basename)[0]
  f = f'{dir_hasil}{generate_filename}'
  file_result = ffmpeg.output(file_masuk, f + '.mp4'  , loglevel='verbose', vcodec='libx264', vb='512k', acodec='aac', ab='128k', fpsmax=30, t=10)
  ffmpeg.run(file_result)
  print('\n======= OK =======\n')

      


