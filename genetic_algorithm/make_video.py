import cv2

if __name__ == '__main__':
    fps = 16
    size = (640, 480)
    video_writer = cv2.VideoWriter('ga_process.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)

    for i in range(190):
        file_name = 'ga_process/' + 'iter_' + str(i) + '.jpg'
        img = cv2.imread(file_name)
        video_writer.write(img)
