# 🧹 Codebase Cleanup Plan

**Goal:** Create a clean, production-ready variant for GitHub/deployment
**Current Size:** 11GB (mostly in resource_repos: 5.5GB)
**Total Python Files:** 14,030 files

## 📊 Analysis Summary

### Large Directories to Remove/Archive
1. **resource_repos/** - 5.5GB (old code, examples, other projects)
2. **extra-guides/** - 1.4MB (planning guides, not needed in production)
3. **pages_backup/** - 104KB (old Streamlit pages format)
4. **other_repos/** - Unknown size (external repos)

### Temporary/Generated Files to Remove
- `__pycache__/` directories
- `.pytest_cache/`
- `*.log` files
- `temp_files/`, `temp_uploads/`
- `outputs/`, `runs/`
- `task_artifacts/`
- `.DS_Store` files
- `campaign_assets.zip`

### Test Files to Remove (or move to specs/)
- `test_*.py` in root
- `*_test.py` files
- Testing tools scattered around

### Duplicate/Legacy Files to Remove
- `nova_system_pro.py` (keep main one)
- `nova_system.py.backup`
- `email_marketing_service_old.py`
- `streamlit_app.py` (use nova_system.py)
- Legacy workflow converters
- Old platform integration files

### Documentation to Keep (but organize)
- README.md ✓
- DOCKER.md ✓
- requirements.txt ✓
- .env.example ✓

### Core Application Files (KEEP)
All `abp_*.py` files (main application tabs)
- nv_abp_dashboard.py
- nv_abp_products.py
- nv_abp_campaigns.py
- nv_abp_content.py
- etc.

### Core Service Files (KEEP)
- nv_api_service.py
- nv_global_job_queue.py
- nv_fastapi_backend.py
- nv_tab_job_helpers.py
- nv_platform_helpers.py
- nv_background_tasks.py
- session_manager.py
- etc.

## 🎯 Cleanup Strategy

### Phase 1: Safe Archive (Don't Delete Yet)
Create `archive/` directory and move:
- resource_repos/
- extra-guides/
- pages_backup/
- other_repos/

### Phase 2: Remove Generated/Temp Files
Safe to delete immediately:
- All `__pycache__/`
- `.pytest_cache/`
- `*.log` files
- temp_files/, temp_uploads/
- outputs/, runs/
- task_artifacts/
- .DS_Store files

### Phase 3: Consolidate Structure
Create clean directory structure:
```
nv_printify-clean/
├── core/
│   ├── tabs/          # All abp_*.py files
│   ├── services/      # Core services
│   ├── utils/         # Helper utilities
│   └── models/        # Data models
├── backend/           # FastAPI backend
├── config/            # Configuration files
├── static/            # Static assets
├── specs/             # All test files
├── guides/              # Essential guides only
├── tools/           # Deployment/setup tools
├── requirements.txt
├── .env.example
└── README.md
```

### Phase 4: Remove Duplicates/Legacy
- Identify and remove duplicate functionality
- Remove old/unused service files
- Clean up migration tools

## 📋 Estimated Reduction
- Current: 11GB, 14,030 files
- After cleanup: ~500MB-1GB, ~200-300 core files
- **~90% size reduction**

## ⚠️ Safety First
1. Create new branch: `git checkout -b cleanup-production`
2. Archive before deleting
3. Test after each phase
4. Keep git history intact
