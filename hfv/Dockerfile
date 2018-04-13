FROM opengn.org:32333/easypi/alpine-arm
MAINTAINER joliu<joliu@s-an.org>
ENV TIME_ZONE Asia/Shanghai
RUN apk --update add python3 py3-pip tzdata
RUN pip3 install pymysql -i https://pypi.douban.com/simple
RUN echo "${TIME_ZONE}" > /etc/timezone \
&& ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime 

WORKDIR /data
COPY listenSer.py /data
COPY workProcess.py /data
COPY testDevice.py /data
COPY start.sh /data

CMD sh /data/start.sh
