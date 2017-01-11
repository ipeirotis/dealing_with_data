#!/bin/bash
sudo -H pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | tee >(xargs -n1 sudo -H python3 -m pip install -U) | grep -v "Requirement"
