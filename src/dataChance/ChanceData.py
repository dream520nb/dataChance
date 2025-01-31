'''
编写进行格式转换的主类

BatchChanceData:批量格式转换
'''
import os
from concurrent.futures import ThreadPoolExecutor
from .readFile import readDirToList
from pathlib import Path
import sys


def BatchChanceData(input_dir: str, output_dir: str, mode: int | str, dir_keep: bool = True, thread_number=4) -> None:
    '''
    用于批量格式转换
    参数：
        input_dir: 输入文件的主目录
        output_dir: 输出文件的目录
        mode: 转换的模式
        dir_keep: 是否保留原始目录结构
        thread_number: 线程数量
    '''

    # 判断输入值是否符合要求
    if not os.path.isdir(input_dir) or not os.path.isdir(output_dir):
        raise FileNotFoundError('输入路径或者输出路径有误')
    input_dir = str(Path(input_dir))
    output_dir = str(Path(output_dir))

    # 创建线程池
    pool = ThreadPoolExecutor(thread_number)

    # 获得需要转化的文件路径

    match mode:
        case 1 | 'nii2nii.gz':
            input_type = '.nii'
            output_type = '.nii.gz'
        case 2 | 'webm2mp4':
            input_type = '.webm'
            output_type = '.mp4'
        case 3 | 'pptx2pdf' :
            input_type = '.pptx'
            output_type = '.pdf'
        case 4 | 'mp42jpg':
            input_type='.mp4'
            output_type = '/'
        case 5 | 'mp42avi':
            input_type='.mp4'
            output_type='.avi'
        case _:
            raise ValueError('模式不存在')
        

        

    print('获取文件中')
    file_path_list = readDirToList(input_dir, input_type)
    print('获取到的文件有:')
    print('-'*10)
    for file_path in file_path_list:
        print(file_path)
    print('-'*10)

    # 开始格式转换
    futures = []
    for file_path in file_path_list:
        # 获得输出路径
        file_path = str(Path(file_path))
        file_name = os.path.basename(file_path)
        new_file_name = file_name.replace(input_type, output_type)
        if dir_keep:
            new_file_path = file_path.replace(
                input_dir, output_dir, 1)
            new_file_path = new_file_path.replace(
                file_name, new_file_name, -1)
            if not os.path.isdir(os.path.dirname(new_file_path)):
                os.mkdir(os.path.dirname(new_file_path))
        else:
            new_file_path = os.path.join(output_dir, new_file_name)
        # 开始转换
        future = pool.submit(_chanceData, file_path, new_file_path, mode)
        futures.append(future)
        pass

    # 设置线程守护
    pool.shutdown(wait=True)
    return


def _chanceData(input_file_path, output, mode):
    '''
    用于进行单个文件的转换
    参数：
        input_file_path: 输入文件的地址
        output: 输出文件的地址
        mode: 转换模式
    '''
    # 根据转换模式选择转换方法
    try:
        print(f'正在转换文件{input_file_path}')
        match mode:
            case 1 | 'nii2nii.gz':
                chanceDate = __nii2niigz
            case 2 | 'webm2mp4':
                chanceDate = __webm2mp4
            case 3 | 'pptx2pdf' :
                chanceDate = __ppt2pdf
            case 4 | 'mp42jpg' :
                chanceDate = __mp42jpg
            case 5 | 'mp42avi':
                chanceDate = __mp42avi
                pass

        # 转换
        chanceDate(input_file_path, output)
        print(f'{output}转换完成')
    except Exception as e:
        print(e)
    pass

def __mp42avi(input_file_path,output):
    import subprocess
    # 创建ffmpeg命令
    command = [
        'ffmpeg',  # ffmpeg 命令
        '-i', input_file_path,  # 输入文件路径
        output # 输出文件路径
    ]

    # 调用 ffmpeg 执行转换
    try:
        subprocess.run(command, check=True)
        print(f"Conversion successful! Output saved to {output}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    
    pass

def __nii2niigz(input_file_path, output):
    '''
    将nii文件转化为nii.gz文件
    '''
    # 读取文件
    from .readFile import readNii
    data = readNii(input_file_path)
    # 保存文件
    from .writeDataToFile import writeNiigz
    writeNiigz(data, output)
    pass


def __webm2mp4(input_file_path, output):
    '''
    将webm文件转化为mp4文件
    '''
    from moviepy.editor import VideoFileClip
    # 读取文件
    video = VideoFileClip(input_file_path)
    video.write_videofile(output)
    pass

def __ppt2pdf(input_file_path, output):
    '''
    将ppt文件转化为pdf文件
    '''
    from .readFile import readPptx
    from .writeDataToFile import writePdf
    data = readPptx(input_file_path)
    writePdf(data,output)
    pass

def __mp42jpg(input_file_path, output):
    '''
    将mp4文件转化为jpg文件。
    '''
    import cv2
    video_path = input_file_path
    output_folder = output
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    # 检查视频是否成功打开
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
    frame_count = 0
    # 创建文件夹
    if not os.path.isdir(output):
        os.makedirs(output)

    try:
        while True:
            # 读取一帧
            ret, frame = cap.read()
            if not ret:
                break  # 读取结束

            # 保存帧为JPG文件
            frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.jpg')
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
            
    except Exception as e:
        print(f"Error: {e}")
        return False
    # 释放视频对象
    cap.release()
    
    pass