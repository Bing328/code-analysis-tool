# 🛡️ Professional Code Auditor v2.0

<div align="center">

![Multi-Platform Build](https://github.com/Bing328/code-analysis-tool/actions/workflows/multi-platform.yml/badge.svg)
![Windows Build](https://github.com/Bing328/code-analysis-tool/actions/workflows/build.yml/badge.svg)
![Release](https://github.com/Bing328/code-analysis-tool/actions/workflows/release.yml/badge.svg)
![GitHub License](https://img.shields.io/github/license/Bing328/code-analysis-tool)
![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20macOS-lightgrey.svg)
![Mode](https://img.shields.io/badge/modes-3-9b59b6.svg)
![Release](https://img.shields.io/github/v/release/Bing328/code-analysis-tool)

**专业代码审计工具 | 全平台自动构建 | 持续集成/部署**

[快速开始](#-快速开始) • [下载](#-下载) • [CI/CD管道](#-cicd-管道) • [功能特性](#-功能特性) • [文档](docs/)

</div>

## 🚀 CI/CD 管道状态

### 工作流状态

| 工作流 | 状态徽章 | 描述 |
|--------|----------|------|
| **多平台构建** | ![Multi-Platform Build](https://github.com/Bing328/code-analysis-tool/actions/workflows/multi-platform.yml/badge.svg) | Windows/Linux/macOS自动构建 |
| **Windows构建** | ![Windows Build](https://github.com/Bing328/code-analysis-tool/actions/workflows/build.yml/badge.svg) | Windows专用可执行文件构建 |
| **发布流程** | ![Release](https://github.com/Bing328/code-analysis-tool/actions/workflows/release.yml/badge.svg) | 自动创建GitHub Release |
| **兼容性测试** | ✅ Python 3.7-3.11 | 多版本Python测试 |

### 自动触发条件
- ✅ **推送代码**到 main/master 分支
- ✅ **创建标签** (v*.*.*格式)
- ✅ **手动触发** (workflow_dispatch)
- ✅ **Pull Request** 构建验证

### 构建产物
每次构建自动生成：
- **Windows**: `CodeAuditor.exe` (单文件可执行程序)
- **Linux**: `CodeAuditor` (Linux可执行文件)
- **macOS**: `CodeAuditor` (macOS应用程序)
- **源码包**: 完整Python源码和文档

## 📥 下载最新版本

### 访问GitHub Releases
**[GitHub Releases](https://github.com/Bing328/code-analysis-tool/releases)** 获取最新版本：

```bash
# Windows用户
下载 CodeAuditor.exe

# Linux用户  
下载 CodeAuditor
chmod +x CodeAuditor

# Python用户
python professional_code_auditor_v2.py


直接链接
最新Windows版本: CodeAuditor.exe
最新Linux版本: CodeAuditor

🔧 快速开始

Windows用

# 1. 下载最新的CodeAuditor.exe
# 2. 双击运行或在命令行执行：
CodeAuditor.exe

Linux用户

# 1. 下载Linux版本
wget https://github.com/Bing328/code-analysis-tool/releases/latest/download/CodeAuditor

# 2. 添加执行权限
chmod +x CodeAuditor

# 3. 运行工具
./CodeAuditor

Python开发者

# 1. 克隆仓库
git clone https://github.com/Bing328/code-analysis-tool.git
cd code-analysis-tool

# 2. 运行Python版本
python3 professional_code_auditor_v2.py

📋 项目结构

.github/workflows/          # GitHub Actions配置
├── multi-platform.yml     # 多平台构建工作流
├── build.yml             # Windows专用构建
├── release.yml           # 发布工作流
└── test.yml             # 测试工作流（可选）

🔄 工作流详情

multi-platform.yml
同时在Windows、Linux、macOS上构建
生成平台特定的可执行文件
上传到GitHub Artifacts

build.yml

专门为Windows优化构建
生成独立的.exe文件
详细的构建验证

release.yml

创建标签时自动触发
生成漂亮的Release页面
包含所有构建产物

📊 徽章使用说明

在README.md中使用的徽章：

![Multi-Platform Build](https://github.com/Bing328/code-analysis-tool/actions/workflows/multi-platform.yml/badge.svg)
![Windows Build](https://github.com/Bing328/code-analysis-tool/actions/workflows/build.yml/badge.svg)
![Release](https://github.com/Bing328/code-analysis-tool/actions/workflows/release.yml/badge.svg)

徽章格式：

https://github.com/<username>/<repository>/actions/workflows/<workflow-file>.yml/badge.svg

🤝 贡献指南

1.Fork本仓库
2.创建功能分支 (git checkout -b feature/AmazingFeature)
3.提交更改 (git commit -m 'Add some AmazingFeature')
4.推送到分支 (git push origin feature/AmazingFeature)
5.开启Pull Request

所有Pull Request会自动运行CI/CD流程验证。

📄 许可证

MIT License - 详见 LICENSE 文件。

⭐ **如果这个项目对你有帮助，请给它一个Star！**
如果你觉得这个项目有用：

Star ⭐ 这个仓库
Watch 👀 关注更新
Fork 🍴 创建自己的版本
分享 🔗 给其他开发者
🌟 如果这个项目对你有帮助，请给它一个Star！



🔧 专业代码审计工具 | 🛡️ 安全开发助手 | 🚀 持续集成支持
                                                                       https://api.star-history.com/svg?repos=Bing328/code-analysis-tool&type=Date
EOF `````

