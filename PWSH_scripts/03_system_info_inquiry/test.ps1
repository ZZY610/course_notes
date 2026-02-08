# 动态监控进程资源使用情况的PowerShell脚本

function Get-ProcessResourceUsage {
    param (
        [int]$RefreshInterval = 1  # 刷新间隔时间（秒）
    )

    while ($true) {
        Clear-Host  # 清屏
        Write-Host "当前系统进程资源使用情况：" -ForegroundColor Cyan

        # 获取进程信息
        $processes = Get-Process | Select-Object -Property Id, ProcessName, CPU, WS, PrivateMemorySize, WorkingSet64, DiskReadBytes, DiskWriteBytes

        # 显示表头
        Write-Host "进程ID`t进程名`t`tCPU使用率`t内存使用(MB)`t工作集(MB)`t磁盘读取(KB)`t磁盘写入(KB)" -ForegroundColor Yellow

        # 遍历进程并显示资源使用情况
        foreach ($process in $processes) {
            $cpuUsage = [math]::Round($process.CPU, 2)  # CPU使用率，保留两位小数
            $memoryUsageMB = [math]::Round($process.WS / 1MB, 2)  # 内存使用量，单位MB
            $privateMemoryMB = [math]::Round($process.PrivateMemorySize / 1MB, 2)  # 私有内存使用量，单位MB
            $workingSetMB = [math]::Round($process.WorkingSet64 / 1MB, 2)  # 工作集大小，单位MB
            $diskReadKB = [math]::Round($process.DiskReadBytes / 1KB, 2)  # 磁盘读取量，单位KB
            $diskWriteKB = [math]::Round($process.DiskWriteBytes / 1KB, 2)  # 磁盘写入量，单位KB

            Write-Host "$($process.Id)`t$($process.ProcessName)`t`t$cpuUsage`t$memoryUsageMB`t$workingSetMB`t$diskReadKB`t$diskWriteKB"
        }

        Start-Sleep -Seconds $RefreshInterval  # 按指定间隔刷新
    }
}

# 调用函数，设置刷新间隔为1秒
Get-ProcessResourceUsage -RefreshInterval 1