# dockerfile for opencv4 
# c.f. https://www.pyimagesearch.com/2018/08/15/how-to-install-opencv-4-on-ubuntu/
FROM nvidia/cuda:9.1-devel-ubuntu16.04
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential cmake unzip pkg-config wget && \
    apt-get install -y libjpeg-dev libpng-dev libtiff-dev && \
    apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev && \
    apt-get install -y libxvidcore-dev libx264-dev && \
    apt-get install -y libgtk-3-dev && \
    apt-get install -y libatlas-base-dev gfortran && \
    apt-get install -y python3-dev && \
    apt-get install -y ffmpeg && \
    ln -s -f /usr/bin/python3 /usr/bin/python

RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip && \
    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip && \
    unzip opencv.zip && \
    unzip opencv_contrib.zip && \
    mv opencv-4.0.0 opencv && \
    mv opencv_contrib-4.0.0 opencv_contrib

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    pip install numpy ipython

RUN cd opencv && mkdir build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules \
	-D PYTHON_EXECUTABLE=/usr/bin/python3 \
	-D WITH_CUDA=ON \
	-D ENABLE_FAST_MATH=ON \
	-D CUDA_FAST_MATH=ON \
	-D WITH_CUBLAS=1 \
	-D WiTH_FFMPEG=ON \	
	-D BUILD_EXAMPLES=ON .. && \
    make -j$(nproc) && make install && ldconfig && \
    find /opencv/ -name "cv2.*.so" -exec cp {} /usr/local/lib/python3.5/dist-packages/cv2.so \;
    
RUN rm /opencv.zip /opencv_contrib.zip
