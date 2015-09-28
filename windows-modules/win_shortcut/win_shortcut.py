#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Dennis Cao <DennisCao@live.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# this is a windows documentation stub.  actual code lives in the .ps1
# file of the same name
DOCUMENTATION = '''
---
module: win_unzip
short_description: Creates a shortcut to a file
description:
     - Creates a shortcut to a target location.
options:
  target:
    description:
      - The path of the intended target of the shortcut
    required: true
  link:
    description:
      - The path in which the shortcut will be placed. Must end in a .lnk file extension.
    required: true
author: Dennis Cao
'''
EXAMPLES = '''

# Creates a link to a file and places it on the public desktop
---
- name: Create a shortcut to internet explorer and put it on the desktop
  win_shortcut:
    target: "C:\Program Files (x86)\Internet Explorer\iexplore.exe"
    link: "C:\Users\Public\Desktop\iexplore.lnk"

# Create a link to a file and put it into the start menu
- name: Create a link to a file and put it into the start menu
  win_shortcut:
    target: "C:\Program Files (x86)\Internet Explorer\iexplore.exe"
    link: "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/InternetExplorer/InternetExplorer.lnk"
'''
