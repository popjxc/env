#!/bin/env python
# coding=utf8

import sys
import os
import time
import datetime
from optparse import OptionParser

header_tmpl = '''// Copyright (c) {year}, Alibaba Inc.
// All right reserved.
//
// Author: Xincai Jiang <xincai.jiang@alibaba-inc.com>
// Created: {date}
// Description

#ifndef {defname}
#define {defname}

{name_space}

class {class_name}
{{
public:
    {class_name}();
    ~{class_name}() {{}}

private:

}};

{endnamespace}
#endif // {defname}
'''

cpp_tmpl = '''// Copyright (c) {year}, Alibaba Inc.
// All right reserved.
//
// Author: Xincai Jiang <xincai.jiang@alibaba-inc.com>
// Created: {date}
// Description

#include "{class_header}"

{name_space}

{class_name}::{class_name}()
{{
}}

{endnamespace}
'''


def initOptParser():
    msg = "usage %prog --class=MasterWorker --dir=ml/predict/master/ --namespace='apsara::odps'"
    parser = OptionParser(usage=msg)

    parser.add_option("-c", "--class",
                      action="store",
                      type="string",
                      dest="class_name",
                      # default = "",
                      help="class name for generating.")

    parser.add_option("-d", "--dir",
                      action="store",
                      type="string",
                      dest="dir",
                      # default = "",
                      help="dir of generated file.")

    parser.add_option("-n", "--namespace",
                      action="store",
                      type="string",
                      dest="name_space",
                      # default = "",
                      help="namespace of the class.")

    return parser


def convertFileNameFormat(class_name, tail):
    ret = ""
    for i in range(len(class_name)):
        if i == 0:
            ret = ret + class_name[i]
        elif class_name[i].isupper():
            ret = ret + "_" + class_name[i]
        else:
            ret = ret + class_name[i]

    ret = ret + tail
    return ret.lower()


def convertDefName(dir1, class_name):
    dir1 = dir1.replace('/', '_')
    if dir1[len(dir1) - 1] != '_':
        dir1 = dir1 + "_"
    dir1 = dir1 + class_name + "_H"
    return dir1.upper().strip('_')


def convertNameSpace(ns):
    names = ns.split("::")
    name_space = ""
    for name in names:
        name_space = name_space + "namespace %s {\n" % (name)

    end_name_space = ""
    for name in names[::-1]:
        end_name_space = end_name_space + "} // namespace %s\n" % (name)

    return name_space.rstrip("\n"), end_name_space.rstrip("\n")

if __name__ == "__main__":
    parser = initOptParser()
    (options, args) = parser.parse_args()

    if not options.dir.endswith("/"):
        options.dir = options.dir + "/"
    header_file = options.dir + convertFileNameFormat(options.class_name, ".h")
    cpp_file = options.dir + convertFileNameFormat(options.class_name, ".cpp")

    def_name = convertDefName(
        options.dir, convertFileNameFormat(options.class_name, ""))

    name_space, end_name_space = convertNameSpace(options.name_space)

    now = time.strftime('%Y/%m/%d')
    year = time.strftime('%Y')

    header_content = header_tmpl.format(
        class_name=options.class_name,
        name_space=name_space,
        defname=def_name,
        year=year,
        date=now,
        endnamespace=end_name_space)

    # print header_content
    h_file = open(header_file, "w")
    h_file.write(header_content)
    h_file.close()
    print header_file

    log_path = options.dir
    if log_path[0] != '/':
        log_path = "/" + log_path
    if log_path[len(log_path) - 1] != '/':
        log_path = log_path + "/"
    cpp_content = cpp_tmpl.format(
        class_name=options.class_name,
        name_space=name_space,
        year=year,
        date=now,
        endnamespace=end_name_space,
        dir=log_path,
        class_header=header_file)

    # print cpp_content
    cpp = open(cpp_file, "w")
    cpp.write(cpp_content)
    cpp.close()
    print cpp_file
