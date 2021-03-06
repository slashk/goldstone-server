#!/bin/bash

# Copyright 2016 Solinea, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

tmux new -d -s goldstone_dev \
    'cd ${PROJECT_HOME}/goldstone-server;
     eval $(docker-machine env default); 
     docker-compose -f docker-compose-local-dev.yml up' \; \
     split-window -d \
     'cd ${PROJECT_HOME}/goldstone-server;
     sleep 15;
     bin/start_local_celery.sh' \; \
     attach -t goldstone_dev \;

     # set-option -t goldstone_dev remain-on-exit \; \
