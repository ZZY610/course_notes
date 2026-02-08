<#
.SYNOPSIS
获取并导出计算机硬件基础信息

.DESCRIPTION
本脚本用于收集当前计算机的硬件信息，支持导出为 TXT、CSV 或 Excel 格式。

.PARAMETER OutputFormat
指定输出格式（TXT/CSV/Excel），默认 TXT

.PARAMETER OutputPath
指定输出文件路径，默认当前目录

.EXAMPLE
.\Get-HardwareInfo.ps1 -OutputFormat Excel -OutputPath C:\Reports
#>

$hardware_info =[PSCustomObject]@{
    Name = Value
}

Get-CimInstance -ClassName Win32_Processor
Get-CimInstance -ClassName Win32_BaseBoard
Get-CimInstance -ClassName Win32_BIOS

function Get-HardwareInfo {
# 检查机器上所有分区的存储空间、空闲空间大小
$x = Get-CimInstance -ClassName Win32_LogicalDisk |
Select-Object DeviceID, @{Name="SizeGB";Expression={$_.Size/1GB}}, 
@{Name="FreeSpaceGB";Expression={$_.FreeSpace/1GB}}

return $x
}

Get-HardwareInfo