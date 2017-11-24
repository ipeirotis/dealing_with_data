# A base docker image that includes a Jupyter server 
# 
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

# install latest version of pip
RUN pip3 install -U pip 

# TODO: Move the Python libraries to a requirements.txt file?

# install basic Python libraries to run Jupyter
RUN pip3 install -U \
	jupyter \
	ipython 
	
# add libraries used in intro to python exercise
RUN pip3 install -U jellyfish \
	ngram \

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

# Add a notebook profile.
RUN mkdir -p -m 700 /root/.jupyter/ && \
    echo "c.NotebookApp.ip = '*'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.notebook_dir = '/notebooks'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = 'sha1:44967f2c7dbb:4ae5e013fa8bae6fd8d4b8fa88775c0c5caeffbf'" >> /root/.jupyter/jupyter_notebook_config.py

WORKDIR /notebooks
RUN ["git", "clone", "--verbose", "https://github.com/ipeirotis/dealing_with_data.git", "/notebooks"]
# VOLUME /notebooks

WORKDIR /data 
RUN ["git", "clone", "--verbose", "https://github.com/ipeirotis/data.git", "/data"]
# VOLUME /data

EXPOSE 8888

LABEL org.jupyter.service="jupyter"

CMD ["jupyter", "notebook", "--no-browser", "--allow-root"]
