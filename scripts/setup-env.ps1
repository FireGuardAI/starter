$ErrorActionPreference = 'Stop'

$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$repositoryNames = @(
    'fireguard-vector-store'
    'fireguard-agent-retrieval'
    'fireguard-agent-compliance'
    'fireguard-agent-report'
    'fireguard-agent-intake'
    'fireguard-api'
    'fireguard-frontend'
)

foreach ($name in $repositoryNames) {
    $directory = Join-Path $root $name
    $envPath = Join-Path $directory '.env'
    $examplePath = Join-Path $directory '.env.example'
    if (Test-Path $envPath) {
        Write-Host ".env exists: $name"
    } elseif (Test-Path $examplePath) {
        Copy-Item $examplePath $envPath
        Write-Host "Created .env: $name"
    } else {
        Write-Host "No .env.example: $name"
    }
}
