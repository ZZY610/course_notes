cd F:\notebook\operation_notes
git add .
$sysdate=Get-Date
echo $sysdate
git commit -m $sysdate
git push operation main 