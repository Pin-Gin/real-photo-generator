#Requires -Version 5.1
[CmdletBinding()]
param(
    [string]$Root = 'D:\AI\real-photo-generator'
)
$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath 'D:\' -PathType Container)) {
    throw 'D: drive is not available. No folders were created.'
}

$repo = Join-Path $Root 'repo'
if (-not (Test-Path -LiteralPath (Join-Path $repo '.git') -PathType Container)) {
    throw "Repository not cloned at $repo. Complete the Git step first."
}
if (-not (Test-Path -LiteralPath (Join-Path $repo 'docs\requirements\REQUIREMENTS_V1.md') -PathType Leaf)) {
    throw 'Git scaffold is incomplete. Do not continue with D-drive setup.'
}

$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) { throw 'git.exe is required to validate the repository.' }
$remote = (& git -C $repo remote get-url origin 2>$null)
if ($LASTEXITCODE -ne 0) { throw 'Cannot read Git origin URL.' }
$valid = @('https://github.com/Pin-Gin/real-photo-generator.git', 'https://github.com/Pin-Gin/real-photo-generator', 'git@github.com:Pin-Gin/real-photo-generator.git')
if ($valid -notcontains ($remote.Trim())) { throw "Unexpected Git origin: $remote" }

# Make sure the remote Git branch contains the local scaffold before the next stage.
$remoteInfo = (& git -C $repo ls-remote origin refs/heads/main 2>$null)
if ($LASTEXITCODE -ne 0 -or -not $remoteInfo) { throw 'Cannot confirm remote main. Confirm network/Git access first.' }
$remoteSha = (($remoteInfo | Select-Object -First 1) -split '\s+')[0]
$localSha = (& git -C $repo rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $localSha -ne $remoteSha) {
    throw 'Git local HEAD and remote main differ. Complete the Git update before D-drive folder creation.'
}

$dirs = @(
    'runtime\comfyui',
    'runtime\python',
    'runtime\video-tools',
    'assets\models',
    'assets\references\incoming',
    'assets\references\masters',
    'assets\references\poses',
    'outputs\quality-tests',
    'outputs\approved',
    'outputs\videos\quality-tests',
    'outputs\videos\approved',
    'outputs\video-frames',
    'backups\downloaded-apps',
    'backups\downloaded-models',
    'backups\manifests',
    'state',
    'logs',
    'temp'
)

foreach ($dir in $dirs) {
    $path = Join-Path $Root $dir
    if (Test-Path -LiteralPath $path -PathType Leaf) {
        throw "A file blocks a required directory: $path"
    }
    if (-not (Test-Path -LiteralPath $path -PathType Container)) {
        New-Item -ItemType Directory -Path $path -Force -ErrorAction Stop | Out-Null
        Write-Host "[CREATED] $path"
    }
    else { Write-Host "[EXISTS]  $path" }
}
Write-Host '[DONE] D-drive empty directory layout created; no models or applications were moved or installed.'
