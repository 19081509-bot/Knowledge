# scan2text.ps1  —  扫描PDF一键OCR（tesseract中文+OCRmyPDF）
# 用法: powershell -File scan2text.ps1 -In <扫描PDF> [-Out <输出PDF>] [-Txt <文本>] [-Lang chi_sim] [-Dpi 200] [-Force]
param(
  [Parameter(Mandatory=$true)][string]$In,
  [string]$Out,
  [string]$Txt,
  [string]$Lang = "chi_sim",
  [int]$Dpi = 200,
  [switch]$Force
)
$ErrorActionPreference = "Stop"
$tess = "C:\Program Files\Tesseract-OCR\tesseract.exe"
if(-not (Test-Path $tess)){ throw "tesseract未安装: $tess (需含$Lang语言包)" }
if(-not $Out){ $Out = [System.IO.Path]::ChangeExtension($In, ".ocr.pdf") }
if(-not $Txt){ $Txt = [System.IO.Path]::ChangeExtension($In, ".ocr.txt") }
$args = @("-l", $Lang, "--force-ocr", "--sidecar", $Txt, "--dpi", "$Dpi")
if($Force){ $args += "--force-ocr" }
if(Test-Path $Out){ Remove-Item -LiteralPath $Out -Force }
python -m ocrmypdf @args $In $Out 2>&1
if($LASTEXITCODE -ne 0){ throw "OCRmyPDF失败 exit=$LASTEXITCODE" }
Write-Host "OK 文字层PDF: $Out"
Write-Host "OK 文本: $Txt ($((Get-Item $Txt).Length) bytes)"
