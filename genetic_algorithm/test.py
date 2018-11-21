import cv2
from genetic_algorithm.GA import GA
from genetic_algorithm.otsu import otsuth

if __name__ == '__main__':
    file_path = 'images\ship_1.jpg'
    image = cv2.imread(file_path)

    model = GA(image, otsuth, 100, 1000)
    model.run()

