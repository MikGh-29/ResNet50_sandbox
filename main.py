import torch
from flask import Flask, make_response, jsonify, request, render_template
from torchvision import transforms
import requests
import os
from PIL import Image, UnidentifiedImageError

device = torch.device("cpu")
app = Flask(__name__)

resnet50 = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_resnet50', pretrained=True)
utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_convnets_processing_utils')
resnet50.eval().to(device)


def test(img_path, img):
    transformer = transforms.ToTensor()
    img = transformer(img)
    transforms.Resize((224, 224))(img)
    batch = torch.unsqueeze(img, dim=0).to(device)

    with torch.no_grad():
        output = torch.nn.functional.softmax(resnet50(batch), dim=1)

    result = utils.pick_n_best(predictions=output, n=5)
    string = ""
    for i in range(0, len(result[0])):
        string += result[0][i][0] + ", with possibility " + result[0][i][1] + "; "

    return render_template("result.html", img_src=img_path, result=string)


@app.route("/web", methods=["POST"])
def process():
    path = request.form["img_label"]
    # if not os.path.exists(os.path.abspath(path)) or not os.path.isfile(os.path.abspath(path)):
    #     return make_response(jsonify("No image found in this path"), 404)
    try:
        img = Image.open(requests.get(path, stream=True).raw)
    except UnidentifiedImageError:
        return make_response(jsonify("File is not a valid image"), 400)
    else:
        return test(path, img)


@app.route("/")
def default():
    return render_template("template1.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
