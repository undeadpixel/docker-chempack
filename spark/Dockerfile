ARG CHEMPACK_VERSION=latest

FROM undeadpixel/chempack:$CHEMPACK_VERSION
MAINTAINER Josep Arús-Pous <josep@joseparus.com>

# install mesos using ubuntu repos (should work)
RUN set -ex &&\
  echo "deb http://repos.mesosphere.com/ubuntu xenial main" | tee -a /etc/apt/sources.list &&\
  apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF &&\
  apt update -y &&\
  apt install -y --no-install-recommends mesos &&\
  apt remove --purge -y gnupg && apt autoremove -y &&\
  rm -rf /var/lib/apt/lists/*

# install spark
ENV SPARK_HOME="/usr/local/spark"
ENV PATH="$SPARK_HOME/bin:$PATH"
WORKDIR $SPARK_HOME

ARG SPARK_DIST_MIRROR="https://d3kbcqa49mib13.cloudfront.net"
ARG SPARK_VERSION=2.2.0

# create user spark and 
RUN set -ex && apt update -y && apt install -y --no-install-recommends wget && mkdir -p $SPARK_HOME &&\
  wget -qO- $SPARK_DIST_MIRROR/spark-${SPARK_VERSION}-bin-hadoop2.7.tgz | tar xz --strip-components=1 -C $SPARK_HOME &&\
  apt remove --purge -y wget && apt autoremove -y && rm -rf /var/lib/apt/lists/*

ENV MESOS_NATIVE_JAVA_LIBRARY /usr/lib/libmesos.so

COPY conf/* $SPARK_HOME/conf/
COPY run/* /run/

CMD ["pyspark"]

