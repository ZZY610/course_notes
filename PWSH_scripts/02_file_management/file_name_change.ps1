<#
.SYNOPSIS
    批量替换文件名中的指定字符串。

.DESCRIPTION
    通过命令行参数指定目标目录、旧字符串和新字符串，批量修改目录下文件的名称。

.PARAMETER TargetDirectory
    指定操作的目标目录路径。

.PARAMETER OldString
    指定文件名中需要替换的旧字符串。

.PARAMETER NewString
    指定文件名中用于替换的字符串。

.EXAMPLE
    .\file_name_change.ps1 -TargetDirectory "D:\YourDirectoryPath" -OldString "asd" -NewString "lkj"
    替换 D:\YourDirectoryPath 目录中所有包含 "asd" 的文件名，将其替换为 "lkj"。
#>

param (
    [Parameter(Mandatory = $true, HelpMessage = "请输入目标目录路径")]
    [string]$TargetDirectory,

    [Parameter(Mandatory = $true, HelpMessage = "请输入需要替换的旧字符串")]
    [string]$OldString,

    [Parameter(Mandatory = $true, HelpMessage = "请输入替换为的新字符串")]
    [string]$NewString
)

# 验证目标目录是否存在
if (!(Test-Path -Path $TargetDirectory)) {
    Write-Host "错误：目标目录 '$TargetDirectory' 不存在。" -ForegroundColor Red
    exit 1
}

# 获取目标目录中的所有文件
$Files = Get-ChildItem -Path $TargetDirectory -File

# 检查目录是否为空
if ($Files.Count -eq 0) {
    Write-Host "目标目录 '$TargetDirectory' 中没有文件。" -ForegroundColor Yellow
    exit 0
}

# 遍历每个文件并替换文件名
foreach ($File in $Files) {
    # 获取当前文件名
    $OldFileName = $File.Name

    # 检查文件名是否包含旧字符串
    if ($OldFileName -like "*$OldString*") {
        # 替换文件名中的旧字符串为新字符串
        $NewFileName = $OldFileName -replace $OldString, $NewString

        # 获取文件的完整路径
        $OldFilePath = $File.FullName
        $NewFilePath = Join-Path -Path $TargetDirectory -ChildPath $NewFileName

        # 重命名文件
        try {
            Rename-Item -Path $OldFilePath -NewName $NewFilePath
            Write-Host "成功将文件名从 '$OldFileName' 修改为 '$NewFileName'" -ForegroundColor Green
        } catch {
            Write-Host "修改文件名时出错：'$OldFileName'" -ForegroundColor Red
            Write-Host $_.Exception.Message -ForegroundColor Yellow
        }
    } else {
        Write-Host "文件名不包含指定字符串：'$OldFileName'" -ForegroundColor Cyan
    }
}

Write-Host "文件名替换完成！" -ForegroundColor Blue
