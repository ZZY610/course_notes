<#
.SYNOPSIS
    批量生成文件。

.DESCRIPTION
    按照指定的文件名前缀和数字范围，在目标目录下生成文件。

.PARAMETER TargetDirectory
    指定生成文件的目标目录。

.PARAMETER FilePrefix
    指定文件名前缀。

.PARAMETER StartNumber
    指定生成文件的起始编号。

.PARAMETER EndNumber
    指定生成文件的结束编号。

.EXAMPLE
    .\generate_files.ps1 -TargetDirectory "D:\YourDirectoryPath" -FilePrefix "hello" -StartNumber 1 -EndNumber 5
    在 D:\YourDirectoryPath 下生成 hello1、hello2、hello3、hello4、hello5 文件。
#>

param (
    [Parameter(Mandatory = $true)]
    [string]$TargetDirectory,  # 文件生成目标目录

    [Parameter(Mandatory = $true)]
    [string]$FilePrefix,       # 文件名前缀

    [Parameter(Mandatory = $true)]
    [int]$StartNumber,         # 起始编号

    [Parameter(Mandatory = $true)]
    [int]$EndNumber            # 结束编号
)

# 验证目标目录是否存在
if (!(Test-Path -Path $TargetDirectory)) {
    Write-Host "错误：目标目录 '$TargetDirectory' 不存在。" -ForegroundColor Red
    exit 1
}

# 循环生成文件
for ($i = $StartNumber; $i -le $EndNumber; $i++) {
    $FileName = "$FilePrefix$i.txt"
    $FilePath = Join-Path -Path $TargetDirectory -ChildPath $FileName

    # 创建文件
    try {
        New-Item -ItemType File -Path $FilePath -Force | Out-Null
        Write-Host "成功生成文件：$FileName" -ForegroundColor Green
    } catch {
        Write-Host "生成文件失败：$FileName" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Yellow
    }
}

Write-Host "文件生成完成！" -ForegroundColor Blue
