@echo off
echo zzy2024
echo 已经不是一般的电脑了，必须要出重拳！
echo 清理系统缓存和不需要的文件...

:: 清理 Windows 临时文件
echo 清理临时文件...
del /s /f /q %temp%\*
rd /s /q %temp%

:: 清理 Windows 预取文件
echo 清理预取文件...
del /s /f /q C:\Windows\Prefetch\*

:: 清理回收站
echo 清理回收站...
rd /s /q C:\$Recycle.Bin

:: 清理 Windows 更新缓存
echo 清理 Windows 更新缓存...
net stop wuauserv
rd /s /q C:\Windows\SoftwareDistribution\Download
net start wuauserv

:: 清理浏览器缓存（以 Chrome 为例）
echo 清理 Chrome 缓存...
rd /s /q %LocalAppData%\Google\Chrome\User Data\Default\Cache

:: 使用 cleanmgr 清理磁盘
echo 使用 cleanmgr 清理磁盘...
cleanmgr /sagerun:1

echo 清理完成！
echo 天无二日，我心中只有卡卡一个太阳！
pause
exit
