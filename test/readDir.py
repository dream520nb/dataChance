# readDir.py
from ..src.dataChance.readFile import readDirToList


def main():
    directory_path = '/path/to/directory'  # 替换为你的目录路径
    files = readDirToList(directory_path)
    print("目录中的文件：", files)


if __name__ == "__main__":
    main()
