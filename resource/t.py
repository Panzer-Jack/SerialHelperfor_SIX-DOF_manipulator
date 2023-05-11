import PyQt5
import cv2
from personData import *
import paddlehub as hub
# import numpy as np
from pyzbar import pyzbar
import requests
import ast


# TODO
# 1. 人脸识别 记录违反人员
# 2. 口罩识别
# 3. 健康码识别
# 扩展功能 - 红外线测温
# 可部署在 类似树莓派-Linux / STM32单片机




class AI_EP_System:
    def __init__(self, recog_yml):
        self.name = self.frame = self.cap = None
        self.module = hub.Module(name="pyramidbox_lite_mobile_mask")
        self.recog = cv2.face.LBPHFaceRecognizer_create()
        self.recog.read(recog_yml)
        self.face_xml = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        self.cap = cv2.VideoCapture(0)
        self.isOpened = self.cap.isOpened()

    def run(self):
        self.cap_working()

    def cap_working(self):

        while self.isOpened:
            self.face_detect()
            self.mask_detect()
            self.hQRcode_detect()
            self.release()

    def face_detect(self):

        while 1:
            _, self.frame = self.cap.read()
            frameGray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            face = self.face_xml.detectMultiScale(frameGray, 1.1, 3)
            if ord("q") == cv2.waitKey(1):
                return
            cv2.imshow("1", self.frame)
            for (x, y, w, h) in face:
                ids, confidence = self.recog.predict(frameGray[y:y+h, x:x+w])
                if confidence > 80:
                    print("未注册用户！")
                else:
                    self.name = names[ids - 1]
                    print(f"{self.name} is OK！")
                    return 1

    def mask_detect(self):

        while 1:
            _, self.frame = self.cap.read()
            results = self.module.face_detection(data={"data": [self.frame]})
            for result in results:
                label = result['data'][0]['label']
                confidence = result['data'][0]['confidence']
                if ord("q") == cv2.waitKey(1):
                    return
                cv2.imshow("2", self.frame)
                if label == "MASK" and confidence > 0.95:
                    cv2.putText(self.frame, "Please go foward.", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (25, 255, 25), 2)
                    print("Mask is OK!")
                    return 1
                elif label == "NO MASK" or label == "MASK" and confidence < 0.85:
                    cv2.putText(self.frame, "please put on mask!", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (25, 25, 255), 2)
                    print(f"{self.name} 防疫不规范，请正确佩戴口罩")

    def hQRcode_detect(self):

        while 1:
            _, self.frame = self.cap.read()
            bacodes = pyzbar.decode(self.frame, symbols=[pyzbar.ZBarSymbol.QRCODE])
            for bacode in bacodes:
                url = bacode.data.decode("UTF-8")

                uid = url[str(url).find(".cn/") + 4:]
                tar_url = f"https://suishenmafront1.sh.gov.cn/smzy/yqfkewm/ssm/ewmcheck?uid={uid}"

                tar_req = requests.get(tar_url, 'lxml')
                tar_req.encoding = 'utf-8'
                tar_json = ast.literal_eval(tar_req.json()["data"])["type"]
                # print(tar_url)
                print(tar_json)
                cv2.imshow("3", self.frame)
                if ord("q") == cv2.waitKey(1):
                    return
                if tar_json == "00":
                    print("绿码 通行。")
                    return 1
                else:
                    print("健康码 有风险 请等待工作人员核查！")
                    return 0

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()