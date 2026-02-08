chcp 65001 > nul
@echo off
setlocal enabledelayedexpansion

:: 获取用户输入
set /p "targetDir=请输入目标文件夹绝对路径: "

:: 去掉首尾引号（如果有）
set targetDir=!targetDir:"=!

:: 基本合法性检查
if not exist "!targetDir!\*" (
    echo 路径无效或目录不存在！
    pause
    exit /b 1
)

:: 遍历并输出文件名
echo.
echo 文件夹 [!targetDir!] 下的文件:
for %%f in ("!targetDir!\*") do (
    if not exist "%%f\" (
        echo %%~nxf
    )
)

echo.
echo 输出完毕。
pause