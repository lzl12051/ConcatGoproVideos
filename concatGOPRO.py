import os
import shutil
import sys

# install PySimpleGUI if not installed
try:
    import PySimpleGUI as sg
except ImportError:
    print("Looks like you don't have PySimpleGUI installed, do you want me to install for you?\nyes/no")
    yes_or_no = input()
    if yes_or_no in ('yes', 'YES', 'Y', 'y', 'Yes'):
        os.system('pip install pysimplegui')
        import PySimpleGUI as sg
    else:
        raise ImportWarning('No PySimpleGUI package found')


def get_video_list(folder: str):
    all_videos = dict()
    video_formats = {"mp4", "MP4"}
    all_files = os.listdir(folder)
    for file_name in all_files:
        try:
            is_g = file_name[0]
            code_type = file_name[1]
            ext_name = file_name[-3:]
            video_idx = file_name[4:8]
        except IndexError:
            continue
        # GoPro files start with "G"
        if is_g == 'G' and ext_name in video_formats:
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
        event = sg.popup_yes_no("The output folder doesn't exist, create it?")
        if event == 'Yes':
            try:
                os.mkdir(output_dir)
            except:
                raise OSError("Faild to create the output folder.")
        else:
            return False
    return True


def concat_videos(source_dir, output_dir):
    if path_validation(source_dir, output_dir):
        os.chdir(output_dir)
        videos = get_video_list(source_dir)
        sliced_video_num = 0
        # Temp folder to store the .join file for FFmpeg
        try:
            os.mkdir("temp")
        except FileExistsError:
            pass
        for name in videos.keys():
            # if it is a sliced video
            if len(videos[name][0]) > 1:
                sliced_video_num += 1
                os.chdir(output_dir+"/temp")
                # create .join file which includes all chapters of the video
                with open(f"{name}.join", 'w') as file:
                    chapters = videos[name][0]
                    for c in chapters:
                        file.write(f"file '{source_dir}/{c}'\n")
                # Call FFmpeg to concatenate those videos
                status = os.system(
                    f"ffmpeg -f concat -safe 0 -i {name}.join -c copy ../GX01{name}.mp4")
                if status:
                    raise OSError("Something Goes Wrong With FFmpeg.")
            # if it is a single video file, copy to the output folder
            else:
                print(videos)
                shutil.copyfile(
                    f'{source_dir}/{videos[name][0][0]}', output_dir+'/'+videos[name][0][0])
        # clean temp folder
        os.chdir(output_dir)
        print(output_dir)
        try:
            shutil.rmtree('temp')
        except FileNotFoundError:
            print("Failed to clean temp folder")
            pass
        sg.Window('Done', [[sg.T(f"Detected {len(videos.keys())} videos, {sliced_video_num} are(is) sliced.")], [
            sg.Ok()]], disable_close=True).read(close=True)
    else:
        sg.popup_ok("Invalid Path")
        raise FileNotFoundError("Invalid Path")


if __name__ == "__main__":
    # if using CLI mode
    try:
        _, source_dir, output_dir = sys.argv
        concat_videos(source_dir, output_dir)
    # start GUI
    except ValueError:
        sg.theme('SystemDefault')  # please make your windows colorful
        # input_dir, output_dir = '', ''
        layout = [[sg.Text(' Input Folder', size=(10, 1)), sg.InputText(), sg.FolderBrowse()],
                      [sg.Text('Output Folder', size=(10, 1)), sg.InputText(), sg.FolderBrowse()],
                      [sg.Ok()]]
        window = sg.Window('GoPro Video Concatenation', layout)
        while True:

            event, values = window.read()
            if event == 'Ok':
                input_dir, output_dir = values[0], values[1]
                # check if it is empty string
                if input_dir and output_dir and path_validation(input_dir, output_dir):
                    if input_dir == output_dir:
                        event = sg.popup_yes_no("Can't output to the same folder as input, please change the output folder."
                                                "Or press Yes to create an output folder")
                        if event == "Yes":
                            os.chdir(input_dir)
                            try:
                                os.mkdir('Output')
                            except FileExistsError:
                                pass
                            output_dir += '/Output'
                        else:
                            continue
                    concat_videos(input_dir, output_dir)
                    window.close()  # job done
                else:
                    sg.popup_ok("Please input valid paths")
            elif event == sg.WIN_CLOSED:
                window.close()
                break