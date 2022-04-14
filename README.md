# ConcatGoproVideos
A python script that can help you to concatenate GoPro's 4GB chaptered videos.

The script will scan the file names ([GoPro File naming Convention](https://community.gopro.com/s/article/GoPro-Camera-File-Naming-Convention?language=en_US), e.g. GH011234.mp4) in your input directory (maybe GoPro's TF card) and find out all chaptered videos. And it will generate a file for FFmpeg to concatenate all videos.

# Usage
**FFmpeg must be installed first to use this script.**

```
python3 concatGOPRO.py input_path output_path
```

And go check your output folder!