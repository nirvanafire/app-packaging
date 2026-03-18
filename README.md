# PyQt6 跨平台应用打包项目

一个基于 Python + PyQt6 的跨平台 GUI 应用程序，通过 GitHub Actions 自动构建 Windows、macOS (Intel & Apple Silicon)、Linux 平台的可执行程序。

## 📦 项目特性

- ✅ 支持 Windows (.exe)
- ✅ 支持 macOS Intel (.dmg)
- ✅ 支持 macOS Apple Silicon M1/M2/M3 (.dmg)
- ✅ 支持 Linux (.tar.gz)
- ✅ 自动化构建发布
- ✅ 单文件可执行程序

## 🚀 快速开始

### 本地开发

```bash
# 克隆项目
git clone https://github.com/nirvanafire/app-packaging.git
cd app-packaging

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行应用
python src/main.py
```

### 本地构建

```bash
# 安装 PyInstaller
pip install pyinstaller

# 构建
pyinstaller --noconfirm --onefile --windowed \
  --name "PyQt6Demo" \
  src/main.py
```

## 📋 发布流程

### 方法一：通过 Tag 自动触发

```bash
# 创建并推送 tag
git tag v1.0.0
git push origin v1.0.0
```

### 方法二：手动触发

1. 进入 GitHub 仓库
2. 点击 "Actions" 选项卡
3. 选择 "Build and Release" workflow
4. 点击 "Run workflow"
5. 输入版本号（如 v1.0.1）

## ⚠️ 重要注意事项

### 🔴 跨平台打包核心原则

> **关键原则：必须在本平台构建本平台的程序！**

PyInstaller 打包的可执行文件**不具备跨平台能力**：
- Windows 构建只能运行在 Windows 上
- macOS 构建只能运行在 macOS 上
- Linux 构建只能运行在 Linux 上

**解决方案：使用 GitHub Actions 的多平台 Runner**

| 平台 | Runner 标签 | 架构 |
|------|-------------|------|
| Windows | `windows-latest` | x64 |
| macOS Intel | `macos-13` | x64 |
| macOS Apple Silicon | `macos-14` | arm64 |
| Linux | `ubuntu-latest` | x64 |

### 🍎 macOS ARM 架构兼容性

#### 问题：Intel vs Apple Silicon

macOS 有两种架构：
- **Intel (x86_64)**: 旧款 Mac（2019年前）
- **Apple Silicon (arm64)**: M1/M2/M3 芯片 Mac（2020年后）

#### 解决方案

使用不同的 GitHub Runner 分别构建：

```yaml
# Intel 版本
build-macos-intel:
  runs-on: macos-13  # Intel runner

# Apple Silicon 版本  
build-macos-arm:
  runs-on: macos-14  # M1 runner
```

#### 关于通用二进制 (Universal Binary)

理论上可以创建同时支持 Intel 和 ARM 的 Universal Binary：

```bash
# 分别构建两个版本
pyinstaller --target-architecture x86_64 ...
pyinstaller --target-architecture arm64 ...

# 合并为 Universal Binary
lipo -create -output universal_app dist/app_x64 dist/app_arm64
```

但实际操作中：
- ❗ 需要安装两个架构的 Python 和依赖
- ❗ 复杂度高，容易出错
- ❗ 文件体积翻倍
- ✅ 推荐分别打包两个版本

### 🪟 Windows 打包注意事项

1. **杀毒软件误报**
   - PyInstaller 打包的程序可能被杀毒软件误报为病毒
   - 解决方法：申请代码签名证书，对程序进行签名

2. **缺少运行时**
   - 用户可能缺少 Visual C++ 运行时
   - 解决方法：在 README 中说明需要安装 VC++ 运行时，或打包进程序

3. **管理员权限**
   - 如需管理员权限，需在 PyInstaller 中指定：
     ```bash
     pyinstaller --uac-admin ...
     ```

### 🐧 Linux 打包注意事项

1. **动态链接库问题**
   - 在较新系统构建的程序可能无法在旧系统运行
   - 建议：在 oldest-supported 环境构建

2. **GUI 库依赖**
   - 需要安装 X11 相关库：
     ```bash
     sudo apt-get install libxcb-xinerama0 libxcb-cursor0
     ```

3. **打包格式选择**
   - `.tar.gz`: 简单通用
   - `.AppImage`: 单文件，便携
   - `.deb/.rpm`: 系统包管理器安装

### 📦 PyInstaller 最佳实践

#### 1. 使用 spec 文件管理配置

创建 `PyQt6Demo.spec`：

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('src', 'src')],  # 包含资源文件
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PyQt6Demo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 启用 UPX 压缩
    console=False,  # GUI 程序隐藏控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

#### 2. 减小体积技巧

```bash
# 使用 UPX 压缩（需要先安装 UPX）
pyinstaller --upx-dir=/path/to/upx ...

# 排除不需要的模块
pyinstaller --exclude-module matplotlib --exclude-module numpy ...

# 单文件 vs 单目录
# 单文件 (--onefile): 便携，启动稍慢
# 单目录 (--onedir): 启动快，文件多
```

#### 3. 隐藏导入处理

某些库的动态导入 PyInstaller 无法自动检测：

```python
# 在 spec 文件中添加
hiddenimports=['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets']
```

或使用命令行：

```bash
pyinstaller --hidden-import=module_name ...
```

### 🔐 代码签名（生产环境必需）

#### Windows

```bash
# 使用 signtool
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com PyQt6Demo.exe
```

#### macOS

```bash
# 签名
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name (XXXXXXXXXX)" PyQt6Demo.app

# 公证（Apple 要求）
xcrun notarytool submit PyQt6Demo.dmg --apple-id your@email.com --team-id XXXXXXXXXX --password app-specific-password
```

### 🐛 常见问题排查

#### 问题1：macOS 提示"已损坏"

```bash
# 用户运行以下命令解决
xattr -cr /Applications/PyQt6Demo.app
```

或开发者进行公证签名。

#### 问题2：找不到模块

```bash
# 检查隐藏导入
pyinstaller --log-level DEBUG main.py 2>&1 | grep "import"

# 在 spec 中添加 hiddenimports
```

#### 问题3：图片/资源文件找不到

```python
# 在代码中使用正确的资源路径
import sys
import os

def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发环境和打包后环境"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时目录
        base_path = sys._MEIPASS
    else:
        # 开发环境
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# 使用
icon_path = resource_path("assets/icon.png")
```

#### 问题4：中文乱码

```python
# 确保 Python 文件使用 UTF-8 编码
# 在文件开头添加
# -*- coding: utf-8 -*-

# 控制台输出中文
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 📊 项目结构

```
app-packaging/
├── .github/
│   └── workflows/
│       └── build-release.yml    # GitHub Actions 配置
├── src/
│   └── main.py                  # 应用主程序
├── pyproject.toml               # 项目配置
├── requirements.txt             # 依赖列表
├── README.md                    # 说明文档
└── LICENSE                      # 许可证
```

## 🔧 高级配置

### 添加应用图标

#### Windows (.ico)

```bash
pyinstaller --icon=assets/icon.ico ...
```

#### macOS (.icns)

```bash
# 生成 .icns 文件
mkdir icon.iconset
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset

# 打包时指定
pyinstaller --icon=assets/icon.icns ...
```

### 自动更新功能

推荐使用 `pyupdater` 或 `esky` 库实现自动更新：

```bash
pip install pyupdater
```

## 📚 参考资源

- [PyInstaller 官方文档](https://pyinstaller.org/en/stable/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [PyQt6 官方文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [macOS 代码签名指南](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)

## 📄 许可证

MIT License

---

Made with ❤️ using Python & PyQt6
