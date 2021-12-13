
# Copyright 2020 Google Inc. All Rights Reserved.
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

import os
import logging
import random
from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['R', 'L', 'F']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():

    logger.info(request.json)
    state = request.json
    me_href = state["_links"]["self"]["href"]
    dims_w = state["arena"]["dims"][0]
    dims_h = state["arena"]["dims"][1]
    arena = dict()
    for player_name, player_state in state["arena"]["state"].items():
        pos_x = player_state["x"]
        pos_y = player_state["y"]
        arena[(pos_x, pos_y)] = player_name

        if player_name == me_href:
            me_x = pos_x
            me_y = pos_y
            me_d = player_state["direction"]

    # check if somebody is on the line
    if me_d == "N":
        if (me_x, me_y - 1) in arena or (me_x, me_y - 2) in arena or (me_x, me_y - 3) in arena:
            return "T"
    elif me_d == "E":
        if (me_x+1, me_y) in arena or (me_x+2, me_y) in arena or (me_x+3, me_y) in arena:
            return "T"
    elif me_d == "S":
        if (me_x, me_y + 1) in arena or (me_x, me_y + 2) in arena or (me_x, me_y + 3) in arena:
            return "T"
    else: 
        if (me_x-1, me_y) in arena or (me_x-2, me_y) in arena or (me_x-2, me_y) in arena:
            return "T"


    return moves[random.randrange(len(moves))]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
