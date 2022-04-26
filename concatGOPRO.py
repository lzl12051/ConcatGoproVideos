import os
import shutil
import sys

try:
    import PySimpleGUI as sg
except ImportError:
    print("Looks like you don't have PySimpleGUI installed, do you want me to install for you?\nyes/no")
    yes_or_no = input()
    yes_set = {'yes', 'YES', 'Y', 'y', 'Yes'}
    if yes_or_no in yes_set:
        os.system('pip install pysimplegui')
    else:
        raise ImportWarning('No PySimpleGUI package found')


def get_video_list(dir: str):
    all_videos = dict()
    video_formats = {"mp4", "MP4"}
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


def path_validation(source_dir, output_dir):
    if not os.path.isdir(source_dir):
        return False
    if not os.path.isdir(output_dir):
        try:
            os.mkdir(output_dir)
        except:
            raise OSError("Faild to create the output folder.")
    return True


def do_the_job(source_dir, output_dir):
    if path_validation(source_dir, output_dir):
        os.chdir(input_dir)
        videos = get_video_list(source_dir)
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
        sg.Window('Done', [[sg.T(f"Detected {len(videos.keys())} videos, {chaptered_video_num} are(is) sliced.")], [
            sg.Ok()]], disable_close=True).read(close=True)
    else:
        sg.popup_ok("Invalid Path")
        raise FileNotFoundError("Invalid Path")


if __name__ == "__main__":
    try:
        _, source_dir, output_dir = sys.argv
        do_the_job(source_dir, output_dir)
    except ValueError:
        sg.theme('SystemDefault')  # please make your windows colorful

        # layout = [[sg.Text('Input Folder')],
        #           [sg.Input(), sg.FolderBrowse()],
        #           [sg.Text('Output Folder')],
        #           [sg.Input(), sg.FolderBrowse()],
        #           [sg.OK(), sg.Cancel()]]
        layout = [[sg.Text(' Input Folder', size=(10, 1)), sg.InputText(), sg.FolderBrowse()],
                  [sg.Text('Output Folder', size=(10, 1)), sg.InputText(), sg.FolderBrowse()],
                  [sg.Ok(), sg.Cancel()]]

        window = sg.Window('GoPro Video Concatenator', layout)
        event, values = window.read()
        if event == 'OK':
            input_dir, output_dir = values[0], values[1]
            if input_dir == output_dir:
                event = sg.popup_yes_no("Can't output to the same folder as input, please change the output folder.\n"
                                        "Press Yes to create an output folder")
                if event == "Yes":
                    os.chdir(input_dir)
                    try:
                        os.mkdir('Output')
                    except FileExistsError:
                        pass
                    output_dir += '/Output'
                else:
                    window.close()
            do_the_job(input_dir, output_dir)

        elif event in (sg.WIN_CLOSED, 'Cancel'):
            window.close()
