$ErrorActionPreference = "Stop"

$base = Join-Path $PSScriptRoot "diagram_as_code"
$mermaidDir = Join-Path $base "mermaid"
$imageRoot = Join-Path $base "images"
$svgDir = Join-Path $imageRoot "svg"
$pngDir = Join-Path $imageRoot "png"
$config = Join-Path $base "puppeteer-config.json"

New-Item -ItemType Directory -Force -Path $svgDir, $pngDir | Out-Null

$env:PUPPETEER_SKIP_DOWNLOAD = "true"
$files = Get-ChildItem $mermaidDir -Filter "*.mmd" | Sort-Object Name

foreach ($file in $files) {
    $name = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $svg = Join-Path $svgDir "$name.svg"
    $png = Join-Path $pngDir "$name.png"

    if ((Test-Path $svg) -and ((Get-Item $svg).Length -gt 0)) {
        Write-Host "Skipping $($file.Name) -> svg"
    } else {
        Write-Host "Rendering $($file.Name) -> svg"
        & npx -y -p "@mermaid-js/mermaid-cli@11.12.0" mmdc -i $file.FullName -o $svg -p $config -b white
        if ($LASTEXITCODE -ne 0) {
            throw "SVG render failed for $($file.Name)"
        }
    }

    if ((Test-Path $png) -and ((Get-Item $png).Length -gt 0)) {
        Write-Host "Skipping $($file.Name) -> png"
    } else {
        Write-Host "Rendering $($file.Name) -> png"
        & npx -y -p "@mermaid-js/mermaid-cli@11.12.0" mmdc -i $file.FullName -o $png -p $config -b white --scale 2
        if ($LASTEXITCODE -ne 0) {
            throw "PNG render failed for $($file.Name)"
        }
    }
}

Write-Host "Rendered $($files.Count) Mermaid diagrams to:"
Write-Host "  $svgDir"
Write-Host "  $pngDir"
