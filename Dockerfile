# A base docker image that includes a Jupyter server running
# 
# docker build --network=host -t dwd NYU
# 

FROM ubuntu:latest

MAINTAINER Panos Ipeirotis <panos@stern.nyu.edu>

ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV PYTHONIOENCODING UTF-8

RUN useradd -ms /bin/bash ubuntu


RUN apt-get -y update && \
    apt-get -y dist-upgrade && \
    apt-get -y upgrade && \
    apt-get update && apt-get -y install \
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
        zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install Python libraries
RUN pip3 install -U pip 

# TODO: Move the Python libraries to a requirements.txt file?
# install Python libraries
RUN pip3 install -U \
	pip \
	jupyter \
	ipython \
	jellyfish \
	ngram \
	numpy \
	scipy \
	matplotlib \
	pandas \
	requests \
	requests_oauthlib \
	statsmodels \
	spacy \
	nltk \
	Flask \
	boto \
	boto3 \
	elasticsearch  folium  gensim  geopy  geopandas googlefinance  networkx   py2neo  pymongo  selenium  slackclient tweepy  yahoo-finance 

# Add a notebook profile.
RUN mkdir -p -m 700 /root/.jupyter/ && \
    echo "c.NotebookApp.ip = '*'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.notebook_dir = '/notebooks'" >> /root/.jupyter/jupyter_notebook_config.py

WORKDIR /notebooks
RUN ["git", "clone", "--verbose", "https://github.com/ipeirotis/dealing_with_data.git", "/notebooks"]
# VOLUME /notebooks

WORKDIR /data 
RUN ["git", "clone", "--verbose", "https://github.com/ipeirotis/data.git", "/data"]
# VOLUME /data

EXPOSE 8888

LABEL org.jupyter.service="jupyter"

CMD ["jupyter", "notebook", "--no-browser", "--allow-root"]
