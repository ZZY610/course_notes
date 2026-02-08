# 展示当前目录下所有项和大小
Get-ChildItem | 
Select-Object Name, 
@{Name = "iscontainer";Expression = {$_.psiscontainer}},
@{Name="SizeKB"; Expression={[math]::Round($_.Length / 1KB, 2)}} |
Where-Object {$_.iscontainer -eq "True"}