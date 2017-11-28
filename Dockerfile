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

ENV MYSQL_USER=mysql \
    MYSQL_DATA_DIR=/var/lib/mysql \
    MYSQL_RUN_DIR=/var/run/mysqld \
    MYSQL_LOG_DIR=/var/log/mysql
        
ENV MYSQL_ROOT_PASSWORD='dwdstudent2015' 

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
	&& apt-get install -y mysql-server \
	&& apt-get install -y python3-mysqldb \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf ${MYSQL_DATA_DIR} \
	&& mkdir -p ${MYSQL_DATA_DIR} ${MYSQL_RUN_DIR} \
	&& chown -R mysql:mysql ${MYSQL_DATA_DIR} ${MYSQL_RUN_DIR} \
	&& chmod 777 ${MYSQL_RUN_DIR} \
	&& echo '[mysqld]\nskip-host-cache\nskip-name-resolve\nuser=mysql' > /etc/mysql/conf.d/docker.cnf

RUN pip3 install ipython-sql

RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf

RUN mysqld --initialize-insecure --user=mysql 

RUN chown -R mysql:mysql ${MYSQL_DATA_DIR} ${MYSQL_RUN_DIR} && \
    service mysql start & sleep 5 \
    && zcat /data/facebook.sql.gz | mysql -uroot \
    && zcat /data/imdb.sql.gz | mysql -uroot \
    && echo "use mysql; ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';" | mysql -uroot
    
EXPOSE 3306 8888 

LABEL org.jupyter.service="jupyter"

ENTRYPOINT chown -R mysql:mysql ${MYSQL_DATA_DIR} ${MYSQL_RUN_DIR}; service mysql start
ENTRYPOINT ["jupyter", "notebook", "--no-browser", "--allow-root"]
