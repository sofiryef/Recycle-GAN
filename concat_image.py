import argparse
from PIL import Image
from os import listdir
from os.path import isfile, join, isdir, basename
import os


def get_image_label_from_name(folder_name):
    if 'train' in folder_name:
        # Train picture
        return folder_name.split("train")[1][0]
    else:
        # Test picture
        return folder_name.split("test")[1][0]


def merge_images(images_path_list):
    images = map(Image.open, [im_path for im_path in images_path_list])
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    images = map(Image.open, [im_path for im_path in images_path_list])
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im


def process_images(src, dst, test_percent):
    train_count = {'A': 0, 'B': 0}
    test_count = {'A': 0, 'B': 0}
    only_folders = [src + f for f in listdir(src) if isdir(join(src, f))]
    # Checking if test folders exist
    if test_percent:
        if not os.path.exists(f"{dst}\\testA"):
            os.makedirs(f"{dst}\\testA")
        if not os.path.exists(f"{dst}\\testB"):
            os.makedirs(f"{dst}\\testB")
    for current_folder in only_folders:
        # Create output folder
        dst_folder = f"{dst}\\train{get_image_label_from_name(basename(current_folder))}"
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        only_files = [current_folder + "\\" + f for f in listdir(current_folder) if isfile(join(current_folder, f))]
        only_files.sort()
        if "train" in basename(current_folder).lower():
            test_sampling_rate = int(test_percent)
            for image_index in range(3, len(only_files)):
                # Print progress
                if image_index % 100 == 0:
                    print(f"{basename(current_folder)}, progress - {image_index}/{len(only_files)}")
                # Checking if we should exclude the picture to test
                if image_index % test_sampling_rate < 3:
                    # We shouldn't create a triple train set out of this sample
                    if image_index % test_sampling_rate == 0:
                        # We should save the test image here
                        image_label = get_image_label_from_name(basename(current_folder))
                        new_im = merge_images([only_files[image_index]])
                        new_im.save(f"{dst}\\test{image_label}\\{str(test_count[image_label])}.jpg")
                        test_count[image_label] += 1
                    continue
                # Creating the triplet image
                new_im = merge_images(only_files[image_index-2:image_index+1])
                current_image_label = get_image_label_from_name(basename(current_folder))
                new_im.save(f"{dst_folder}\\{str(train_count[current_image_label])}.jpg")
                train_count[current_image_label] += 1
        else:
            # Here we just translate test images
            for image_index in range(0, len(only_files)):
                if image_index % 100 == 0:
                    print(f"{basename(current_folder)}, progress - {image_index}/{len(only_files)}")
                new_im = merge_images([only_files[image_index]])
                image_label = get_image_label_from_name(basename(current_folder))
                new_im.save(f"{dst}\\test{image_label}\\{str(test_count[image_label])}.jpg")


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--src', required=True, help='path to the input folder')
parser.add_argument('--out', required=True, help='path to the output folder')
parser.add_argument('--test_percent', default=0, help='Percent of data to exclude from train (Use this in case you '
                                                      'dont have test data in the src folder')
opt = parser.parse_args()


if __name__ == '__main__':
    process_images(opt.src, opt.out.format(input_folder=opt.src), opt.test_percent)
