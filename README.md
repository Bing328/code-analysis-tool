# 🛡️ Professional Code Auditor v2.0

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey.svg)
![Mode](https://img.shields.io/badge/modes-3-9b59b6.svg)

**多模式、隐私保护的代码安全审计工具**

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [使用指南](docs/USAGE_GUIDE.md) • [功能详解](docs/FEATURES.md)

</div>

---

## 📖 简介

**Professional Code Auditor v2.0** 是一款专为开发者和安全工程师设计的代码审计工具。它提供三种分析模式（离线、在线漏洞库、AI智能分析），支持多种编程语言，并特别注重用户隐私保护。

无论是日常代码审查、CI/CD 流水线集成，还是敏感环境下的安全扫描，本工具都能提供专业的支持。

## ✨ 功能特性

### 🔧 三种分析模式
| 模式 | 描述 | 适用场景 |
| :--- | :--- | :--- |
| **🚀 离线分析** | 本地全面扫描，极速且零网络依赖 | 内网环境、敏感项目、快速检查 |
| **☁️ 在线模式** | 接入免费云端漏洞库 (CVE/CWE) | 开源项目、合规性检查 |
| **🤖 AI 智能分析** | 深度代码质量分析与优化建议 | 代码重构、质量提升 |

### 🔐 隐私保护承诺
- **本地加密存储**：API 密钥采用 Base64 编码加密存储，永不上传明文。
- **内容自动脱敏**：上传至云端分析前，自动移除密码、Token 等敏感信息。
- **匿名化处理**：文件标识采用 Hash 处理，无法追踪源文件。

### 📊 核心能力
- **多语言支持**：Python, Java, C/C++, JavaScript, Go, Rust, SQL 等 20+ 种语言。
- **二进制检测**：智能识别 .exe, .dll, .so, .jar 等二进制文件。
- **安全扫描**：硬编码凭证、SQL 注入、命令注入、XSS 等常见漏洞检测。
- **Docker 审计**：Dockerfile 最佳实践与安全配置检查。
- **可视化报告**：生成美观的 HTML 交互式报告。

## 🚀 快速开始

### 环境要求
- Python 3.7 或更高版本
- **无需安装任何第三方依赖库** (基于 Python 标准库)

### 安装
```bash
# 克隆仓库
git clone https://github.com/yourusername/professional-code-auditor.git
cd professional-code-auditor

# (可选) 虽然无外部依赖，但习惯上可以检查环境
python --version

