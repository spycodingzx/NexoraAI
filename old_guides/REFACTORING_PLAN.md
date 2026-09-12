# Refactoring Plan for Autonomous Business Platform (Clean Repo)

## Current Issues
1. **55 symlinks in root** pointing to `core/tabs/` files
2. **69 real Python files scattered in root** that should be organized
3. **Imports use root-level symlinks** instead of proper module paths
4. **Mixed structure** - some files in `core/` folders, others loose in root

## Target Structure (Best Practices)
```
nova_system/
├── nova_system.py  (main entry point)
├── requirements.txt
├── .python-version
├── packages.txt
├── README.md
├── STREAMLIT_DEPLOYMENT.md
│
├── core/
│   ├── __init__.py
│   │
│   ├── tabs/                 # All UI tab plugins
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── campaigns.py
│   │   ├── products.py
│   │   └── ... (all other tabs)
│   │
│   ├── services/             # Business logic & API integrations
│   │   ├── __init__.py
│   │   ├── nv_api_service.py
│   │   ├── nv_shopify_service.py
│   │   ├── nv_credential_manager.py
│   │   ├── nv_secure_config.py
│   │   └── ... (AI services, background tasks, etc)
│   │
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   ├── nv_prompt_templates.py
│   │   ├── nv_video_export_utils.py
│   │   └── nv_performance_optimizations.py
│   │
│   ├── models/               # Data models & schemas
│   │   ├── __init__.py
│   │   └── ... (if any)
│   │
│   └── core/                 # Core business logic
│       ├── __init__.py
│       ├── campaign_engine.py
│       ├── content_generator.py
│       └── ... (major features)
│
├── config/                   # Configuration files
│   └── nv_brand_templates.json
│
├── static/                   # Static assets
│   └── assets/
│
├── specs/                    # Test files
│   └── ...
│
└── guides/                     # Documentation
    └── ...
```

## Refactoring Steps

### Phase 1: Remove Symlinks (Safe - No Code Changes)
- Delete all 55 symlinks from root
- Files already exist in `core/tabs/` so nothing breaks

### Phase 2: Organize Root-Level Service Files
Move scattered service files to proper locations:
- `nv_ai_twitter_poster.py` → `core/services/`
- `nv_background_task_manager.py` → `core/services/`
- `nv_blog_generator.py` → `core/services/`
- `nv_digital_product_generator.py` → `core/services/`
- `nv_multi_platform_poster.py` → `core/services/`
- `nv_social_media_ad_service.py` → `core/services/`
- And ~60 more similar files

### Phase 3: Update Import Statements
Update `nova_system.py`:
```python
# OLD
from nv_abp_sidebar import render_sidebar
from nv_abp_config import AppConfig

# NEW
from core.tabs.sidebar import render_sidebar
from core.tabs.config import AppConfig
```

### Phase 4: Rename Tab Files (Remove `abp_` Prefix)
- `core/tabs/nv_abp_dashboard.py` → `core/tabs/dashboard.py`
- `core/tabs/nv_abp_sidebar.py` → `core/tabs/sidebar.py`
- Cleaner imports, less redundant naming

### Phase 5: Test Everything
- Run locally on port 8502
- Verify all tabs load
- Check all features work
- Fix any import issues

### Phase 6: Deploy
- Commit changes
- Push to GitHub
- Verify Streamlit Cloud deployment

## Safety Measures
✅ Work on printify_clean only (not nv_printify)
✅ Test after each major change
✅ Keep git commits granular for easy rollback
✅ Backup before starting
