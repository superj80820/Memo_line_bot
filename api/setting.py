# coding: utf-8

### lib ###
import requests
import datetime  
import json
import random
import hmac
from hashlib import sha1
import base64
import time
import sys
import os
import re
import configparser as ConfigParser
from math import sin, cos, sqrt, atan2, radians
import ast
import sqlite3 as sqlite

## information ##
## file info ##
FileRoute='%s' %os.path.dirname(os.path.abspath(__file__))
## line info ##
LINE_TOKEN = 'kU3x7Y0u3SobhucFHhTOOY01AMV2wv+dTqieTAxle/WXksbWXMVGnXDpLYvdJM+qWA6X8L+GExz6E3LvBavE7t76h6gZpXc2JScufqHOCwOMGQzaIBTFr+/wtK2SxweCwVsVUtGa9OGbWY/5nDa8bwdB04t89/1O/w1cDnyilFU='
LINE_SECRET = '85da4d0c5bb12b1f139abcfe4ac6d133'

## self lib ###
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")))
