FROM ubuntu:latest

ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV PYTHONIOENCODING UTF-8
ENV NB_USER ubuntu

RUN useradd -ms /bin/bash ubuntu

RUN apt-get -y update && \
    apt-get -y dist-upgrade && \
    apt-get -y upgrade && \
    apt-get -y install \
        sudo \
        build-essential \
        python3-dev \
        python3-pip \
        ca-certificates \
        curl \
        git \
        gfortran \
        libblas-dev \
        liblapack-dev \
        libssl-dev \
        libffi-dev \
        libcurl4-openssl-dev \
        libgdal-dev \
        wget \
        jq \
        language-pack-en \
        libcurl4-openssl-dev \
        libffi-dev \
        libzmq3-dev \
        libxml2-dev \
        libxslt-dev \
        python3-lxml \
        zlib1g-dev \
    python3-mysqldb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install latest version of pip
RUN pip3 install -U pip

# TODO: Move the Python libraries to a requirements.txt file?

# install basic Python libraries to run Jupyter
RUN pip3 install -U \
    notebook==5.2.* \
    jupyterhub==0.8.* \
    ipython

# add libraries used in intro to python exercise
RUN pip3 install -U jellyfish \
    ngram

# add standard data science libraries
RUN pip3 install -U \
    numpy \
    scipy \
    matplotlib \
    pandas \
    statsmodels \
    scikit-learn

# add libraries for teaching web APIs
RUN pip3 install -U \
    requests \
    requests_oauthlib \
    Flask \
    slackclient

# add libraries for NLP
RUN pip3 install -U \
    spacy \
    nltk \
    gensim

# add libraries for visualization/mapping
RUN pip3 install -U \
    seaborn \
    bokeh \
    folium \
    geopandas \
    geopy

# add libraries for finance
RUN pip3 install -U \
    googlefinance \
    yahoo-finance \
    quandl

# misc libraries
RUN pip3 install -U \
    boto \
    boto3 \
    elasticsearch \
    networkx \
    py2neo \
    pymongo \
    selenium \
    tweepy

ARG FILE_PATH
# Add a notebook profile.
COPY $FILE_PATH/jupyter_notebook_config.py /etc/jupyter/
RUN echo "c.NotebookApp.notebook_dir = '/notebooks'" >> /etc/jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.allow_root = True" >> /etc/jupyter/jupyter_notebook_config.py
RUN echo "$NB_USER ALL=NOPASSWD: ALL" >> /etc/sudoers

WORKDIR /notebooks
RUN ["git", "clone", "--verbose", "https://github.com/ipeirotis/dealing_with_data.git", "/notebooks"]
# VOLUME /notebooks

WORKDIR /data
RUN ["git", "clone", "--verbose", "https://github.com/ipeirotis/data.git", "/data"]
# VOLUME /data

RUN pip3 install ipython-sql sql_magic mysqlclient

EXPOSE 8888
LABEL org.jupyter.service="jupyter"
RUN chmod -R 777 /notebooks
RUN chmod -R 777 /data

CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
COPY $FILE_PATH/start-notebook.sh /usr/local/bin/

USER $NB_USER
