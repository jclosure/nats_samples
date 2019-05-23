#!/bin/bash

# ln -s /usr/bin/pip3 /usr/bin/pip

# TODO(jholder): Convert this to a setup tools project
pip install jupyter
pip install --upgrade certifi
pip install asyncio-nats-client
pip install asyncio-nats-streaming
pip install protobuf3-to-dict
pip install pytest

ipython profile create
cat > ~/.ipython/profile_default/startup/00-magics.ipy <<- EOM
%load_ext autoreload
%autoreload 2
EOM
