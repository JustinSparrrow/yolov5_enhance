# yolov5 数据增强

---
## 初始准备
将图片保存在original_img中，将图片标签保存在original_txt中。  

如果需要电脑摄像头进行数据集的收集，[该python文件](take_photo.py)可以用来进行图片拍摄，只需要将output_folder设置成original_img文件夹即可。

yolo格式标签需要自己去进行数据标注。

---
## coco数据集增强
该种数据增强的思路是改变物体所在的背景将数据总量进行扩张，将物体从原本图片抠出来再粘贴至coco数据集中，可以实现数据集的扩增。  

所需要用到的python文件：[coco数据增强](backgroundSwitch_ImageEnhancement.py)  
coco[数据集位置](coco_images)

**需要注意的是各个路径是否正确**  

## xml版数据增强
这种方法用的是开源项目，源代码链接为[YOLO数据集实现数据增强的方法（裁剪、平移 、旋转、改变亮度、加噪声等）](https://blog.csdn.net/weixin_43334693/article/details/131744918?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522169951716216800215059002%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=169951716216800215059002&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-131744918-null-null.142%5Ev96%5Epc_search_result_base4&utm_term=%E6%95%B0%E6%8D%AE%E5%A2%9E%E5%BC%BA&spm=1018.2226.3001.4187)

具体文件内容如何写可以自己去读代码。  

1. 需要注意的是，该种方法是通过修改xml上的标记内容来进行图形变换的，所以在使用之前我们需要将txt内yolo格式的文件全部转换为xml文件，具体代码参考[yolo -> xml](yolo_txtToXml.py)  

2. 转换成xml文件后，直接放进数据增强代码中运行即可，仍然记住文件夹路径一定要正确 [img_enhance](imageEnhance.py)  

3. 数据增强后标签文件依然是xml文件，但是yolo需要的是yolo格式文件，所以需要将其转换为yolo格式的txt文件，[xml -> yolo](xmlToYolo.py)  

在这个过程中可能会有命名不恰当的地方，因为训练过程要求图片名称与标签名称要一模一样，代码[nameChange.py](nameChange.py)和[nameChangeTxtToJpg.py](nameChangeTxtToJpg.py)就是解决对应问题的。  

---
最后将数据集分成训练集和验证集放进train里面就可以了。
