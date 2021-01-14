import argparse
import os
import cv2

PARSE_ARGS_ERROR = 0
IMGSIZE_NOT_REGULAR = 1
SOURCE_NOT_EXISTS = 2


def parse_app_args():
    parser = argparse.ArgumentParser(
        description="Image resize program by Python. (To the same path)")
    parser.add_argument(
        "--size",
        metavar="Size",
        type=str,
        required=True,
        help="The image size of the target. Format: 112*112.",
    )
    parser.add_argument(
        "--source",
        metavar="Source",
        type=str,
        required=True,
        help="Path to the source image.",
    )

    args = parser.parse_args()
    return args


def get_size(size_str):
    try:
        size_list = size_str.split("*")
        height, width = int(size_list[0]), int(size_list[1])
        if height <= 0 or width <= 0:
            return IMGSIZE_NOT_REGULAR
        return height, width
    except Exception:
        return IMGSIZE_NOT_REGULAR


def get_params_from_args(args):
    target_size = get_size(args.size)
    if target_size == IMGSIZE_NOT_REGULAR:
        return PARSE_ARGS_ERROR

    if not os.path.exists(args.source):
        return SOURCE_NOT_EXISTS
    source_path = args.source

    file_name = os.path.basename(source_path)
    target_path = os.path.join(
        os.path.dirname(source_path),
        "resized_" + file_name,
    )
    return target_size, source_path, target_path


def do_resize(target_size, source_path, target_path):
    img = cv2.imread(source_path)
    img = cv2.resize(img, target_size)
    cv2.imwrite(target_path, img)


if __name__ == "__main__":
    args = parse_app_args()
    result = get_params_from_args(args)
    if result == PARSE_ARGS_ERROR:
        print("Parse image size error, bad format.")
        exit(0)
    elif result == SOURCE_NOT_EXISTS:
        print("Source path not exist.")
        exit(0)
    else:
        target_size, source_path, target_path = result
    print("Tranforming", source_path, "to size (", target_size[0], ",", target_size[1], ").")

    try:
        do_resize(target_size, source_path, target_path)
    except Exception:
        print("Image", source_path, "format not supported by OpenCV-Python.")
        exit(0)
    print("Resized image saved to", target_path + ".")
