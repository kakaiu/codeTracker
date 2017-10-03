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
import re

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_author(line):
    regex = re.compile("author:\s(.*)?\semail")
    author = regex.findall(line)
    return author


def get_email(line):
    # TODO: resolve ".com.cn" or ".edu.cn" case
    regex = re.compile(".+?([a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)")
    email = regex.findall(line)
    return email


def get_code_snippet(lines):
    snippet_list = list()
    snippet = list()
    regex_plus = re.compile("^\+(?!\+\+)(.*)$")
    regex_minus = re.compile("^-(?!--)(.*)$")
    regex_remain = re.compile("^\s+(.*)")
    regex_pause = re.compile("^(@@|hash)")
    for line in lines:
        snippet_plus = regex_plus.findall(line)
        snippet_minus = regex_minus.findall(line)
        snippet_remain = regex_remain.findall(line)
        if len(snippet_plus):
            snippet = snippet_plus
        elif len(snippet_minus):
            snippet = snippet_minus
        elif len(snippet_remain):
            snippet = snippet_remain
        if regex_pause.findall(line):
            break
        if len(snippet):
            snippet_list.append(snippet[0])
    return snippet_list


def get_change_section(line):
    regex = re.compile("^@@")
    if regex.findall(line):
        return 1
    else:
        return 0

# def get_line_index(inp):
#     a_start_line_list = list()
#     a_total_line_list = list()
#     b_start_line_list = list()
#     b_total_line_list = list()
#     lines = inp.split("\n")
#     regex_a_start = re.compile("@@\s-(\d+),\d+\s")
#     regex_a_total = re.compile("@@\s-\d+,(\d+)\s")
#     regex_b_start = re.compile("\+(\d+),\d+\s@@")
#     regex_b_total = re.compile("\+\d+,(\d+)\s@@")
#     for line in lines:
#         a_start_line = regex_a_start.findall(line)
#         a_total_line = regex_a_total.findall(line)
#         b_start_line = regex_b_start.findall(line)
#         b_total_line = regex_b_total.findall(line)
#         a_start_line_list.extend(a_start_line)
#         a_total_line_list.extend(a_total_line)
#         b_start_line_list.extend(b_start_line)
#         b_total_line_list.extend(b_total_line)
#     return a_start_line_list, a_total_line_list, b_start_line_list, b_total_line_list


def get_code(inp):
    code_list = list()
    command = "git log --pretty=format:'hash: %h ref: %d commit_title: %f date: %ci author: %aN email: %ae' " \
              "--abbrev-commit -p " + inp\
              # + " > " + outp + "/log.txt"
    input_data = os.popen(command)
    data = input_data.read()
    # print(data)
    lines = data.split("\n")
    for index, line in enumerate(lines):
        code_dict = dict()
        tmp = get_author(line)
        if len(tmp):
            commit_author = tmp[0]
            tmp = get_email(line)
            if len(tmp):
                code_dict['author'] = commit_author
                # print(commit_author)
                commit_email = tmp[0]
                code_dict['email'] = commit_email
                # print(commit_email)
                code_snippet = get_code_snippet(lines[(index + 1):len(lines)])
                code_dict['code_snippet'] = code_snippet
                # code_list.append(code_dict)
        elif get_change_section(line):
            code_dict['author'] = commit_author
            # print(commit_author)
            code_dict['email'] = commit_email
            # print(commit_email)
            code_snippet = get_code_snippet(lines[(index + 1):len(lines)])
            code_dict['code_snippet'] = code_snippet
            code_list.append(code_dict)
    # (fa_start_line_list, fa_total_line_list, fb_start_line_list, fb_total_line_list) = get_line_index(data)
    # code_data = zip(commit_author, commit_email, fa_start_line_list, fa_total_line_list, fb_start_line_list, fb_total_line_list)
    # code_dict = [{"author": author, "email": email, "a_start_line": a_start_line, "a_total_line": a_total_line,
    #                  "b_start_line": b_start_line, "b_total_line": b_total_line}
    #              for author, email, a_start_line, a_total_line, b_start_line, b_total_line in code_data]
    # print(code_list)
    for code in code_list:
        print('\033[1;31m')
        print('*' * 150)
        print("")
        print("")
        print("")
        print("Author: {}".format(code['author']))
        print("")
        print("")
        print("")
        print("Email: {}".format(code['email']))
        print("")
        print("")
        print("")
        print('*' * 150)
        print('\033[0m')
        snippet = code["code_snippet"]
        for line in snippet:
            print(line)
    return code_list


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


