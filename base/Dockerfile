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

ARG PYTHON_VERSION=3.6.2

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
    pip install matplotlib numpy scipy seaborn pandas ipython scikit-learn statsmodels &&\
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

ARG RDKIT_RELEASE=2017_03_3

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
    -DBoost_NO_SYSTEM_PATHS=ON &&\
  make -j 12 && make install &&\
  mkdir -p /usr/local/rdkit/python && mv /tmp/rdkit/lib /usr/local/rdkit/lib &&\
  mv /tmp/rdkit/rdkit /usr/local/rdkit/python/rdkit && mv /tmp/rdkit/Code /usr/local/rdkit/include &&\
  find /usr/local/rdkit/include -type f -not \( -name '*.h' -o -name '*.hpp' \) -delete &&\
  find /usr/local/rdkit/include -type d -empty -delete &&\
  apt remove -y --purge \
    git wget flex bison build-essential cmake sqlite3 libsqlite3-dev libicu-dev &&\
  apt autoremove -y && libDeps='libc6 libssl1.0.0 libgcc1 libstdc++6' &&\
  apt install --no-install-recommends -y $libDeps && apt-mark manual $libDeps &&\
  rm -fr /tmp/rdkit /tmp/boost /usr/local/boost/include && rm -rf /var/lib/apt/lists/*

ENV RDBASE="/usr/local/rdkit" \
    LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/rdkit/lib:/usr/local/boost/lib"\
    PYTHONPATH="/usr/local/rdkit/python:$PYTHONPATH"


#####
# R #
#####

ARG R_VERSION=3.4.1

ENV PATH="$PATH:/usr/local/R/bin"

# installed manually
RUN set -ex && apt update -y && \
  apt install -y --no-install-recommends \
    wget build-essential libcairo-dev libpng-dev libreadline-dev gfortran tcl-dev zlib1g-dev \
    libbz2-dev libcairo2-dev libpcre3-dev liblzma-dev liblapack-dev libblas-dev libcurl4-openssl-dev \
    libjpeg-dev libicu-dev libtiff5-dev texinfo libssl-dev &&\
  mkdir /tmp/R &&\
  wget -qO- https://cran.r-project.org/src/base/R-3/R-${R_VERSION}.tar.gz \
    | tar xz --strip-components=1 -C /tmp/R &&\
  cd /tmp/R && ./configure \
    --with-x=no \
    --with-cairo=yes \
    --with-libpng=yes \
    --enable-R-shlib \
    --prefix=/usr/local/R &&\
  make && make install &&\
  R -e "install.packages('knitr', repos='http://cran.us.r-project.org')" && \
  R -e "install.packages('ggplot2', repos='http://cran.us.r-project.org')" && \
  R -e "install.packages('googleVis', repos='http://cran.us.r-project.org')" && \
  R -e "install.packages('data.table', repos='http://cran.us.r-project.org')" && \
  R -e "install.packages('devtools', repos='http://cran.us.r-project.org')" && \
  R -e "install.packages('Rcpp', repos='http://cran.us.r-project.org')" && \
  Rscript -e "library('devtools'); library('Rcpp'); install_github('ramnathv/rCharts')" &&\
  apt remove -y --purge \
    wget build-essential libcairo-dev libpng-dev libreadline-dev gfortran tcl-dev zlib1g-dev \
    libbz2-dev libcairo2-dev libpcre3-dev liblzma-dev liblapack-dev libblas-dev libcurl4-openssl-dev \
    libjpeg-dev libicu-dev libtiff5-dev texinfo libssl-dev &&\
  apt autoremove -y && libDeps=' \
      libc6 libx11-6 libbz2-1.0 libc6 libssl1.0.0 libgcc1 libncurses5 libreadline6 \
      libstdc++6 libtcl8.6 zlib1g libtiff5 libquadmath0 libpng16-16 libpcre3 liblzma5 libjpeg-turbo8 \
      libicu55 libgomp1 libgfortran3 libfreetype6 libcurl3 libcairo2 \
  ' && apt install --no-install-recommends -y $libDeps && apt-mark manual $libDeps &&\
  rm -fr /tmp/R && rm -rf /var/lib/apt/lists/*

##################
# CONFIG SCRIPTS #
##################

RUN apt update -y && apt install -y --no-install-recommends gosu &&\
  rm -fr /var/lib/apt/lists/*

COPY run.sh /run.sh
COPY run/* /run/

ENTRYPOINT ["/run.sh"]

CMD ["ipython"]
