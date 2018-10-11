ARG CHEMPACK_VERSION=latest

FROM undeadpixel/chempack:$CHEMPACK_VERSION
MAINTAINER Josep Arús-Pous <josep@joseparus.com>

# install mesos using ubuntu repos
RUN set -ex &&\
  echo "deb http://repos.mesosphere.com/ubuntu xenial main" | tee -a /etc/apt/sources.list &&\
  apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF &&\
  apt update -y &&\
  apt install -y --no-install-recommends mesos &&\
  apt autoremove -y &&\
  rm -rf /var/lib/apt/lists/*

# install spark
ENV SPARK_HOME="/usr/local/spark"
ENV PATH="$SPARK_HOME/bin:$PATH"
WORKDIR $SPARK_HOME

ARG SPARK_DIST_MIRROR="http://mirror.easyname.ch/apache/spark/"
ARG SPARK_VERSION=2.3.1

# create user spark and 
RUN set -ex && apt update -y && apt install -y --no-install-recommends wget libopenblas-base texlive-latex-base && mkdir -p $SPARK_HOME &&\
  wget -qO- $SPARK_DIST_MIRROR/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}.tgz | tar xz --strip-components=1 -C $SPARK_HOME &&\
  $SPARK_HOME/dev/make-distribution.sh \
    --name spark-full-${SPARK_VERSION} \
    --pip --tgz \
    -Phadoop-2.7 -Phive \
    -Phive-thriftserver -Pmesos -Pyarn -Pnetlib-lgpl \
    -DskipTests &&\
  apt remove --purge -y wget texlive-latex-base && apt autoremove -y && rm -rf /var/lib/apt/lists/*

ENV MESOS_NATIVE_JAVA_LIBRARY /usr/lib/libmesos.so

COPY conf/* $SPARK_HOME/conf/
COPY run/* /run/

CMD ["pyspark"]
