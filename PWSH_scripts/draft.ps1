function compute {
    param (
        [int] $num1,
        [int] $num2
    )
    return $num1 + $num2
}

$x = compute 1 2
echo $x