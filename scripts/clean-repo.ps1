param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath
)

$resolvedPath = Resolve-Path -LiteralPath $RepoPath -ErrorAction SilentlyContinue
if (-not $resolvedPath) {
    Write-Host "Repository not found; skipped: $RepoPath"
    exit 0
}

Push-Location $resolvedPath.Path
try {
    if (Test-Path docker-compose.yml) {
        docker compose down --volumes --remove-orphans
    } elseif (Test-Path compose.yml) {
        docker compose -f compose.yml down --volumes --remove-orphans
    }
} finally {
    Pop-Location
}

Remove-Item -LiteralPath $resolvedPath.Path -Recurse -Force
Write-Host "Removed repository: $RepoPath"
