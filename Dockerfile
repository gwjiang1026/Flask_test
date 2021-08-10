# Build image
FROM ubuntu:18.04 AS build
LABEL INSTANCE_TYPE="darknet"
MAINTAINER gwjiang1026@gmail.com

RUN apt-get update
RUN apt-get install -y build-essential git

# Get and compile darknet
WORKDIR /src
RUN git clone https://github.com/AlexeyAB/darknet.git
WORKDIR /src/darknet
RUN git checkout b8dceb7 

RUN sed -i -e "s!OPENMP=0!OPENMP=1!g" Makefile && \
	sed -i -e "s!AVX=0!AVX=1!g" Makefile && \
	sed -i -e "s!LIBSO=0!LIBSO=1!g" Makefile && \
	make
 
 
#RUN apt-get clean
#RUN apt update && \
#   apt install -y pkg-config && \
#	apt install -y libopencv-dev




#RUN sed -i 's/OPENCV=0/OPENCV=1/' Makefile && \
#	sed -i 's/GPU=0/GPU=1/' Makefile && \
#	sed -i 's/CUDNN=0/CUDNN=1/' Makefile && \
#	sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile && \
#    sed -i -e "s!AVX=0!AVX=1!g" Makefile && \
#    sed -i -e "s!LIBSO=0!LIBSO=1!g" Makefile && \
#	make


FROM ubuntu:18.04
LABEL INSTANCE_TYPE="hello-world"
MAINTAINER gwjiang1026@gmail.com

WORKDIR /app
COPY --from=build /src/darknet/libdarknet.so .
COPY --from=build /src/darknet/darknet.py .
COPY --from=build /src/darknet/cfg data/
COPY --from=build /src/darknet/data data/

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y locales && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8 

RUN apt-get update \
	&& apt-get install -y libgomp1 wget  \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
	pip install opencv-python-headless && \
    pip install matplotlib


ENV PYTHONIOENCODING utf-8
ENV PYTHONUNBUFFERED=1

ENV TZ="Asia/Taipei"
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get -y install tzdata curl vim && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

## Change TimeZone
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

EXPOSE 5000

# set work directory
WORKDIR /opt

# install dependencies
COPY ./flask_app /opt/flask_app
COPY ./yolo_weight /opt/yolo_weight
COPY ./test_image /opt/test_image
COPY run.py requirements.txt logging.ini ./
RUN pip install -r requirements.txt
RUN mkdir /opt/logs

# set work directory
WORKDIR /opt/yolo_weight

#RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=18LiYE2W7f7H_rAiUMcR_uaxjtnh30Y6y' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=18LiYE2W7f7H_rAiUMcR_uaxjtnh30Y6y" -O wheelchair.weights && rm -rf /tmp/cookies.txt
#RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1qj--C27Lfi9nLe9C_WajgRV_Y49MqZPm' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1qj--C27Lfi9nLe9C_WajgRV_Y49MqZPm" -O pose.weights && rm -rf /tmp/cookies.txt
#RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1K2TasIlqFVxVvzmlLX1sXjO5fZVP5kJ-' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1K2TasIlqFVxVvzmlLX1sXjO5fZVP5kJ-" -O pose.weights && rm -rf /tmp/cookies.txt

# set work directory
WORKDIR /opt
ENV FLASK_APP="/opt/run.py"
ENV FLASK_ENV="development"

# CMD flask run --no-reload

