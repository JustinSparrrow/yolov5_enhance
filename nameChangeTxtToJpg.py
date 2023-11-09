import os

# 指定文件夹路径
folder_path = 'C:/Users/Lenovo/Desktop/rc/yolov5/image_improve/xml/'

# 获取文件夹内所有文件的列表
files = os.listdir(folder_path)

# 循环遍历文件列表
for filename in files:
    if '.txt' in filename:
        # 构建原始文件的完整路径
        original_filepath = os.path.join(folder_path, filename)

        # 构建新文件名，将'.txt'替换为'.jpg'
        new_filename = filename.replace('.txt', '.jpg')

        # 构建新的文件路径
        new_filepath = os.path.join(folder_path, new_filename)

        # 重命名文件
        os.rename(original_filepath, new_filepath)
