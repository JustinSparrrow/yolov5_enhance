import os
import xml.etree.ElementTree as ET


classes = ["rb", "bb", "rv", "bv", "zz"]  # 类别

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(image_id):
    in_file = os.path.join(xml_path, f'{image_id}.xml')
    out_file = os.path.join(txt_path, f'{image_id}.txt')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open(out_file, 'w') as out:
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out.write(f"{cls_id} {' '.join(map(str, bb))}\n")

xml_path = r'C:\Users\Lenovo\Desktop\rc\yolov5\image_improve\final_xml'  # 替换为XML文件夹的路径
txt_path = r'C:\Users\Lenovo\Desktop\rc\yolov5\image_improve\final_txt'  # 替换为TXT文件夹的路径

# 创建TXT文件夹
if not os.path.exists(txt_path):
    os.makedirs(txt_path)

# 获取XML文件列表
xml_files = os.listdir(xml_path)
xml_files.sort()  # 将文件按照名称排序

# 遍历XML文件并生成对应的TXT文件
for index, xml_file in enumerate(xml_files, start=1):
    file_name = os.path.splitext(xml_file)[0]
    convert_annotation(file_name)
