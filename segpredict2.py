# segpredict.py
from fastsam import FastSAM, FastSAMPrompt
import torch
import argparse

def main(prompt):
    model = FastSAM('FastSAM-x.pt')
    IMAGE_PATH = './images/latest.jpg'
    DEVICE = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    everything_results = model(
        IMAGE_PATH,
        device=DEVICE,
        retina_masks=True,
        imgsz=1024,
        conf=0.4,
        iou=0.9,
    )
    prompt_process = FastSAMPrompt(IMAGE_PATH, everything_results, device=DEVICE)

    # Use the provided prompt
    ann = prompt_process.text_prompt(text=prompt)

    prompt_process.plot(
        annotations=ann,
        output_path='./output/output.jpg',
        mask_random_color=True,
        better_quality=True,
        retina=False,
        withContours=True,
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastSAM with a text prompt")
    parser.add_argument("--prompt", type=str, required=True, help="Text prompt for object detection")
    args = parser.parse_args()

    main(args.prompt)
