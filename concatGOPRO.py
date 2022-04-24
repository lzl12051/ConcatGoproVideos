import os
import sys
import shutil
import PySimpleGUI as sg


def getVideoList(dir: str) -> dict[list[list, str]]:
    all_videos = dict()
    video_formats = set(["mp4", "MP4"])
    all_files = os.listdir(dir)
    for file_name in all_files:
        try:
            isG = file_name[0]
            code_type = file_name[1]
            ext_name = file_name[-3:]
            # video_chapter = file_name[2:4]
            video_idx = file_name[4:8]
        except IndexError:
            continue
        # GoPro files start with "G"
        if isG == 'G' and ext_name in video_formats:
            try:
                all_videos[video_idx][0].append(file_name)
            except KeyError:
                all_videos[video_idx] = [[file_name], code_type]
    # sort the chapters
    for video in all_videos.keys():
        all_videos[video][0] = sorted(all_videos[video][0])
    return all_videos


def pathValidation(source_dir, output_dir):
    if not os.path.isdir(source_dir):
        return False
    if not os.path.isdir(output_dir):
        try:
            os.mkdir(output_dir)
        except:
            raise OSError("Faild to create the output folder.")
    return True


def doTheJob(source_dir, output_dir):
    if pathValidation(source_dir, output_dir):
        videos = getVideoList(source_dir)
        chaptered_video_num = 0
        # print(videos)
        try:
            os.mkdir("temp")
        except FileExistsError:
            pass
        for name in videos.keys():
            if len(videos[name][0]) > 1:
                chaptered_video_num += 1
                os.chdir(output_dir)
                os.chdir("temp")
                with open(f"{name}.join", 'w') as file:
                    chapters = videos[name][0]
                    for c in chapters:
                        file.write(f"file '{source_dir}/{c}'\n")
                status = os.system(
                    f"ffmpeg -f concat -safe 0 -i {name}.join -c copy ../GX01{name}.mp4")
                if status:
                    raise OSError("Something Goes Wrong With FFmpeg.")

        os.chdir(output_dir)
        try:
            shutil.rmtree('temp')
        except FileNotFoundError:
            pass
        sg.Window('Done', [[sg.T(f"Detected {len(videos.keys())} videos, {chaptered_video_num} are(is) chaptered.")], [
                  sg.Ok()]], disable_close=True).read(close=True)
    else:
        sg.popup_error("Invalid Path")
        raise FileNotFoundError("Invalid Path")


if __name__ == "__main__":
    try:
        _, source_dir, output_dir = sys.argv
        doTheJob(source_dir, output_dir)
    except ValueError:
        doTheJob(sg.popup_get_folder('Please enter an input path'),
                 sg.popup_get_folder('Please enter an output path'))
