ARG CHEMPACK_SPARK_VERSION=latest

FROM undeadpixel/chempack-spark:$CHEMPACK_SPARK_VERSION
MAINTAINER Josep Arús-Pous <josep@joseparus.com>

ENV ZEPPELIN_HOME=/usr/local/zeppelin

ARG ZEPPELIN_DIST_MIRROR=http://archive.apache.org/dist/zeppelin
ARG ZEPPELIN_VERSION=0.7.2

# install zeppelin with ALL
RUN set -ex && apt update -y && apt install -y --no-install-recommends wget && mkdir -p $ZEPPELIN_HOME &&\
  wget -qO- $ZEPPELIN_DIST_MIRROR/zeppelin-${ZEPPELIN_VERSION}/zeppelin-${ZEPPELIN_VERSION}-bin-netinst.tgz |\
    tar xz --strip-components=1 -C $ZEPPELIN_HOME &&\
  $ZEPPELIN_HOME/bin/install-interpreter.sh --name md,shell,python &&\
  pip install py4j && rm -rf /root/.cache &&\
  apt remove --purge -y wget && apt autoremove -y && rm -rf /var/lib/apt/lists/*

EXPOSE 8080 8443

VOLUME $ZEPPELIN_HOME/logs \
       $ZEPPELIN_HOME/notebook \
       $ZEPPELIN_HOME/conf

WORKDIR $ZEPPELIN_HOME

COPY run/* /run/

CMD ["./bin/zeppelin.sh", "run"]
