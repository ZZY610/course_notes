param(
    [Parameter(Mandatory=$true)]
    [string]$SourcePath,
    
    [Parameter(Mandatory=$true)]
    [string]$DestinationPath
)

# 验证源目录是否存在
if (-not (Test-Path -Path $SourcePath -PathType Container)) {
    Write-Error "源目录 $SourcePath 不存在！"
    exit 1
}

# 创建目标目录（如果不存在）
if (-not (Test-Path -Path $DestinationPath -PathType Container)) {
    New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
}

Write-Output "选择你的操作："
Write-Output "1、仅移动源目录下的文件，不包括子目录。"
Write-Output "2、移动源目录下所有文件，包括子目录下所有文件。"
$choice = Read-Host "输入操作编号" 

switch ($choice) {
    '1' { 
        try {
            # 获取源目录下所有文件（不包括子目录）
            $files = Get-ChildItem -Path $SourcePath -File
            
            if ($files.Count -eq 0) {
                Write-Host "源目录中没有可移动的文件"
                exit 0
            }
        
            # 移动文件
            $files | Move-Item -Destination $DestinationPath -Force
            
            Write-Host "成功移动 $($files.Count) 个文件到 $DestinationPath"
        }
        catch {
            Write-Error "移动文件时发生错误：$_"
            exit 2
        }
     }

    '2'{
        try {
            # 获取所有文件，包括子目录下的文件
            $files = Get-ChildItem -Path $SourcePath -Recurse -File

            if ($files.Count -eq 0) {
                Write-Host "源目录及其子目录中没有可移动的文件"
                exit 0
            }

            # 遍历所有文件，确保在目标目录中创建相同的子目录结构
            foreach ($file in $files) {
                # 计算相对路径
                $relativePath = $file.FullName.Substring($SourcePath.Length).TrimStart("\")
                
                # 计算目标文件夹路径（保持原有子目录结构）
                $targetFolder = Join-Path -Path $DestinationPath -ChildPath (Split-Path -Path $relativePath -Parent)
                
                # 确保目标文件夹存在
                if (-not (Test-Path -Path $targetFolder)) {
                    New-Item -Path $targetFolder -ItemType Directory -Force | Out-Null
                }

                # 计算目标文件路径
                $targetFilePath = Join-Path -Path $targetFolder -ChildPath $file.Name

                # 移动文件
                Move-Item -Path $file.FullName -Destination $targetFilePath -Force
            }

            Write-Host "成功移动 $($files.Count) 个文件，并保留目录结构"
        }
        catch {
            Write-Error "移动文件时发生错误：$_"
            exit 2
        }
    }
    Default {Write-Output "输入错误。"}
}

