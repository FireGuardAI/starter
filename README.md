# FireGuard Starter

Run these commands from `starter/` with Docker Desktop, Git, and Task installed:

```powershell
task clone
task setup-env
task keys
task up
task health
task down
task clean
```

Repositories are cloned as siblings of `starter/` under the workspace root:

```text
D:\SLIIT\fireguard-api
D:\SLIIT\fireguard-frontend
D:\SLIIT\fireguard-agent-intake
D:\SLIIT\fireguard-agent-report
D:\SLIIT\fireguard-agent-compliance
D:\SLIIT\fireguard-agent-retrieval
D:\SLIIT\fireguard-vector-store
```

`task up` starts services sequentially and detached, waiting for each Compose project to become healthy before continuing. `task down` stops containers and keeps the repositories. `task clean` is a destructive fresh reset: it stops Compose projects, removes their volumes and orphans, and deletes the cloned repository folders outside `starter/`.

Edit each generated `.env` before running `task up`, especially API keys required by the compliance and report services.

`task keys` generates missing local values for JWT, PostgreSQL, internal gateway authentication, upload encryption, report signing, and the gateway API-key hash inside a temporary Docker container. Local Python is not required. Existing non-placeholder values are preserved. `GROQ_API_KEY` and `GEMINI_API_KEY` are provider credentials and must be supplied manually; they cannot be generated locally.