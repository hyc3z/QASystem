import shutil
import os
import datetime
import time
import tarfile


def make_tarxz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:xz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def print_time_diff(taskstr, start, finish):
    minutes = int((finish - start) / 60)
    seconds = int((finish - start) - 60 * minutes)
    string = "{} Spent: {} min {} secs.".format(taskstr, minutes, seconds)
    print(string)
    return string


def get_datetime_string_now():
    now = datetime.datetime.now()
    date = now.date()
    timeobj = now.time()
    timestr = "{0:02d}{1:02d}{2:02d}".format(timeobj.hour, timeobj.minute, timeobj.second)
    return timestr


def main(make_release=True,make_source=True):
    start_time = time.time()
    cur_dir = "."
    entrance_file = "main.py"
    work_dir = "./build"
    dist_dir = "./dist"
    icon_file = "logo.ico"
    src_dir = "./src"
    copy_dir = [
        "jieba",
        "light",
    ]
    copy_file = [
        "qms_ok.csv",
        "user_dict.txt",
        "light.qss",
        "back3.jpg",
        "Q14.ico",
        "logo.ico",
    ]
    src_file = [
        "main.py",
        "qms_ok.csv",
        "user_dict.txt",
    ]
    if os.path.exists(work_dir):
        if os.path.isdir(work_dir):
            shutil.rmtree(work_dir)
    if os.path.exists(dist_dir):
        if os.path.isdir(dist_dir):
            shutil.rmtree(dist_dir)
    if os.path.exists(src_dir):
        if os.path.isdir(src_dir):
            shutil.rmtree(src_dir)
    os.mkdir(work_dir)
    os.mkdir(dist_dir)
    os.mkdir(src_dir)
    os.system("chcp 65001")
    os.system(""" pyinstaller "{}" --clean --windowed --distpath="{}" -i {}""".format(
            os.path.join(cur_dir, entrance_file),
            os.path.join(cur_dir, dist_dir),
            os.path.join(cur_dir, icon_file),
        )
    )
    dist_subdir = os.listdir(dist_dir)
    if(len(dist_subdir)) != 1:
        return 2
    exe_dir = os.path.join(dist_dir,dist_subdir[0])
    for i in copy_dir:
        target_dir = os.path.join(exe_dir,i)
        if os.path.exists(target_dir):
            if os.path.isdir(target_dir):
                shutil.rmtree(target_dir)
        try:
            shutil.copytree(i, os.path.join(exe_dir,i))
        except Exception as e:
            print(e)
    for i in copy_file:
        target_dir = os.path.join(exe_dir, i)
        if os.path.exists(target_dir):
            if os.path.isfile(target_dir):
                os.remove(target_dir)
        try:
            shutil.copyfile(i, os.path.join(exe_dir, i))
        except Exception as e:
            print(e)
    timestr = get_datetime_string_now()
    for i in src_file:
        target_dir = src_dir
        try:
            shutil.copyfile(i, os.path.join(target_dir, i))
        except Exception as e:
            print(e)
    for i in copy_dir:
        target_dir = src_dir
        try:
            shutil.copytree(i, os.path.join(target_dir, i))
        except Exception as e:
            print(e)
    # shutil.make_archive("{}-{}-{}".format(dist_subdir[0],date,timestr), "zip", exe_dir)
    now = datetime.datetime.now()
    date = now.date()
    generate_finish = time.time()
    print_time_diff(finish=generate_finish, start=start_time, taskstr="Generating")
    if make_source:
        print("Making source tar.xz archive...")
        print("WARNING: It's going to take a long time.")
        make_tarxz("{}-{}-{}.{}".format("source", date, timestr, "tar.xz"), src_dir)
        finish_time = time.time()
        print_time_diff(finish=finish_time, start=generate_finish, taskstr="Compressing source")
    if make_release:
        print("Making release tar.xz archive...")
        print("WARNING: It's going to take a long time.")
        make_tarxz("{}-{}-{}.{}".format(dist_subdir[0], date, timestr, "tar.xz"), exe_dir)
        finish_time_2 = time.time()
        print_time_diff(finish=finish_time_2, start=finish_time, taskstr="Compressing release")

if __name__ == '__main__':
    main(make_release=False, make_source=True)
