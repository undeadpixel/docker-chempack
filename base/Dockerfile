from ubuntu:xenial
maintainer Josep Arús-Pous <josep@joseparus.com>

# default to utf8
ENV LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    LC_CTYPE="C.UTF-8"

##########
# JAVA 8 #
##########

# i don't think other will work... but I leave it for now
ARG JAVA_VERSION=8

# installed from APT
RUN set -ex &&\
    apt update && apt install --no-install-recommends -y openjdk-${JAVA_VERSION}-jdk-headless &&\
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME="/usr/lib/jvm/java-${JAVA_VERSION}-openjdk-amd64"

############
# PYTHON 3 #
############

ARG PYTHON_VERSION=3.6.6

ENV PATH="$PATH:/usr/local/python/bin" \
    LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/python/lib"

# installation with python-build
RUN set -ex && apt update &&\
    apt install --no-install-recommends -y git wget curl &&\
    git clone https://github.com/pyenv/pyenv.git /tmp/pyenv &&\
    cd /tmp/pyenv/plugins/python-build/bin &&\
    apt install --no-install-recommends -y \
      make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev xz-utils tk-dev \
      libatlas-dev libpng-dev libfreetype6-dev libxft-dev gfortran libfftw3-dev &&\
    env PYTHON_CONFIGURE_OPTS="--enable-shared" ./python-build $PYTHON_VERSION /usr/local/python &&\
    pip install matplotlib numpy scipy seaborn pandas ipython scikit-learn statsmodels jupyter &&\
    find /usr/local/python -depth \
        \( \
          \( -type d -a \( -name test -o -name tests \) \) \
          -o \
          \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
        \) -exec rm -rf '{}' + &&\
    apt remove -y --purge \
      git wget curl &&\
    apt remove -y --purge \
      make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev xz-utils tk-dev \
      libatlas-dev libpng-dev libfreetype6-dev libxft-dev gfortran libfftw3-dev &&\
    apt autoremove -y && libDeps=' \
      libc6 libx11-6 libbz2-1.0 libssl1.0.0 libgcc1 libncurses5 libreadline6 libsqlite3-0 \
      libstdc++6 libtcl8.6 zlib1g libtk8.6' &&\
    apt install --no-install-recommends -y $libDeps && apt-mark manual $libDeps &&\
    rm -fr /tmp/pyenv && rm -rf /var/lib/apt/lists/* && rm -rf /root/.cache

#########
# RDKIT #
#########

ARG RDKIT_RELEASE=2018_03_3

# installed manually
RUN set -ex &&\
  pythonIncludePath=$(python -c "import sysconfig as sc; print(sc.get_path('include'))") &&\
  pythonLibPath=$(python -c "import sysconfig as sc; print(sc.get_path('platlib'))") &&\
  apt update -y &&\
  apt install -y --no-install-recommends \
    git wget flex bison build-essential cmake libsqlite3-dev libicu-dev &&\
  mkdir /tmp/boost &&\
  wget -qO- https://downloads.sourceforge.net/project/boost/boost/1.58.0/boost_1_58_0.tar.bz2 | tar xj --strip-components=1 -C /tmp/boost &&\
  cd /tmp/boost && ./bootstrap.sh \
    --with-libraries=python,regex,thread,serialization \
    --with-python=/usr/local/python/bin/python &&\
  CPATH=$pythonIncludePath ./b2 install --prefix=/usr/local/boost &&\
  git clone -b Release_${RDKIT_RELEASE} https://github.com/rdkit/rdkit /tmp/rdkit && cd /tmp/rdkit && mkdir build && cd build &&\
  cmake .. \
    -DPYTHON_EXECUTABLE='/usr/local/python/bin/python' \
    -DPYTHON_INCLUDE_DIR=$pythonIncludePath \
    -DPYTHON_LIBRARY='/usr/local/python/lib/libpython3.so' \
    -DPYTHON_NUMPY_INCLUDE_PATH="${pythonLibPath}/numpy/core/include" \
    -DBOOST_ROOT=/usr/local/boost \
    -DBoost_NO_SYSTEM_PATHS=ON \
    -DRDK_BUILD_AVALON_SUPPORT=ON &&\
  make -j 12 && make install &&\
  mkdir -p /usr/local/rdkit/python && mv /tmp/rdkit/lib /usr/local/rdkit/lib &&\
  mv /tmp/rdkit/rdkit /usr/local/rdkit/python/rdkit && mv /tmp/rdkit/Code /usr/local/rdkit/include &&\
  find /usr/local/rdkit/include -type f -not \( -name '*.h' -o -name '*.hpp' \) -delete &&\
  find /usr/local/rdkit/include -type d -empty -delete &&\
  mv /tmp/rdkit/Data /usr/local/rdkit/Data &&\
  apt remove -y --purge \
    git wget flex bison build-essential cmake sqlite3 libsqlite3-dev libicu-dev &&\
  apt autoremove -y && libDeps='libc6 libssl1.0.0 libgcc1 libstdc++6' &&\
  apt install --no-install-recommends -y $libDeps && apt-mark manual $libDeps &&\
  rm -fr /tmp/rdkit /tmp/boost /usr/local/boost/include && rm -rf /var/lib/apt/lists/*

ENV RDBASE="/usr/local/rdkit" \
    LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/rdkit/lib:/usr/local/boost/lib"\
    PYTHONPATH="/usr/local/rdkit/python:$PYTHONPATH"

##################
# CONFIG SCRIPTS #
##################

RUN apt update -y && apt install -y --no-install-recommends gosu &&\
  rm -fr /var/lib/apt/lists/*

COPY run.sh /run.sh
COPY run/* /run/

ENTRYPOINT ["/run.sh"]

CMD ["ipython"]
