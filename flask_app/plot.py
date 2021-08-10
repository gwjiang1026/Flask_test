
import pandas as pd
import json
import requests
file_path = r'C:\Users\GWJIANG\Desktop\GW\python code\yolov4\downloads\val_images\8_data1575.jpg'
url = 'http://34.122.163.27:5000/api/PredictPose?image'
files = {'image': open(file_path, 'rb')}
r = requests.post(url, files=files)
result = json.loads(r.text)

result['predict'][0]['objectRectangle']['height']


print(print(r.text))

from d2l import mxnet as d2l

from mxnet import image, np, npx
npx.set_np()
d2l.set_figsize()
img = image.imread(file_path).asnumpy()
d2l.plt.imshow(img);

x = result['predict'][0]['objectRectangle']['left']
y = result['predict'][0]['objectRectangle']['top']
w = result['predict'][0]['objectRectangle']['width']
h = result['predict'][0]['objectRectangle']['height']

box = [(x - w / 2),(y - h / 2),w,h]


def bbox_to_rect(bbox, color):

    return d2l.plt.Rectangle(xy=(bbox[0], bbox[1]), width=bbox[2],
                             height=bbox[3], fill=False,
                             edgecolor=color, linewidth=2)

fig = d2l.plt.imshow(img)
fig.axes.add_patch(bbox_to_rect(box, 'red'))

