# Facial Recognition Security System (FRSS)
Facial Recognition Security System is an application <b>under development</b> that has as one of its main objectives, 
detecting intruders in a certain ambient by using a camera and notifying the owner who's in their property by sending them
an email notification with the person's face.

You can either select if you want to use facial recognition or not to recognize the intruder. You can register people you trust
in the system so you won't get notified when that person goes into your room / property.

# Installation

- <b>OpenCV</b>: This application is built under the [OpenCV (2.4.13)](http://opencv.org) library so it 
must be installed and configured to work with python 2.7 on your computer.
- <b>facerec</b>: In order to recognize the faces from the snpashots taken by the camera, you'll need to get the facerec.py
file from the [shhavel's facerec repository](https://github.com/shhavel/facerec) and follow the instructions there to train
your face with the algorithm. It's recommended that you run the <b>facerec.py</b> file from the <b>FacialRecognitionSecuritySystem</b>
folder once you want the <b>subjects</b> folder that is created by <b>facerec</b> to be there.

After training your face with <b>facerec</b> you can start <b>faceanalyzer</b>:
```
$ python faceanalyzer.py with_facerec
```
If you'd like to run <b>faceanalyzer</b> without facial recognition (it will notify you whenever someone is detected 
by the camera) just change the argument from `with_facerec` to `withou_facerec`:
```
$ python faceanalyzer.py without_facerec
```
After starting <b>faceanalyzer.py</b>, you can start <b>facedetector.py</b> and whenever it detects a face it will save a snapshot of it so it can be analyzed by <b>faceanalyzer</b>.
```
$ python facedetector.py
```

# More Info

- By default <b>facedetector</b> is configured to take 3 snapshots when it detects a face and then wait a
minute to start taking pictures again. You can changing these parameters by editing the following lines
right at the beginning of <b>facedetector.py</b>:
```python
# minutes_to_refresh holds the number of minutes the program should wait to start taking
# snapshots again after taking them
minutes_to_refresh = 1

# Number of snapshots that will be taken when a face is detected
snapshots = 3
```
