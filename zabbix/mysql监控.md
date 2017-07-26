
## 配置zabbix监控mysql

编辑C:\zabbix\conf\zabbix_agentd.win.conf，修改如下两行
```
UnsafeUserParameters=1
Include=c:\zabbix\conf\zabbix_agentd.userparams.conf
```

编辑C:\zabbix\conf\zabbix_agentd.userparams.conf，添加如下三行
```
UserParameter=mysql.version,cscript /nologo  C:\zabbix\conf\Mysql_Version.vbs
UserParameter=mysql.status[*],cscript /nologo  C:\zabbix\conf\MySQL_Ext-Status_Script.vbs $1
UserParameter=mysql.ping,cscript /nologo  C:\zabbix\conf\MySql_Ping.vbs
```

## 监控脚本

编辑C:\zabbix\conf\MySQL_Ping.vbs
```
Set objFS = CreateObject("Scripting.FileSystemObject")
Set objArgs = WScript.Arguments
str1 = getCommandOutput("D:\mysql\bin\mysqladmin.exe ping")

If Instr(str1,"alive") > 0 Then
WScript.Echo 1
Else
WScript.Echo 0
End If

Function getCommandOutput(theCommand)

Dim objShell, objCmdExec
Set objShell = CreateObject("WScript.Shell")
Set objCmdExec = objshell.exec(thecommand)
getCommandOutput = objCmdExec.StdOut.ReadAll

end Function
```

编辑C:\zabbix\conf\MySQL_Ext-Status_Script.vbs
```
Set objFS = CreateObject("Scripting.FileSystemObject")
Set objArgs = WScript.Arguments
str1 = getCommandOutput("D:\mysql\bin\mysqladmin.exe extended-status")
Arg = objArgs(0)
str2 = Split(str1,"|")
For i = LBound(str2) to UBound(str2)
If Trim(str2(i)) = Arg Then
WScript.Echo TRIM(str2(i+1))
Exit For
End If
next

Function getCommandOutput(theCommand)
Dim objShell, objCmdExec
Set objShell = CreateObject("WScript.Shell")
Set objCmdExec = objshell.exec(thecommand)
getCommandOutput = objCmdExec.StdOut.ReadAll
end Function
```

编辑C:\zabbix\conf\Mysql_Version.vbs
```
Set objFS = CreateObject("Scripting.FileSystemObject")
Set objArgs = WScript.Arguments
str1 = getCommandOutput("D:\mysql\bin\mysql.exe -V")

WScript.Echo str1

Function getCommandOutput(theCommand)
Dim objShell, objCmdExec
Set objShell = CreateObject("WScript.Shell")
Set objCmdExec = objshell.exec(thecommand)
getCommandOutput = objCmdExec.StdOut.ReadAll
end Function
```
