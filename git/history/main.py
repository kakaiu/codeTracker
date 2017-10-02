#!~/anaconda3/bin/ python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Zimeng Qiu <CNPG-qzm@hotmail.com>
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
USAGE: %(program)s input_code_file output_dir
"""

import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_code(inp):
    command = "git log --pretty=format:'hash: %h ref: %d commit_title: %f date: %ci author: %aN email:%ae' " \
              "--abbrev-commit -p --graph " + inp\
              # + " > " + outp + "/log.txt"
    input_data = os.popen(command)
    data = input_data.read()
    return data

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s " % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) != 3:
        print(len(sys.argv))
        raise SystemExit("Usage: python main.py input_code_file output_dir")
    input_file, output_dir = sys.argv[1:3]
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as exception:
            raise SystemExit("Error: Could not create the output dir.")

    commit_history = get_code(input_file)
    print(commit_history)


