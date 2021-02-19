LabelImg for AIDATA
========

졸음운전 예방을 위한 운전자 상태 정보 (통제환경) 데이터 가공을 위한 어노테이션 도구.


'LabelImg<https://github.com/tzutalin/labelImg>' 기반으로 작성되어, JSON 형식으로 어노테이션을 저장합니다.


설치 및 빌드(Installation & Build)
------------------

'LabelImg<https://github.com/tzutalin/labelImg>'의 설치 방법과 동일합니다.

- Build from source 이하를 운영체제에 맞게 실행함. 모두 Python 기반 환경을 구축하고 관련 종속 라이브러리를 설치하고 빌드 합니다.
- Python 기반 환경 구축 : Python 3.x 버전 권장(Anaconda 설치 환경 권장)
- 종속 라이브러리 설치 : 하기의 명령어를 Shell, Prompt 등에서 실행(단, 현재 경로는 본 레포로 되어 있어야 함)

.. code:: shell
        conda install pyqt=5
        conda install -c anaconda lxml
        pyrcc5 -o libs/resources.py resources.qrc
        pip install pyinstaller

- 실행 방법 1 : 코드로 실행

.. code:: shell
        python labelImg.py
  
- 실행 방법 2 : 빌드 후에 실행

.. code:: shell
        cd <repo>/build-tools/
        pyinstaller --hidden-import=xml --hidden-import=xml.etree --hidden-import=xml.etree.ElementTree --hidden-import=lxml.etree -D -F -n labelImg -c "../labelImg.py" -p ../libs -p ../

을 실행하면 "<repo>/build-tools/build" "<repo>/build-tools/dist"가 "<repo>/build-tools/labelImg.spec"이 생성되며,  "<repo>/build-tools/dist" 내에 빌드된 실행파일(labelImg.exe)이 생성됨.

labelImg.exe를 더블클릭하여 실행.




단축키(Hotkeys)
~~~~~~~

+--------------------+--------------------------------------------+
| Ctrl + u           | Load all of the images from a directory    |
+--------------------+--------------------------------------------+
| Ctrl + r           | Change the default annotation target dir   |
+--------------------+--------------------------------------------+
| Ctrl + s           | Save                                       |
+--------------------+--------------------------------------------+
| Ctrl + d           | Copy the current label and rect box        |
+--------------------+--------------------------------------------+
| Ctrl + Shift + d   | Delete the current image                   |
+--------------------+--------------------------------------------+
| Space              | Flag the current image as verified         |
+--------------------+--------------------------------------------+
| w                  | Create a rect box                          |
+--------------------+--------------------------------------------+
| d                  | Next image                                 |
+--------------------+--------------------------------------------+
| a                  | Previous image                             |
+--------------------+--------------------------------------------+
| del                | Delete the selected rect box               |
+--------------------+--------------------------------------------+
| Ctrl++             | Zoom in                                    |
+--------------------+--------------------------------------------+
| Ctrl--             | Zoom out                                   |
+--------------------+--------------------------------------------+
| ↑→↓←             |  Keyboard arrows to move selected rect box   |
+--------------------+--------------------------------------------+


How to reset the settings
~~~~~~~~~~~~~~~~~~~~~~~~~

In case there are issues with loading the classes, you can either:

1. From the top menu of the labelimg click on Menu/File/Reset All
2. Remove the `.labelImgSettings.pkl` from your home directory. In Linux and Mac you can do:
    `rm ~/.labelImgSettings.pkl`


License
~~~~~~~
`Free software: MIT license <https://github.com/tzutalin/labelImg/blob/master/LICENSE>`_

Citation: Tzutalin. LabelImg. Git code (2015). https://github.com/tzutalin/labelImg

Related
~~~~~~~

1. `ImageNet Utils <https://github.com/tzutalin/ImageNet_Utils>`__ to
   download image, create a label text for machine learning, etc
2. `Use Docker to run labelImg <https://hub.docker.com/r/tzutalin/py2qt4>`__
3. `Generating the PASCAL VOC TFRecord files <https://github.com/tensorflow/models/blob/4f32535fe7040bb1e429ad0e3c948a492a89482d/research/object_detection/g3doc/preparing_inputs.md#generating-the-pascal-voc-tfrecord-files>`__
4. `App Icon based on Icon by Nick Roach (GPL) <https://www.elegantthemes.com/>`__
5. `Setup python development in vscode <https://tzutalin.blogspot.com/2019/04/set-up-visual-studio-code-for-python-in.html>`__
6. `The link of this project on iHub platform <https://code.ihub.org.cn/projects/260/repository/labelImg>`__


Stargazers over time
~~~~~~~~~~~~~~~~~~~~

.. image:: https://starchart.cc/tzutalin/labelImg.svg

