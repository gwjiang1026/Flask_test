# -*- coding: utf-8 -*-
import os
import logging
import time
import numpy as np
import cv2
from flask_app import app, api_bp
from .utils import *
import sys
import base64
import PIL.Image as Image
import sys
import io
import base64
import time
import numpy as np
from flask import current_app, Blueprint, jsonify, request
from io import BytesIO
os.chdir("/app")
sys.path.append('/app')# YOLO V4 model switch
import darknet as dn 
import cv2
logger = logging.getLogger(__name__)

        
def loadYoloModel(model):
    model_net = None
    model_meta = None

    if model == "wheelchair":
        cfg = "../opt/yolo_weight/wheelchair.cfg"
        weight = "../opt/yolo_weight/wheelchair.weights"
        data = "../opt/yolo_weight/wheelchair.data"
    elif model == "pose":
        cfg = "../opt/yolo_weight/pose.cfg"
        weight = "../opt/yolo_weight/pose.weights"
        data = "../opt/yolo_weight/pose.data" 
    
    try:  
    
        model_net, class_names, class_colors = dn.load_network(cfg,  data, weight, batch_size=1)
        model_meta = dn.load_meta(data.encode('utf-8'))
        
    except Exception as err:
        print("[Error] loading {} model fail.".format(model))
        print(err)

    return model_net,model_meta,class_names, class_colors
print("load model.")    

model_net_1,model_meta_1,class_names_1, class_colors_1 = loadYoloModel("wheelchair")  
model_net_2,model_meta_2,class_names_2, class_colors_2 = loadYoloModel("pose")  
#------------------


@api_bp.route('/PredictWheelchair', methods=['GET', 'POST'])
def PredictWheelchair():
    try:

        start = time.time()
        
        img_bytes = request.files['image'].read()
        filename = 'predict.jpg'  
        
      ##待修改
        image = Image.open(io.BytesIO(img_bytes))
        image.save(filename)
      
            
        im = dn.load_image(filename.encode('utf-8'), 0, 0)
        detections = dn.detect_image(model_net_1, class_names_1, im, thresh=0.7)

        output={ 'status': "100" }
        res_objects = []
        
        for detection in detections:
            x, y, w, h = detection[2][0], \
                         detection[2][1], \
                         detection[2][2], \
                         detection[2][3]
            conf = detection[1]
            
            print(conf)
            
            #x *= width / dn.network_width(model_net_1)
            #w *= width / dn.network_width(model_net_1)
            #y *= height / dn.network_height(model_net_1)
            #h *= height / dn.network_height(model_net_1)
            
            
            #xyxy = np.array([x - w / 2, y - h / 2, x + w / 2, y + h / 2])
            #label = detection[0].decode()
            label = detection[0]
            #label = f'{label} {conf:.2f}'
            #print(label)
            res_object = {}
            res_object['label'] = label
            res_object['conf'] = round(float(conf),2)
            res_object['objectRectangle'] =  {
                "top": round(y,2),
                "left": round(x,2),
                "width": round(w,2),
                "height": round(h,2)
                }
            
            res_objects.append(res_object)

        output['status'] = 0
        output['status'] = 0
        output['predict'] = res_objects
        end = time.time()
        print(end - start)
        return jsonify(output)
    except Exception as err:
        logger.error("Fatal error in %s", err, exc_info=True)
        status = {"Fatal": str(err)}
        return jsonify(status)
    
@api_bp.route('/PredictPose', methods=['GET', 'POST'])
def PredictPose():
    try:

        start = time.time()
        
        img_bytes = request.files['image'].read()
        filename = 'predict.jpg'  
        
      ##待修改
        image = Image.open(io.BytesIO(img_bytes))
        image.save(filename)
      
            
        im = dn.load_image(filename.encode('utf-8'), 0, 0)
        detections = dn.detect_image(model_net_2, class_names_2, im, thresh=0.8)

        output={ 'status': "100" }
        res_objects = []
        
        for detection in detections:
            x, y, w, h = detection[2][0], \
                         detection[2][1], \
                         detection[2][2], \
                         detection[2][3]
            conf = detection[1]
            
            print(conf)
            
            #x *= width / dn.network_width(model_net_1)
            #w *= width / dn.network_width(model_net_1)
            #y *= height / dn.network_height(model_net_1)
            #h *= height / dn.network_height(model_net_1)
            
            
            #xyxy = np.array([x - w / 2, y - h / 2, x + w / 2, y + h / 2])
            #label = detection[0].decode()
            label = detection[0]
            #label = f'{label} {conf:.2f}'
            #print(label)
            res_object = {}
            res_object['label'] = label
            res_object['conf'] = round(float(conf),2)
            res_object['objectRectangle'] =  {
                "top": round(y,2),
                "left": round(x,2),
                "width": round(w,2),
                "height": round(h,2)
                }
            
            res_objects.append(res_object)

        output['status'] = 0
        output['status'] = 0
        output['predict'] = res_objects
        end = time.time()
        print(end - start)
        return jsonify(output)
    except Exception as err:
        logger.error("Fatal error in %s", err, exc_info=True)
        status = {"Fatal": str(err)}
        return jsonify(status)
    
@api_bp.route('/hello', methods=['GET'])
def hello():
    try:

        detection = [(b'cruth', 0.5050353407859802, (94.2735595703125, 133.45567321777344, 267.7733459472656, 308.9346008300781))]
        detections = [('person', 0.850121259689331, (55.81684494018555, 350.7244873046875, 83.28942108154297, 125.45098876953125)), ('person', 0.7424463033676147, (423.0081481933594, 325.21337890625, 454.625, 314.12713623046875)), ('cup', 0.6773239374160767, (167.36326599121094, 377.0586853027344, 26.889423370361328, 39.0584602355957)), ('person', 0.6160455346107483, (267.4810485839844, 332.66485595703125, 62.76264190673828, 101.07070922851562)), ('tvmonitor', 0.5468893647193909, (266.1971435546875, 301.3278503417969, 40.8376350402832, 48.03203582763672))]
        
        output={ 'status': "100" }
        res_objects = []
        
        for detection in detections:
            
            res_object = {}
            res_object['label'] = label
            res_object['conf'] = round(conf,2)
            res_object['objectRectangle'] =  {
                "top": y,
                "left": x,
                "width": w,
                "height": h
                }
            
            res_objects.append(res_object)
            
        output['status'] = 0
        output['status'] = 0
        output['predict'] = res_objects
        
        return jsonify(output)
    
    except Exception as err:
        logger.error("Fatal error in %s", err, exc_info=True)
        status = {"Fatal": str(err)}
        return jsonify(status)    