import argparse
from PIL import Image
from os import listdir
from os.path import isfile, join, isdir, basename
import os

#src_folder = r"C:\code\Face\datasets\oren2trump_out384\trainB"
#dst_folder = src_folder + r"_output"


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


def process_images(src, dst):
    only_folders = [src + f for f in listdir(src) if isdir(join(src, f))]
    for current_folder in only_folders:
        # Create output folder
        dst_folder = f"{dst}{basename(current_folder)}"
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        only_files = [current_folder + "\\" + f for f in listdir(current_folder) if isfile(join(current_folder, f))]
        only_files.sort()
        if "train" in basename(current_folder).lower():
            for image_index in range(3, len(only_files)):
                if image_index % 100 == 0:
                    print(f"{basename(current_folder)}, progress - {image_index}/{len(only_files)}")
                new_im = merge_images(only_files[image_index-3:image_index])
                new_im.save(f"{dst_folder}\\{str(image_index-2)}.jpg")
        else:
            for image_index in range(0, len(only_files)):
                if image_index % 100 == 0:
                    print(f"{basename(current_folder)}, progress - {image_index}/{len(only_files)}")
                new_im = merge_images([only_files[image_index]])
                new_im.save(f"{dst_folder}\\{str(image_index)}.jpg")


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--src', required=True, help='path to the input folder')
#parser.add_argument('--out', default='{input_folder}_output', help='path to the output folder')
parser.add_argument('--out', required=True, help='path to the output folder')
opt = parser.parse_args()

process_images(opt.src, opt.out.format(input_folder=opt.src))