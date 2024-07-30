import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def check_alpha(img: np.ndarray):
    contain_translucent = (img[..., 3] < 1) & (img[..., 3] > 0)
    return contain_translucent.any()

def processing_image(img_path):
    img_path = Path(img_path)
    folder = img_path.parent
    img_name = img_path.stem
    img = plt.imread(img_path)
    print("Contain translucency pixels (Before):", check_alpha(img))
    img[..., 3] = np.where(img[..., 3] != 1, 0, 1)
    print("Contain translucency pixels (After):", check_alpha(img))
    plt.imsave(folder.joinpath(f"{img_name} Output.png"), img, dpi=300)
    return

processing_image("C:\\Users\\robwo\\Desktop\CS\\nypd\\Python\\ForceStatGen\\images\\nypdsplash.png")