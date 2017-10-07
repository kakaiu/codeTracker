#!~/anaconda3/bin/ python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Zimeng Qiu <CNPG-qzm@hotmail.com>
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
USAGE: %(program)s input_code_file output_dir <--search|--mapping>
"""

import json
import logging
import os
import sys

from commit_history import mapping
from git_search import search_commit_history

dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s " % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) != 4:
        print(len(sys.argv))
        raise SystemExit("Usage: python main.py input_code_file output_dir <--search|--mapping>")
    input_file, output_dir, func_argv = sys.argv[1:4]
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as exception:
            raise SystemExit("Error: Could not create the output dir.")

    if func_argv == "--mapping":
        commit_history = mapping.get_code(input_file)
        history_file = os.path.join(dir_path, output_dir, 'commit_history.json')
        with open(history_file, 'w') as f:
            json.dump(commit_history, f, indent=3)
    elif func_argv == "--search":
        if not os.path.exists(os.path.join(output_dir, 'commit_history.json')):
            try:
                commit_history = mapping.get_code(input_file)
                history_file = os.path.join(dir_path, output_dir, 'commit_history.json')
                with open(history_file, 'w') as f:
                    json.dump(commit_history, f, indent=3)
            except OSError as exception:
                raise SystemExit("Error: Search failed")
        input_code = search_commit_history.get_input_code(input_file)
        search_result = search_commit_history.search_in_history(input_code, output_dir)
        search_commit_history.print_match_result(search_result)
    else:
        print("Lack of argument")
        print("Usage: python main.py input_code_file output_dir <--search|--mapping>")




