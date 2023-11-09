import os

folder_path = r'C:\Users\Lenovo\Desktop\rc\yolov5\image_improve\final_img'  # 替换为你的文件夹路径
files = os.listdir(folder_path)

# 遍历文件夹内的文件
for index, file in enumerate(files, start=1):
    file_name, file_extension = os.path.splitext(file)
    new_file_name = f"{index}{file_extension}"
    os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_file_name))

print("文件名修改完成。")
