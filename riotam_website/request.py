#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import ast
import cgi
import json
import logging
from subprocess import Popen, PIPE, STDOUT

import os

build_result = {
    "cmd_output": ""
}

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, ".."))

LOGFILE = os.path.join(PROJECT_ROOT_DIR, "log", "request_log.txt")


def main():

    form = cgi.FieldStorage()

    selected_modules = form.getlist("selected_modules[]")
    board = form.getfirst("board")
    main_file_content = form.getfirst("main_file_content")

    if not all([selected_modules, board, main_file_content]):
        print_error()
        return

    cmd = ["python", "build.py"]

    cmd.append("--modules")
    for module in selected_modules:
        cmd.append(module)

    cmd.append("--board")
    cmd.append(board)

    cmd.append("--mainfile")
    cmd.append(main_file_content)

    logging.debug(main_file_content)

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, cwd="../../riotam-backend/riotam_backend")
    output = process.communicate()[0]

    # convert string representation of dictionary to "real" dictionary
    build_result = ast.literal_eval(output)
    build_result["cmd_output"] = build_result["cmd_output"].replace("\n", "<br>")

    print_result(json.dumps(build_result))


def print_result(result):

    print ("Content-Type: text/html")
    print ("\n\r")
    print (result)


def print_error():

    print ("Status: 403 Forbidden")
    print ("\n\r")


if __name__ == "__main__":

    logging.basicConfig(filename=LOGFILE, format="%(asctime)s [%(levelname)s]: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
        build_result["cmd_output"] = "Something really bad happened on server side: " + str(e)

        print_result(json.dumps(build_result))