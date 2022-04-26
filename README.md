# ConcatGoproVideos
A python script that can help you to concatenate GoPro's 4GB sliced videos.

The script will scan the file names ([GoPro File naming Convention](https://community.gopro.com/s/article/GoPro-Camera-File-Naming-Convention?language=en_US), e.g. GH011234.mp4) in your input directory (maybe GoPro's TF card) and find out all chaptered videos. And it will generate a file for FFmpeg to concatenate all videos.

# Usage
**FFmpeg must be installed first to use this script.**
Just run the script file and it will ask you to set the source folder and output folder.
```bash
python3 concatGOPRO.py
```
Or you could use command line interface like below:
```bash
python3 concatGOPRO.py input_path output_path
```
Go check your output folder!