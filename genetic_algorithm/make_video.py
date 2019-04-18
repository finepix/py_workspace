import cv2


def make_video(cross_pro, mutation_pro, its, fps=8, size=(640, 480)):
    # fps = 8
    # size = (640, 480)

    # cross_pro = 0.5
    # mutation_pro = 0.01

    # video_file_name = 'video/improve_cross_' + str(cross_pro) + '_mutation_' + str(mutation_pro) + '.avi'
    video_file_name = 'video/IGA_v3_cross_' + str(cross_pro) + '_mutation_' + str(mutation_pro) + '_3.avi'
    video_writer = cv2.VideoWriter(video_file_name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)

    print('start to write video:')
    for i in range(its):
        file_name = 'ga_process/' + 'iter_' + str(i) + '.jpg'
        print('read file: {}'.format(file_name))
        img = cv2.imread(file_name)
        video_writer.write(img)
    print('done.')


if __name__ == '__main__':
    cro_pro = 0.5
    mut_pro = 0.001

    make_video(cro_pro, mut_pro, 14, fps=4)
