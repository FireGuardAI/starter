param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath
)

if (-not (Test-Path $RepoPath)) {
    Write-Host "Repository not found; skipped: $RepoPath"
    exit 0
}

$composePath = Join-Path $RepoPath 'docker-compose.yml'
$alternateComposePath = Join-Path $RepoPath 'compose.yml'
if (Test-Path $composePath) {
    docker compose -f $composePath up -d --build --wait
} elseif (Test-Path $alternateComposePath) {
    docker compose -f $alternateComposePath up -d --build --wait
} else {
    Write-Host "No compose file found: $RepoPath"
}
