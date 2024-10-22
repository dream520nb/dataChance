'''
该文件用于存储读取类的方法。

readDirToList:用于遍历目标路径下的，全部符合需求的文件
readPptx: 用于读取pptx文件

'''

import os
from tqdm import tqdm
from pathlib import Path


def readDirToList(dir, goal_tybe) -> list:
    '''
    用于遍历目标路径下的，全部符合需求的文件

    参数：
        dir:文件夹
        goal_tybe:目标文件的类型  例： '.nii'

    返回：
        goal_file_list:目标文件路径的列表。

    '''
    try:
        if os.path.isdir(dir):
            pass
        else:
            raise Exception(f'不存在该文件夹{dir}')
    except Exception as e:
        raise e
    # 遍历目标下的全部文件，寻找目标
    goal_file_list = []  # 存储结果
    file_list = os.listdir(dir)
    for file_name in tqdm(file_list, leave=False, colour='YELLOW'):
        if goal_tybe in file_name:
            goal_file = os.path.join(dir, file_name)
            goal_file_list.append(goal_file)
        else:
            not_goal_file = os.path.join(dir, file_name)
            if os.path.isdir(not_goal_file):
                goal_file_list += readDirToList(not_goal_file, goal_tybe)
    return goal_file_list


def readNii(file_path: str):
    '''
    用于读取nii文件

    不能包含中文路径
    '''
    import SimpleITK as sitk
    data = sitk.ReadImage(file_path)
    return data


def readPptx(file_path: str):
    from pptx import Presentation
    return Presentation(file_path)
    pass