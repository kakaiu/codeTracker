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

from commit_history import mapping

dir_path = os.path.dirname(os.path.realpath(__file__))

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

    commit_history = mapping.get_code(input_file)


