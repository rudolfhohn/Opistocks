#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run the server
"""
from opistocks import app
from config import PORT, DEBUG

__author__ = "Axel Fahy & Rudolf Hohn & Antoine Magnin"
__version__ = "1.0"
__date__ = "21.04.2017"
__status__ = "Development"

app.run(host='0.0.0.0', port=PORT, debug=DEBUG, threaded=True)

