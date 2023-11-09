import cv2
import numpy as np
import random
import os
import math

SOURCE_NUM = 120  #coco数据集里选取的数量
# 首先随机从模板图片里选取球的图片
def select_ball_from_template(template_image_path, template_label_path,BALL_NUM):
    # 读取模板图片
    template_image = cv2.imread(template_image_path)
    # 读取模板图片的球位置信息
    with open(template_label_path, "r") as f:
        template_bboxes = f.readlines()
    # 创建列表来存储球的标号和对应图片
    ball_index= []
    ball_img=[]
    for i in range(BALL_NUM): 
        # 随机选择一个球的位置信息
        random_bbox = random.choice(template_bboxes).split()
        class_id = random_bbox[0]
        x_center = float(random_bbox[1]) * template_image.shape[1]
        y_center = float(random_bbox[2]) * template_image.shape[0]
        width = float(random_bbox[3]) * template_image.shape[1]
        height = float(random_bbox[4]) * template_image.shape[0]

        # 获取球在原有图片中的位置和尺寸
        # (x_min,y_min)：球的左上角坐标
        # (x_max,y_max)：球的右下角坐标
        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)
        # 对球进行缩小
        ball_width = int((x_max - x_min)/3)
        ball_height = int((y_max - y_min)/3)

        # 将截取的球part调整为目标位置和尺寸
        ball = template_image[y_min:y_max, x_min:x_max]
        ball_resized = cv2.resize(ball, (ball_width, ball_height))
        
        ball_index.append(class_id)
        ball_img.append(ball_resized)
    return ball_index,ball_img

# 然后粘贴到一个coco图片中  保存处理后的图片和label标签信息
def paste_to_coco(coco_image_folder,coco_index,ball_index,ball_img,BALL_NUM):

    # 在COCO数据集中随机选择一个图片路径
    coco_image_files = os.listdir(coco_image_folder)
    random_image_file = coco_image_files[coco_index]
    # 读入图片的路径和输出图片的路径和输出图片标签的路径
    coco_image_path = coco_image_folder + '/' + random_image_file
    print(coco_image_path)
    output_fold = "out" + "_" + str(coco_index) + "_" + random_image_file
    output_image_path = coco_outimg_folder + '/' + output_fold
    label_txt_path = coco_label_folder + '/' + output_fold.replace(".jpg", ".txt")
    # 读取COCO图片
    coco_image = cv2.imread(coco_image_path)
    coco_height, coco_width = coco_image.shape[:2]

    ball_centers = []
    ball_radius = []
    for i in range(BALL_NUM):
        # 获取球的图片的宽度和高度
        class_id = ball_index[i]
        ball_resized = ball_img[i]
        ball_height, ball_width = ball_resized.shape[:2]
        while True:
            # 随机选择球在coco图片中的目标位置(并控制其不超出边界范围)
            x_target = random.randint(0, coco_width - ball_width)
            y_target = random.randint(0, coco_height - ball_height)
            overlap = False
            for center,radius in zip(ball_centers,ball_radius):
                if np.linalg.norm(np.array(center) - np.array([x_target + ball_width/2, y_target + ball_height/2])) < radius+math.sqrt((ball_height/2)**2 + (ball_width/2)**2):
                    overlap = True
                    break
            # 如果不重叠，将球粘贴到 COCO 图像上
            if not overlap:
                ball_centers.append([x_target + ball_width/2, y_target + ball_height/2])
                ball_radius.append(math.sqrt((ball_height/2)**2 + (ball_width/2)**2))
                # 将球放置到COCO图片中的目标位置
                coco_image[y_target:y_target+ball_height, x_target:x_target+ball_width] = ball_resized
                # 生成Yolov5标签txt并保存到output_label中
                class_id = int(class_id)
                x_center = float(x_target +  ball_width/ 2) / coco_width
                y_center = float(y_target + ball_height / 2) / coco_height
                width = float(ball_width) / coco_width
                height = float(ball_height) / coco_height
                
                if i == 0:
                    with open(label_txt_path, "w") as f:
                        f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"+"\n")
                else:
                    with open(label_txt_path, "a+") as f:
                        f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"+"\n")
                break
    # 将处理后的图片保存到output_img中      
    cv2.imwrite(output_image_path, coco_image)

    
if __name__ == '__main__':
    # 模板图片路径
    template_image_path = "C:\\Users\\Lenovo\\Desktop\\rc\\yolov5\\image_improve\\orignal_img\\1.jpg"
    # 模板中球的标签位置信息
    template_label_path = "C:\\Users\\Lenovo\\Desktop\\rc\\yolov5\\image_improve\\orignal_txt\\1.txt"
    # COCO数据集路径
    coco_image_folder = "C:\\Users\\Lenovo\\Desktop\\rc\\yolov5\\image_improve\\coco_images\\train2017"   # coco数据集的路径
    # 处理后的结果的存放路径
    coco_label_folder = "./cowandetu"
    coco_outimg_folder = "./cowandetu_xml"
    # 从coco数据集source_img中选取图片进行粘贴

    for coco_index in range(SOURCE_NUM):
        # 调用函数
        #BALL_NUM = random.randint(1, 4)
        BALL_NUM = 1 # 依据实际需求修改

        ball_index,ball_img = select_ball_from_template(template_image_path, template_label_path,BALL_NUM)
        paste_to_coco(coco_image_folder,coco_index,ball_index,ball_img,BALL_NUM)



# 注 ：需修改模板图片和标签的路径
# 功能：可以实现从一张含有多个球的图片中，随机选取该图片中 BALL_NUM个 的球，然后粘贴到 SOURCE_NUM 个coco数据集上
# 缺点是： 每次只能处理一张拍摄的图片
# 可参考需要修改的行数为 第7行、第103行、第105行、第116行
# 第54行是控制输出的img和label的文件命名
# 注意不要重名