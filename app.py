import os

import gradio as gr
import torch


def download_sample_images():
    """Download sample images to use as examples in the Gradio interface."""
    os.makedirs("sample_images", exist_ok=True)
    os.chdir("sample_images")
    os.system("gdown 1LiKfKhksfu8f_A4x-BhOjZgZHADdLdWz -O img1.jpg")
    os.system("gdown 1jJ6uP_bpdnCRqCuiqZjJG8yeexsz6IUp -O img2.jpg")
    os.system("gdown 1usp9c4VcTX2yche5o2WCi7yJw85n_yeZ -O img3.jpg")
    os.chdir("../")


def load_model():
    """Load the Cartoon Face Converter model."""

    model = torch.hub.load(
        "AK391/animegan2-pytorch:main",
        "generator",
        pretrained=True,
        device="cpu",
        progress=False,
    )
    return model


def cartoonify_animeganv2(model, img):
    """Cartoonify an image using the AnimeGANv2 model."""

    face2paint = torch.hub.load(
        "AK391/animegan2-pytorch:main",
        "face2paint",
        size=512,
        device="cpu",
        side_by_side=False,
    )
    return face2paint(model, img)


def inference(img, method):
    """Perform cartoonification on the input image using the specified method."""

    if not os.path.exists("temp"):
        os.system("mkdir temp")

    img.save("temp/image.jpg", "JPEG")

    if method == "Cartoonify AnimeGanV2":
        out = cartoonify_animeganv2(load_model(), img)
        return out
    else:
        os.system(
            "python cartoon.py --input_path 'temp/image.jpg'  --result_dir './temp/'"
        )
        return "temp/image.jpg"


if __name__ == "__main__":
    download_sample_images()
    model = load_model()

    examples = [
        ["sample_images/img1.jpg", "Cartoonify"],
        ["sample_images/img2.jpg", "Cartoonify"],
        ["sample_images/img3.jpg", "Cartoonify"],
    ]

    inference_on = ["Full Resolution Image", "Downsampled Image"]

    title = "Cartoon Face Converter"
    description = """Gradio demo for <b>Cartoon Face Converter</b>.\n """

    article = "<p style='text-align: center'><a href='#'> Cartoon Face Converter </a> | <a href='#'>Github Repo</a></p>"
    gr.Interface(
        inference,
        [
            gr.inputs.Image(type="pil", label="Input"),
            gr.inputs.Radio(
                ["Cartoonify OpenCV", "Cartoonify AnimeGanV2"],
                default="Cartoonify AnimeGanV2",
                label="Method",
            ),
        ],
        gr.outputs.Image(type="filepath", label="Output"),
        title=title,
        description=description,
        article=article,
        theme="huggingface",
        examples=examples,
        allow_flagging=False,
    ).launch()
