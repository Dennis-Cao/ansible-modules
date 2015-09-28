#!powershell
# This file is part of Ansible
#
# Copyright 2015, Dennis Cao <DennisCao@live.com>
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

# WANT_JSON
# POWERSHELL_COMMON

$params = Parse-Args $args;

$result = New-Object psobject @{
    changed = $false
}
If ($params.target) {
    If (!(Test-Path $params.target)) {
        Exit-Json $result "The target location does not exist"
    }

}
Else{
    Fail-Json $result "missing required argument: target"
}
If (!$params.link) {
    Fail-Json $result "missing required argument: link"
}
$WScriptShell = New-Object -ComObject WScript.Shell
Try{
    $Shortcut = $WScriptShell.CreateShortcut($params.link)
    $Shortcut.TargetPath = $params.target
    $Shortcut.Save()
}
Catch {
    Fail-Json $result $_.Exception.Message;
}
$result.changed = $true
Exit-Json $result;