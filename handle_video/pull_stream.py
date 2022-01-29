# -*- coding: utf-8 -*-
# @Time: 2022/1/27 9:01 AM
# @Author: wangpengpeng
# @Version: first
# @ Function:

import json
import subprocess as sp
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# hls_path /Users/pengpengwang/Downloads/www/hls;
# ffmpeg -re -i D:\XWData\video\test.mp4  -vcodec copy -acodec copy -f rtsp rtsp://192.168.35.74:8554/live.sdp

class StreamOpen():
    def __init__(self, cap, trmp_url):
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        rtmpUrl = "rtmp://10.200.0.102:1935/live/0"
        rtmpUrl = "rtmp://127.0.0.1:1935/live/0"
        rtmpUrl = "rtmp://localhost:1935/live/film"
        rtmpUrl = "rtmp://127.0.0.1:1935/live/0"

        # ffmpeg command

        command = ['ffmpeg',
                   '-y',
                   '-f', 'rawvideo',
                   '-vcodec', 'rawvideo',
                   '-pix_fmt', 'bgr24',
                   '-s', "{}x{}".format(width, height),
                   '-r', str(fps),
                   '-i', '-',
                   '-c:v', 'libx264',
                   '-pix_fmt', 'yuv420p',
                   '-preset', 'ultrafast',
                   '-f', 'flv',
                   rtmpUrl]

        self.p = sp.Popen(command, stdin=sp.PIPE)

    def play(self):
        return self.p

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def p():

    video_path = '/Users/pengpengwang/Downloads/jialebi/23.mp4'
    video_path = '/Users/pengpengwang/Downloads/jialebi/1.mkv'
    video_path = '/Users/pengpengwang/Downloads/jialebi/1.mp4'

    cap = cv2.VideoCapture(video_path)
    f1 = ffmpeg(cap)
    p=f1.play()
    while (True):
        ret, frame = cap.read()
        if not ret:
            cap = cv2.VideoCapture(video_path)
            ret, frame = cap.read()

        p.stdin.write(frame.tostring())
        if cv2.waitKey(1) & 0xFF == ord('q'):  # ?~L~I?~@~Xq?~@~Y?~@~@?~G?
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    p()