#!/bin/bash

docker run -v "$(pwd)":/home/dev -it maxscha/commitbench:latest bash
