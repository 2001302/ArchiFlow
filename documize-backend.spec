# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/user/Source/sample vault/.obsidian/plugins/documize/backend/main.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/user/Source/sample vault/.obsidian/plugins/documize/backend/ai_core', 'ai_core'), ('/Users/user/Source/sample vault/.obsidian/plugins/documize/backend/documize_api', 'documize_api')],
    hiddenimports=['uvicorn.loops.auto', 'uvicorn.loops.asyncio', 'uvicorn.protocols.websockets.auto', 'uvicorn.protocols.http.auto', 'uvicorn.protocols.http.h11_impl', 'uvicorn.protocols.http.httptools_impl', 'uvicorn.lifespan.on', 'fastapi', 'pydantic', 'pydantic_settings', 'openai', 'anthropic', 'httpx', 'loguru', 'jinja2', 'python_multipart', 'ai_core', 'ai_core.providers', 'ai_core.managers', 'ai_core.models', 'ai_core.utils', 'ai_core.config', 'ai_core.processors', 'documize_api', 'documize_api.main'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='documize-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
