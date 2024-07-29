import socket
import threading
import cv2
import time
import numpy as np

# データ受け取り用の関数
def udp_receiver():
    while True:
        try:
            response, _ = sock.recvfrom(1024)
        except Exception as e:
            print(e)
            break

# Tello側のローカルIPアドレス(デフォルト)、宛先ポート番号(コマンドモード用)
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# Telloからの映像受信用のローカルIPアドレス、宛先ポート番号
TELLO_CAMERA_ADDRESS = 'udp://@0.0.0.0:11111'

# キャプチャ用のオブジェクト
cap = None

# データ受信用のオブジェクト備
response = None

# 通信用のソケットを作成
# ※アドレスファミリ：AF_INET（IPv4）、ソケットタイプ：SOCK_DGRAM（UDP）
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 自ホストで使用するIPアドレスとポート番号を設定
sock.bind(('', TELLO_PORT))

# 受信用スレッドの作成
thread = threading.Thread(target=udp_receiver, args=())
thread.daemon = True
thread.start()

# コマンドモード
sock.sendto('command'.encode('utf-8'), TELLO_ADDRESS)

time.sleep(1)

# カメラ映像のストリーミング開始
sock.sendto('streamon'.encode('utf-8'), TELLO_ADDRESS)

time.sleep(5)

if cap is None:
    cap = cv2.VideoCapture(TELLO_CAMERA_ADDRESS)
    #cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))

if not cap.isOpened():
    cap.open(TELLO_CAMERA_ADDRESS)

#sock.sendto('takeoff'.encode('utf-8'), TELLO_ADDRESS)
time.sleep(1)

sock.sendto('up 20'.encode('utf-8'), TELLO_ADDRESS)
time.sleep(1)

#キャプチャ画面の中心点の取得
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
c_x = width//2
c_y = height//2
c_w = width//4
c_h = height//4


c_x_max = c_x + 50
c_x_min = c_x - 50

face_detector = cv2.FaceDetectorYN.create("./model/face_detection_yunet_2023mar.onnx", "", (0, 0))

while True:
    ret, frame = cap.read()

    # 入力サイズを指定する
    height, width, _ = frame.shape
    face_detector.setInputSize((width, height))

    # 顔を検出する
    _, faces = face_detector.detect(frame)
    faces = faces if faces is not None else []
    faces

    for face in faces:
        x, y, w, h = list(map(int, face[:4]))
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)

    # Enter 離陸
    if key == 13:
        sock.sendto('takeoff'.encode('utf-8'), TELLO_ADDRESS)

    # W 20㎝上昇
    if key == ord('w'):
        sock.sendto('up 20'.encode('utf-8'), TELLO_ADDRESS)

    # S 20㎝
    if key == ord('s'):
        sock.sendto('down 20'.encode('utf-8'), TELLO_ADDRESS)

    # D Clockwise 20ds
    if key == ord('d'):
        sock.sendto('cw 20'.encode('utf-8'), TELLO_ADDRESS)

    # A Counterclockwise 20ds
    if key == ord('a'):
        sock.sendto('ccw 20'.encode('utf-8'), TELLO_ADDRESS)
    
    # F Flip back
    if key == ord('f'):
        sock.sendto('flip b'.encode('utf-8'), TELLO_ADDRESS)

    #ESC for Emergency 緊急用です
    if key == 27:
        sock.sendto('emergency'.encode('utf-8'), TELLO_ADDRESS)

    # Q 着陸
    if key & 0xFF == ord('q'):
        sent = sock.sendto('land'.encode('utf-8'), TELLO_ADDRESS)
        break
cap.release()
cv2.destroyAllWindows()

# ビデオストリーミング停止
sock.sendto('streamoff'.encode('utf-8'), TELLO_ADDRESS)