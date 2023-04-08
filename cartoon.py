import argparse
from pathlib import Path

import cv2

from utils import read_img, edge_detection, color_quantisation

LINE_WIDTH = 9
BLUR_VALUE = 7
TOTAL_COLORS = 9


def cartoonify_image(input_path: str, result_dir: str) -> str:
    """
    Takes an input image and applies cartoonify effect on it.
    Returns the path of the saved image.
    """
    out_dir = Path(result_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    img = read_img(input_path)

    edgeImg = edge_detection(img, LINE_WIDTH, BLUR_VALUE)
    img = color_quantisation(img, TOTAL_COLORS)
    blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200, sigmaSpace=200)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edgeImg)

    out_path = out_dir / Path(input_path).name
    cv2.imwrite(str(out_path), cv2.cvtColor(cartoon, cv2.COLOR_RGB2BGR))
    return str(out_path)


def parse_arguments():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description="Cartoonify Face Images")
    parser.add_argument(
        "--input_path",
        default="./temp/image.jpg",
        type=str,
        help="Directory of input images or path of single image",
    )
    parser.add_argument(
        "--result_dir",
        default="./temp/",
        type=str,
        help="Directory for restored results",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    out_path = cartoonify_image(args.input_path, args.result_dir)
    print(f"Cartoonify effect applied on {args.input_path}. Saved to {out_path}.")
