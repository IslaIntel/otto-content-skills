# Install Otto Content Skills for Claude Code (Windows PowerShell).
#
#   .\install.ps1                                     install every skill
#   .\install.ps1 weekly-social-review reel-diagnosis  install only these
#   .\install.ps1 -List                               show the skills in this pack
#   .\install.ps1 -Remove                             remove the skills this pack installed
#
# Skills go to ~\.claude\skills (override with $env:OTTO_SKILLS_DIR).
param(
  [switch]$List,
  [switch]$Remove,
  [Parameter(ValueFromRemainingArguments = $true)][string[]]$Only
)
$ErrorActionPreference = 'Stop'

$pack = Join-Path $PSScriptRoot 'skills'
$target = if ($env:OTTO_SKILLS_DIR) { $env:OTTO_SKILLS_DIR } else { Join-Path $HOME '.claude\skills' }

if (-not (Test-Path $pack)) {
  Write-Error "Can't find the skills folder next to this script. Run it from the cloned repo."
}

$available = Get-ChildItem -Directory $pack | Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } | ForEach-Object { $_.Name }

if ($List) { $available; return }

if ($Remove) {
  $n = 0
  foreach ($s in $available) {
    $p = Join-Path $target $s
    if (Test-Path $p) { Remove-Item -Recurse -Force $p; $n++ }
  }
  Write-Host "Removed $n Otto skills from $target"
  return
}

$wanted = if ($Only) { $Only } else { $available }
New-Item -ItemType Directory -Force -Path $target | Out-Null
$count = 0
foreach ($s in $wanted) {
  if ($available -notcontains $s) { Write-Host "  skipped $s (not in this pack; see .\install.ps1 -List)"; continue }
  $dest = Join-Path $target $s
  if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
  Copy-Item -Recurse (Join-Path $pack $s) $dest
  $count++
}

Write-Host "Installed $count Otto skills into $target"
Write-Host 'Next: connect Otto (https://ottowebmaster.com/introduction/mcp/claude), restart Claude Code, then ask "set up my brand brain".'
