#!powershell
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

# WANT_JSON
# POWERSHELL_COMMON

$params = Parse-Args $args
$target= Get-Attr $params "target" $FALSE
If ($target -eq $FALSE){
    Fail-Json (New-Object psobject) "missing required argument: target"
}
$user= Get-Attr $params "user" $FALSE
If ($user -eq $FALSE){
    Fail-Json (New-Object psobject) "missing required argument: user"
}
$rules= Get-Attr $params "rules" $FALSE
If ($rules -eq $FALSE){
    Fail-Json (New-Object psobject) "missing required argument: rules"
}
$inheritance= Get-Attr $params "inheritance" "None"
$propagation= Get-Attr $params "propagation" "None"
$audit= Get-Attr $params "audit" $FALSE
If ($type -eq $FALSE){
    $audit = Fail-Json (New-Object psobject) "missing required argument: audit"
}
If ($params.overwrite) {
    $overwrite = ConvertTo-Bool ($params.overwrite)
}
Else {
    $overwrite = $false
}
$result = New-Object psobject @{
    changed = $FALSE
}


$ACL = get-acl $target -audit
$AccessRule = New-Object System.Security.AccessControl.FileSystemAuditRule($user,$rules,$inheritance,$propagation,$audit)
If ($overwrite){
	$ACL.SetAuditRule($AccessRule)
	$result.changed = $TRUE
}
Else{
	$ACL.AddAuditRule($AccessRule)
	$result.changed = $TRUE
}
$ACL | Set-Acl $target
Exit-Json $result