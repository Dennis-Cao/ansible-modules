#!/usr/bin/python
# -*- coding: utf-8 -*-

# 2015, Dennis Cao <DennisCao@live.com>
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

import os
import time

DOCUMENTATION = '''
---
module: win_set_audit
short_description: Add or modify audit rules for a file or directory
description:
     - The M(win_set_audit) module adds/modifies the audit rules for a file or directory.
options:
  target:
    description:
      - The absolute path to the file/directory that will have its audit rules modified
    required: ture
    default: null
  user:
    description:
      - The name of the object name to select
    required: true
    default: null
  rules:
    description:
      - Specifies the type of operation associated with the audit rule.
        Multiple values can be included, seperate values must be a single string seperated by commas.
        The full descriptions of each choice can be seen here:
        https://msdn.microsoft.com/en-us/library/system.security.accesscontrol.filesystemrights%28v=vs.110%29.aspx
      required: true
      default: null
      choices:
      - [AppendData,ChangePermissions,CreateDirectories,CreateFiles,Delete,DeleteSubdirectoriesAndFiles,
        ExecuteFile,FullControl,ListDirectory,Modify,Read,ReadAndExecute,ReadAttributes,ReadData,
        ReadExtendedAttributes,ReadPermissions,Synchronize,TakeOwnership,Traverse,Write,WriteAttributes,
        WriteData,WriteExtendedAttributes]
  inheritance:
    description:
      - Specify how access masks are propagated to child objects.
        Inheritance flags specify the semantics of inheritance for access control entries (ACEs).
        If C(ContainerInherit), The ACE is inherited by child container objects.
        If C(ObjectInherit), The ACE is inherited by child leaf objects.
        If C(None), The ACE is not inherited by child objects.
    required: false
    default: None
    choices: [ContainerInherit,ObjectInherit,None]
  propagation:
    description:
      - Specifies how Access Control Entries (ACEs) are propagated to child objects.
        These flags are significant only if inheritance flags are present.
        If C(InheritOnly), the ACE is propagated only to child objects. This includes both container and
        leaf child objects.
        If C(NoPropagateInherit), the ACE is not propagated to child objects.
        If C(None), no inheritance flags are set.
    required: false
    default: None
    choices: [InheritOnly,NoPropagateInherit,None]
  audit:
    description:
      - Specifies the conditions for auditing attempts to access a securable object.
        If C(Failure), failed access attempts are to be audited.
        If C(Success), Successful access attempts are to be audited.
    required: true
    default: null
    choices: [Failure,Success]
  overwrite:
    description:
      - Whether or not to overwrite current audit rules associated with a file
        If C(true)
    required: false
    default: false
    choices: [true, false, yes, no]
author: "Dennis Cao"
notes:
   - The remote user must have the adequate permissions to modify audit rules for the file specified.
'''

EXAMPLES = '''
# Enforce auditing of the "Everyone" group for all failed actions in a directory "foo"
- win_set_audit: target=C:\foo user=Everyone rules=FullControl inheritance="ContainerInherit,ObjectInherit" audit=Failure

# Enforce auditing of the "Everyone" group on a file for successfull actions using special access rules
- win_set_audit: target=C:\foobar.txt user=Everyone rules="CreateFiles,TakeOwnership,Delete" audit=Success

# Erase existing rules and add your own for only one user
- win_set_audit: target=C:\foo user=THIS-PC\thisuser rules="CreateFiles,TakeOwnership,Delete" audit=Success overwrite=true

'''

