# 检查机器上所有分区的存储空间、空闲空间大小
Get-CimInstance -ClassName Win32_LogicalDisk |
Select-Object DeviceID, @{Name="SizeGB";Expression={$_.Size/1GB}}, 
@{Name="FreeSpaceGB";Expression={$_.FreeSpace/1GB}}
