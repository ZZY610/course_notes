# 引入user32.dll
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class MouseOperations {
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int x, int y);
    
    [DllImport("user32.dll")]
    public static extern uint GetMessagePos();
    
    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, uint dwExtraInfo);
}
"@

# 定义鼠标事件常量
$MOUSEEVENTF_LEFTDOWN = 0x02
$MOUSEEVENTF_LEFTUP = 0x04

# 鼠标点击函数
function MouseClick {
    param (
        [int]$x,
        [int]$y
    )

    # 移动鼠标到指定坐标
    [MouseOperations]::SetCursorPos($x, $y)

    # 模拟鼠标左键按下
    [MouseOperations]::mouse_event($MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Start-Sleep -Milliseconds 50  # 按下的持续时间，50毫秒为典型点击时间

    # 模拟鼠标左键抬起
    [MouseOperations]::mouse_event($MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
}

# 设置点击区域和间隔时间
$xStart = 100  # 鼠标点击区域左上角x坐标
$yStart = 100  # 鼠标点击区域左上角y坐标
$width = 200   # 区域宽度
$height = 200  # 区域高度
$interval = 1   # 点击间隔（秒）

# 持续执行点击操作
while ($true) {
    # 随机生成区域内的坐标
    $x = Get-Random -Minimum $xStart -Maximum ($xStart + $width)
    $y = Get-Random -Minimum $yStart -Maximum ($yStart + $height)

    # 执行鼠标点击
    MouseClick $x $y

    # 等待指定的时间间隔
    Start-Sleep -Seconds $interval
}