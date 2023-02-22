from cv2 import imshow
import numpy as np
import cv2
import random
from scipy import misc
from matplotlib import pyplot as plt
from PIL import Image
import math


def transform_images(number_of_images, img):
    rows, cols = img.shape[:2]
    transformed_images = []
    # this dont work, change it

    grey_im = Image.fromarray(img).convert('L')
    grey_im = np.array(grey_im)
    for i in range(number_of_images):
        # Randomly select a degree of rotation
        angle = random.uniform(-90, 90)
        rot_mat = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)

        # Randomly select a scaling factor
        scale = random.uniform(0.5, 1.5)
        sc_mat = np.array([[scale, 0, 0], [0, scale, 0]], dtype=np.float32)

        # Randomly select a translation factor
        tx = random.uniform(-cols * 0.2, cols * 0.2)
        ty = random.uniform(-rows * 0.2, rows * 0.2)
        tr_mat = np.array([[1, 0, tx], [0, 1, ty]], dtype=np.float32)

        # Combine the transformation matrices
        combined_mat = rot_mat  # rot_mat @ sc_mat.transpose() @ tr_mat

        # Perform the affine transformation
        transformed_image = cv2.warpAffine(grey_im, combined_mat, (cols, rows))

        transformed_image = Image.fromarray(transformed_image).convert('L')
        transformed_image = np.array(transformed_image)
        plt.imshow(transformed_image, cmap=plt.get_cmap('gray'))
        plt.show()

    return transformed_images


def crop_image(img, x, y, width, height):
    x = max(x,0)
    x = min(x,len(img[0]))
    y = max(y,0)
    y = min(y,len(img))
    return img[y:y+height, x:x+width]


def rotate_image(image, angle, origin):

    rot_mat = cv2.getRotationMatrix2D(origin, angle, 1.0)
    result = cv2.warpAffine(
        image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result



def rnd(low, high):
    return random.uniform(low, high)


def get_augmented_images_cropped(number_of_images, img, crop_data):

    x, y, w, h = crop_data
    origin = (x + w//2, y+h//2)
    rows, cols = img.shape[:2]
    augmented_images_cropped = []

    img_cropped = crop_image(img, x, y, w, h)

    # Flip images veritically and horizontally
    flipped_image_horizontal = cv2.flip(img_cropped, 1)
    flipped_image_vertical = cv2.flip(img_cropped, 0)
    augmented_images_cropped.append(flipped_image_horizontal)
    augmented_images_cropped.append(flipped_image_vertical)

    

    # Blur
    ksize = (15, 15)
    blurred_image = cv2.blur(img_cropped, ksize)
    augmented_images_cropped.append(blurred_image)

    # Blur
    ksize = (30, 30)
    blurred_image = cv2.blur(img_cropped, ksize)
    augmented_images_cropped.append(blurred_image)

    # Sharpen
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened_image = cv2.filter2D(img_cropped, -1, kernel)
    augmented_images_cropped.append(sharpened_image)

    grey_im = Image.fromarray(img).convert('L')
    grey_im = np.array(grey_im)
    for i in range(number_of_images-4):
        # Randomly select a degree of rotation
        angles = [rnd(-45, -20), rnd(20, 45)]

        idx = int(round(rnd(0, 1)))
        angle = angles[idx]

        # Rotate
        rot_image = crop_image(rotate_image(img, angle, origin), x, y, w, h)
        augmented_images_cropped.append(rot_image)

    return [img_cropped] + augmented_images_cropped


def get_selected_region_from_frame(frame):
    x, y, width, height = cv2.selectROI(frame)

    return (x, y, width, height)
