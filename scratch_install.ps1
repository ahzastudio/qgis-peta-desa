$pluginDir = "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\Template_Peta_Desa_PerKaBIG"
New-Item -ItemType Directory -Force -Path $pluginDir
Copy-Item -Path "d:\TOOLBOX\TEMPLATE PETA DESA\QGIS_Plugin_Peta_Desa\*" -Destination $pluginDir -Recurse -Force

# Simple 1x1 PNG bytes fallback
$bytes = [byte[]](137,80,78,71,13,10,26,10,0,0,0,13,73,72,68,82,0,0,0,1,0,0,0,1,8,6,0,0,0,31,213,196,203,0,0,0,13,73,68,65,84,120,1,99,96,248,15,4,0,9,251,3,253,16,134,244,78,0,0,0,0,73,69,78,68,174,66,96,130)
[System.IO.File]::WriteAllBytes("d:\TOOLBOX\TEMPLATE PETA DESA\QGIS_Plugin_Peta_Desa\icon.png", $bytes)
[System.IO.File]::WriteAllBytes("$pluginDir\icon.png", $bytes)

Write-Host "QGIS Plugin Template Peta Desa PerKa BIG successfully installed!"
