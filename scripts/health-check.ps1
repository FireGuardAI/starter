$ErrorActionPreference = 'Continue'

$urls = @(
    @{ Name = 'vector-store'; Url = 'http://localhost:8000/api/v1/heartbeat' }
    @{ Name = 'retrieval'; Url = 'http://localhost:8001/health' }
    @{ Name = 'compliance'; Url = 'http://localhost:8002/health' }
    @{ Name = 'report'; Url = 'http://localhost:8003/health' }
    @{ Name = 'intake'; Url = 'http://localhost:8004/health' }
    @{ Name = 'api'; Url = 'http://localhost:8090/health' }
)

foreach ($item in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $item.Url -UseBasicParsing -TimeoutSec 5
        Write-Host ($item.Name + ' : OK (' + $response.StatusCode + ')') -ForegroundColor Green
    } catch {
        Write-Host ($item.Name + ' : DOWN') -ForegroundColor Red
    }
}
