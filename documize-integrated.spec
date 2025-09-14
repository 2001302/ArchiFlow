# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/user/Source/sample vault/.obsidian/plugins/documize/backend/main.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/user/Source/sample vault/.obsidian/plugins/documize/backend/mcp_server', 'mcp_server'), ('/Users/user/Source/sample vault/.obsidian/plugins/documize/backend/documize_api', 'documize_api')],
    hiddenimports=['uvicorn.loops.auto', 'uvicorn.loops.asyncio', 'uvicorn.protocols.websockets.auto', 'uvicorn.protocols.http.auto', 'uvicorn.protocols.http.h11_impl', 'uvicorn.protocols.http.httptools_impl', 'uvicorn.lifespan.on', 'fastapi', 'pydantic', 'pydantic_settings', 'openai', 'anthropic', 'httpx', 'loguru', 'jinja2', 'python_multipart', 'mcp_server', 'mcp_server.providers', 'mcp_server.managers', 'mcp_server.models', 'mcp_server.utils', 'mcp_server.config', 'mcp_server.processors', 'mcp_server.mcp_tool', 'mcp_server.mcp_tool.tools', 'mcp_server.mcp_tool.tools.ai_generation', 'mcp_server.mcp_tool.tools.vault_operations', 'mcp_server.mcp_tool.tools.content_management', 'documize_api', 'documize_api.main'],
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
    name='documize-integrated',
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
