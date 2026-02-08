
Write-Output "选择你的操作："
Write-Output "1、仅移动源目录下的文件，不包括子目录。"
Write-Output "2、移动源目录下所有文件，包括子目录下所有文件。"
$choice = Read-Host "输入操作编号" 
echo $choice