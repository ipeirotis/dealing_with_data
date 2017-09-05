export PATH=$PATH:/usr/local/bin/geckodriver
jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10 --notebook-dir=/home/ubuntu/jupyter > /tmp/jupyter.out 2>&1 &

