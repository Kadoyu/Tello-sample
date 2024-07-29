# TelloでOpenCVを使ってみよう 

キーボードでTelloを操作してみたり、カメラで画像認識したり．．．etc. 

Guidelines: 

- 最新の `opencv-python`をインストールする: 
  ```shell
  python3 -m pip install opencv-python
  # Or upgrade to latest version
  python3 -m pip install --upgrade opencv-python

**tello_cascade.py** 
カスケード型分類器を使った顔面認識
```python
# PC内蔵のカメラに切り替える
# 54,55行目
#cap = cv2.VideoCapture(TELLO_CAMERA_ADDRESS)
cap = cv2.VideoCapture(0)
```

**tello_dnn.py** 
DNN：Deep Neural Networkを使った顔面認識
```python
# PC内蔵のカメラに切り替える
# 54,55行目
#cap = cv2.VideoCapture(TELLO_CAMERA_ADDRESS)
cap = cv2.VideoCapture(0)
```

**tello_wifi_access.py** 
Tello EDU用に子機として使用できるようにするプログラム　
一度実行すると次に実行する必要ないです。　
```python
# SSID、PASSWORDにWiFi名とパスワードを入れる。
socket.sendto('ap SSID PASSWORD'.encode('utf-8'),tello_address)
```