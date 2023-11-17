## Facial recognition access control  

This is a simple program which uses the flask, flask_simplelogin, opencv, and face_recognition to recognize and identify faces and
trigger Raspberry Pi GPIO pins as outputs for any device you would like.  

This program also includes a webapp if you wish to view what the face_recognition library is doing.  
This program was developed as a final project for the ECEGR-2000 class and as a learning experience for python and flask.

### Usage  
This was tested on a Raspbery Pi 3, however any subsequent model should be able to run this program.  
1. Clone this repository, then run: `pip install -r requirements.txt` to install dependencies. You will need python 3.9.  
2. To run the program, you can just run the included bash file: `./run.sh`
