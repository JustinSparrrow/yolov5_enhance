import cv2
import os

output_folder = './orignal_img'

def capture_photos():
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    try:
        n=1
        while True:
            # 读取一帧
            ret, frame = cap.read()

            # 显示窗口
            cv2.imshow('Capture Photos', frame)

            # 等待按键操作
            key = cv2.waitKey(1)

            # 如果按下 'q' 键，退出循环
            if key == ord('q'):
                break

            # 如果按下空格键（32对应空格键的ASCII码）
            if key == 32:
                # 生成独一无二的文件名
                filename = f"{n}.jpg"
                n+=1

                # 保存图片到文件夹
                filepath = os.path.join(output_folder, filename)
                cv2.imwrite(filepath, frame)

                print(f"Photo saved: {filename}")

    finally:
        # 释放摄像头并关闭窗口
        cap.release()
        cv2.destroyAllWindows()


# 调用连续拍照函数
capture_photos()

"""
    西巴
    直接修改成相对路径
    西巴罗马
"""
