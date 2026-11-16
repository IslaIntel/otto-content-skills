# Otto Content Skills installer: copies each skill into ~/.claude/skills/
$ErrorActionPreference = 'Stop'

$skillsDir = Join-Path $HOME '.claude\skills'
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null

Get-ChildItem -Directory (Join-Path $PSScriptRoot 'skills') | ForEach-Object {
    $dest = Join-Path $skillsDir $_.Name
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Item -Recurse -Force (Join-Path $_.FullName '*') $dest
    Write-Host "  installed $($_.Name)"
}

Write-Host ''
Write-Host 'Done. Restart Claude Code, connect Otto, then ask: "weekly review"'
Write-Host 'Otto: https://ottowebmaster.com'
