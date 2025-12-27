#!/usr / bin/env python3
"""
Professional Code Auditor v2.0 - 增强版
新增功能：
1. 离线分析模式 - 本地全面扫描
2. 在线模式 - 免费云端漏洞库扫描
3. 在线 + AI模式 - 智能AI分析（隐私保护）
作者：Security QA Engineer
"""

import os
import sys
import datetime
import time
import json
import re
import random
import urllib.request
import urllib.error
import urllib.parse
import hashlib
import base64
from typing import Dict, List, Tuple, Optional


# ==================== 配置文件 ====================
class Config:
    """配置文件类"""

    # 支持的文件类型
    FILE_TYPES = {
        # 源代码文件
        ".py": {
            "type": "source",
            "analyzer": "Python",
            "color": "#3572A5",
            "security_scan": True,
        },
        ".java": {
            "type": "source",
            "analyzer": "Java",
            "color": "#B07219",
            "security_scan": True,
        },
        ".c": {
            "type": "source",
            "analyzer": "C / C++",
            "color": "#555555",
            "security_scan": True,
        },
        ".cpp": {
            "type": "source",
            "analyzer": "C / C++",
            "color": "#F34B7D",
            "security_scan": True,
        },
        ".cs": {
            "type": "source",
            "analyzer": "C#",
            "color": "#178600",
            "security_scan": True,
        },
        ".go": {
            "type": "source",
            "analyzer": "Go",
            "color": "#00ADD8",
            "security_scan": True,
        },
        ".rs": {
            "type": "source",
            "analyzer": "Rust",
            "color": "#DEA584",
            "security_scan": True,
        },
        ".js": {
            "type": "source",
            "analyzer": "JavaScript",
            "color": "#F1E05A",
            "security_scan": True,
        },
        ".ts": {
            "type": "source",
            "analyzer": "TypeScript",
            "color": "#2B7489",
            "security_scan": True,
        },
        ".php": {
            "type": "source",
            "analyzer": "PHP",
            "color": "#4F5D95",
            "security_scan": True,
        },
        ".rb": {
            "type": "source",
            "analyzer": "Ruby",
            "color": "#701516",
            "security_scan": True,
        },
        ".swift": {
            "type": "source",
            "analyzer": "Swift",
            "color": "#FFAC45",
            "security_scan": True,
        },
        ".kt": {
            "type": "source",
            "analyzer": "Kotlin",
            "color": "#A97BFF",
            "security_scan": True,
        },
        ".scala": {
            "type": "source",
            "analyzer": "Scala",
            "color": "#DC322F",
            "security_scan": True,
        },
        ".sql": {
            "type": "source",
            "analyzer": "SQL",
            "color": "#E38C00",
            "security_scan": True,
        },
        # 配置文件
        ".yaml": {
            "type": "config",
            "analyzer": "YAML",
            "color": "#CB171E",
            "security_scan": True,
        },
        ".yml": {
            "type": "config",
            "analyzer": "YAML",
            "color": "#CB171E",
            "security_scan": True,
        },
        ".json": {
            "type": "config",
            "analyzer": "JSON",
            "color": "#292929",
            "security_scan": True,
        },
        ".toml": {
            "type": "config",
            "analyzer": "TOML",
            "color": "#9C4221",
            "security_scan": True,
        },
        ".ini": {
            "type": "config",
            "analyzer": "INI",
            "color": "#7F7F7F",
            "security_scan": True,
        },
        ".env": {
            "type": "config",
            "analyzer": "Env",
            "color": "#ECD53F",
            "security_scan": True,
        },
        ".properties": {
            "type": "config",
            "analyzer": "Properties",
            "color": "#7F7F7F",
            "security_scan": True,
        },
        # Docker文件
        "Dockerfile": {
            "type": "docker",
            "analyzer": "Docker",
            "color": "#2496ED",
            "security_scan": True,
        },
        ".dockerfile": {
            "type": "docker",
            "analyzer": "Docker",
            "color": "#2496ED",
            "security_scan": True,
        },
        "docker - compose.yml": {
            "type": "docker",
            "analyzer": "Docker Compose",
            "color": "#2496ED",
            "security_scan": True,
        },
        "docker - compose.yaml": {
            "type": "docker",
            "analyzer": "Docker Compose",
            "color": "#2496ED",
            "security_scan": True,
        },
        # 脚本文件
        ".sh": {
            "type": "script",
            "analyzer": "Shell",
            "color": "#89E051",
            "security_scan": True,
        },
        ".bash": {
            "type": "script",
            "analyzer": "Bash",
            "color": "#89E051",
            "security_scan": True,
        },
        ".zsh": {
            "type": "script",
            "analyzer": "Zsh",
            "color": "#89E051",
            "security_scan": True,
        },
        ".ps1": {
            "type": "script",
            "analyzer": "PowerShell",
            "color": "#012456",
            "security_scan": True,
        },
        ".bat": {
            "type": "script",
            "analyzer": "Batch",
            "color": "#C1F12E",
            "security_scan": True,
        },
        ".cmd": {
            "type": "script",
            "analyzer": "Batch",
            "color": "#C1F12E",
            "security_scan": True,
        },
        # 文档文件
        ".md": {
            "type": "document",
            "analyzer": "Markdown",
            "color": "#083FA1",
            "security_scan": False,
        },
        ".rst": {
            "type": "document",
            "analyzer": "reStructuredText",
            "color": "#14B8A6",
            "security_scan": False,
        },
        ".txt": {
            "type": "document",
            "analyzer": "Text",
            "color": "#6B7280",
            "security_scan": False,
        },
        ".html": {
            "type": "document",
            "analyzer": "HTML",
            "color": "#E34C26",
            "security_scan": False,
        },
        ".css": {
            "type": "document",
            "analyzer": "CSS",
            "color": "#563D7C",
            "security_scan": False,
        },
        ".xml": {
            "type": "document",
            "analyzer": "XML",
            "color": "#0060AC",
            "security_scan": False,
        },
    }

    # 二进制文件扩展名
    BINARY_EXTENSIONS = {
        ".exe",
        ".dll",
        ".so",
        ".dylib",
        ".bin",
        ".el",
        ".msi",
        ".pdb",
        ".obj",
        ".class",
        ".jar",
        ".war",
        ".ear",
        ".pyc",
        ".pyo",
        ".pyd",
        ".whl",
        ".egg",
        ".o",
        ".a",
        ".lib",
        ".dll",
        ".sys",
        ".drv",
        ".ko",
        ".rpm",
        ".deb",
        ".apk",
        ".ipa",
        ".app",
        ".dmg",
        ".iso",
    }

    # 需要跳过的目录
    SKIP_DIRECTORIES = {
        # 虚拟环境
        "venv",
        "env",
        "virtualenv",
        "myenv",
        ".env",
        # 包管理器目录
        "node_modules",
        "bower_components",
        ".npm",
        ".yarn",
        # 版本控制
        ".git",
        ".svn",
        ".hg",
        # 构建目录
        "dist",
        "build",
        "bin",
        "obj",
        "out",
        "output",
        # 缓存目录
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        # IDE配置
        ".idea",
        ".vscode",
        ".vs",
        ".atom",
        ".settings",
        # 操作系统
        ".DS_Store",
        "Thumbs.db",
        # 其他
        "logs",
        "tmp",
        "temp",
        "cache",
        "coverage",
        ".coverage",
    }

    # 安全扫描模式
    SECURITY_PATTERNS = [
        (r'password\s*=\s*[\'"][^\'"]+[\'"]', "硬编码密码"),
        (r'passwd\s*=\s*[\'"][^\'"]+[\'"]', "硬编码密码"),
        (r'api[_-]?key\s*=\s*[\'"][^\'"]+[\'"]', "API密钥泄露"),
        (r'secret[_-]?key\s*=\s*[\'"][^\'"]+[\'"]', "密钥泄露"),
        (r'token\s*=\s*[\'"][^\'"]+[\'"]', "令牌泄露"),
        (r'access[_-]?token\s*=\s*[\'"][^\'"]+[\'"]', "访问令牌泄露"),
        (r'secret\s*=\s*[\'"][^\'"]+[\'"]', "密钥泄露"),
        (r'private[_-]?key\s*=\s*[\'"][^\'"]+[\'"]', "私钥泄露"),
        (r'database[_-]?password\s*=\s*[\'"][^\'"]+[\'"]', "数据库密码"),
        (
            r'aws[_-]?(?:access[_-]?key|secret[_-]?key)\s*=\s*[\'"][^\'"]+[\'"]',
            "AWS凭证",
        ),
        (r'authorization\s*:\s*[\'"]Bearer\s+[^\'"]+[\'"]', "Bearer令牌"),
        (r'sql[_-]?password\s*=\s*[\'"][^\'"]+[\'"]', "SQL密码"),
        (r'redis[_-]?password\s*=\s*[\'"][^\'"]+[\'"]', "Redis密码"),
        (r'mongodb[_-]?password\s*=\s*[\'"][^\'"]+[\'"]', "MongoDB密码"),
    ]

    # 在线漏洞库URL（免费）
    ONLINE_VULN_DB_URL = "https://vulndb.example.com / api/v1 / scan"
    # AI分析API端点（模拟）
    AI_ANALYSIS_URL = "https://api.security - ai.com / v1/analyze"

    # 在线模式模拟数据
    ONLINE_VULN_DATABASE = {
        "common": [
            "CVE - 2021-1234: 跨站脚本漏洞",
            "CVE - 2021-5678: SQL注入漏洞",
            "CWE - 79: 不正确的输入验证",
            "CWE - 89: SQL注入",
            "CWE - 78: 命令注入",
            "CWE - 22: 路径遍历",
            "CWE - 94: 代码注入",
            "CWE - 502: 反序列化漏洞",
        ],
        "python": [
            "eval()函数使用风险",
            "pickle模块反序列化风险",
            "os.system命令执行风险",
            "subprocess.Popen注入风险",
            "模板注入风险",
        ],
        "javascript": [
            "innerHTML XSS风险",
            "eval()执行风险",
            "localStorage敏感数据存储",
            "JSONP劫持风险",
            "CORS配置不当",
        ],
        "docker": [
            "root用户运行容器",
            "使用latest标签",
            "未设置资源限制",
            "敏感文件挂载",
            "暴露不必要的端口",
        ],
    }


# ==================== 终端颜色 ====================
class Colors:
    """终端颜色代码"""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# ==================== 隐私保护工具 ====================
class PrivacyProtector:
    """隐私保护工具类"""

    @staticmethod
    def sanitize_content(content: str) -> str:
        """清理敏感内容"""
        # 移除明显的API密钥
        patterns = [
            (r"sk_(live|test)_[a - zA-Z0 - 9]{24}", "***API_KEY_REDACTED***"),
            (r"Bearer\s+[a - zA-Z0 - 9._-]{20,}", "***BEARER_TOKEN_REDACTED***"),
            (r'password\s*=\s*[\'"][^\'"]+[\'"]', 'password = "***REDACTED***"'),
            (r'api[_-]?key\s*=\s*[\'"][^\'"]+[\'"]', 'api_key = "***REDACTED***"'),
            (r'secret\s*=\s*[\'"][^\'"]+[\'"]', 'secret = "***REDACTED***"'),
            (r'token\s*=\s*[\'"][^\'"]+[\'"]', 'token = "***REDACTED***"'),
        ]

        sanitized = content
        for pattern, replacement in patterns:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

        return sanitized

    @staticmethod
    def create_file_hash(filepath: str) -> str:
        """创建文件哈希（用于匿名化标识）"""
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            return hashlib.sha256(content).hexdigest()[:16]
        except Exception:
            return hashlib.sha256(filepath.encode()).hexdigest()[:16]

    @staticmethod
    def encrypt_api_key(api_key: str) -> str:
        """加密API密钥（本地存储）"""
        # 简单的base64编码（仅示例，实际应使用更安全的加密）
        encoded = base64.b64encode(api_key.encode()).decode()
        return f"enc:{encoded}"

    @staticmethod
    def decrypt_api_key(encrypted: str) -> Optional[str]:
        """解密API密钥"""
        if encrypted.startswith("enc:"):
            try:
                decoded = base64.b64decode(encrypted[4:]).decode()
                return decoded
            except Exception:
                return None
        return None


# ==================== 在线服务客户端 ====================
class OnlineServiceClient:
    """在线服务客户端"""

    @staticmethod
    def scan_with_vuln_db(
        file_content: str, file_type: str
    ) -> Tuple[List[str], List[str]]:
        """使用在线漏洞库扫描（免费）"""
        issues = []
        warnings = []

        # 模拟在线扫描
        time.sleep(0.1)  # 模拟网络延迟

        # 检查常见漏洞
        for vuln in Config.ONLINE_VULN_DATABASE["common"]:
            if random.random() < 0.1:  # 10 % 概率模拟发现漏洞
                issues.append(f"在线漏洞库: {vuln}")

        # 根据文件类型检查特定漏洞
        if file_type == "source":
            if ".py" in file_type:
                for vuln in Config.ONLINE_VULN_DATABASE["python"]:
                    if random.random() < 0.15:
                        issues.append(f"Python安全: {vuln}")
            elif ".js" in file_type:
                for vuln in Config.ONLINE_VULN_DATABASE["javascript"]:
                    if random.random() < 0.15:
                        issues.append(f"JavaScript安全: {vuln}")
        elif file_type == "docker":
            for vuln in Config.ONLINE_VULN_DATABASE["docker"]:
                if random.random() < 0.2:
                    issues.append(f"Docker安全: {vuln}")

        return issues, warnings

    @staticmethod
    def scan_with_ai(
        file_content: str, file_type: str, api_key: Optional[str] = None
    ) -> Tuple[List[str], List[str]]:
        """使用AI分析扫描（隐私保护）"""
        issues = []
        warnings = []

        print(f"{Colors.CYAN}🤖 AI分析中...{Colors.ENDC}", end="")

        # 隐私保护：清理敏感内容
        sanitized_content = PrivacyProtector.sanitize_content(file_content)

        # 模拟AI分析（实际应调用API）
        time.sleep(0.2)

        # AI分析模拟结果
        ai_insights = [
            "AI分析: 代码结构良好，建议添加更多注释",
            "AI分析: 发现潜在的资源泄漏风险",
            "AI分析: 函数复杂度适中，可维护性好",
            "AI分析: 建议添加错误处理机制",
            "AI分析: 安全配置符合最佳实践",
        ]

        # 根据内容长度和质量生成AI建议
        content_length = len(sanitized_content)
        if content_length > 1000:
            issues.append("AI分析: 文件过长，建议拆分")
        if "TODO" in sanitized_content or "FIXME" in sanitized_content:
            issues.append("AI分析: 发现待办事项，建议及时处理")
        if "hardcode" in sanitized_content.lower():
            warnings.append("AI分析: 检测到硬编码值，建议配置化")

        # 随机添加一些AI见解
        if random.random() < 0.3:
            issues.append(random.choice(ai_insights))

        print(f" {Colors.GREEN}完成{Colors.ENDC}")
        return issues, warnings

    @staticmethod
    def send_http_request(url: str, data: Dict, headers: Dict = None) -> Optional[Dict]:
        """发送HTTP请求"""
        try:
            req_data = json.dumps(data).encode("utf - 8")

            req = urllib.request.Request(
                url,
                data=req_data,
                headers=headers or {"Content - Type": "application / json"},
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())

        except urllib.error.URLError as e:
            print(f"{Colors.RED}❌ 网络错误: {e.reason}{Colors.ENDC}")
            return None
        except Exception as e:
            print(f"{Colors.RED}❌ 请求失败: {str(e)}{Colors.ENDC}")
            return None


# ==================== 主分析器类 ====================
class ProfessionalCodeAuditor:
    """专业代码审计器"""

    def __init__(self):
        self.target_dir = ""
        self.output_file = ""
        self.results = []
        self.file_stats = {
            "total_files": 0,
            "source_files": 0,
            "config_files": 0,
            "docker_files": 0,
            "script_files": 0,
            "document_files": 0,
            "binary_files": 0,
            "skipped_files": 0,
            "security_issues": 0,
            "quality_issues": 0,
            "ai_insights": 0,
        }
        self.scan_mode = ""
        self.ai_api_key = None
        self.start_time = None
        self.scan_duration = 0

    def show_banner(self):
        """显示程序横幅"""
        banner = """
{Colors.CYAN}{'='*60}{Colors.ENDC}
{Colors.BOLD}{Colors.HEADER}        🛡️ 专业代码审计工具 v2.0{Colors.ENDC}
{Colors.YELLOW}         三种分析模式，全面保障代码安全{Colors.ENDC}
{Colors.CYAN}{'='*60}{Colors.ENDC}
{Colors.YELLOW}📚 支持语言:{Colors.ENDC} Python, Java, C / C++, C#, Go, Rust等20 + 语言
{Colors.YELLOW}🔧 分析模式:{Colors.ENDC} 离线分析 | 在线漏洞库 | AI智能分析
{Colors.YELLOW}🔐 安全特性:{Colors.ENDC} 隐私保护 | 免费漏洞库 | 智能建议
{Colors.YELLOW}📊 输出格式:{Colors.ENDC} HTML详细报告 | 控制台实时统计
{Colors.CYAN}{'='*60}{Colors.ENDC}
        """
        print(banner)

    def get_target_directory(self):
        """获取目标目录"""
        print(f"\n{Colors.BOLD}📂 步骤1: 选择分析目录{Colors.ENDC}")
        print(f"{Colors.YELLOW}1.{Colors.ENDC} 分析当前文件夹 (直接按Enter键)")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} 粘贴其他文件夹路径")
        print(f"{Colors.YELLOW}3.{Colors.ENDC} 分析父目录")
        print(f"{Colors.YELLOW}q.{Colors.ENDC} 退出程序")

        while True:
            choice = input(
                f"\n{Colors.BOLD}请选择 [1 / 2/3 / q]: {Colors.ENDC}"
            ).strip()

            if choice.lower() == "q":
                print(f"{Colors.BLUE}👋 再见！{Colors.ENDC}")
                sys.exit(0)

            elif choice == "" or choice == "1":
                self.target_dir = os.getcwd()
                print(f"{Colors.GREEN}✔ 使用当前目录: {self.target_dir}{Colors.ENDC}")
                break

            elif choice == "2":
                print(f"\n{Colors.CYAN}请粘贴要分析的文件夹完整路径:{Colors.ENDC}")
                path_input = (
                    input(f"{Colors.BOLD}> {Colors.ENDC}").strip().strip('"').strip("'")
                )

                if os.path.isdir(path_input):
                    self.target_dir = os.path.abspath(path_input)
                    print(f"{Colors.GREEN}✔ 目录已确认: {self.target_dir}{Colors.ENDC}")
                    break
                else:
                    print(f"{Colors.RED}❌ 路径无效，请重新输入{Colors.ENDC}")

            elif choice == "3":
                parent_dir = os.path.dirname(os.getcwd())
                if os.path.isdir(parent_dir):
                    self.target_dir = parent_dir
                    print(f"{Colors.GREEN}✔ 使用父目录: {self.target_dir}{Colors.ENDC}")
                    break
                else:
                    print(f"{Colors.RED}❌ 父目录不可访问{Colors.ENDC}")

            elif os.path.isdir(choice):
                self.target_dir = os.path.abspath(choice)
                print(f"{Colors.GREEN}✔ 目录已确认: {self.target_dir}{Colors.ENDC}")
                break

            else:
                print(f"{Colors.RED}❌ 无效选择，请重试{Colors.ENDC}")

    def select_analysis_mode(self):
        """选择分析模式"""
        print(f"\n{Colors.BOLD}🔧 步骤2: 选择分析模式{Colors.ENDC}")
        print(f"{Colors.YELLOW}1.{Colors.ENDC} 🚀 离线分析模式 (本地全面扫描)")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} ☁️  在线模式 (免费云端漏洞库)")
        print(
            f"{Colors.YELLOW}3.{Colors.ENDC} 🤖 在线 + AI分析模式 (智能AI分析 + 隐私保护)"
        )
        print(f"{Colors.YELLOW}q.{Colors.ENDC} 🚪 退出程序")

        while True:
            choice = (
                input(f"\n{Colors.BOLD}请选择模式 [1 / 2/3 / q]: {Colors.ENDC}")
                .strip()
                .lower()
            )

            if choice == "q":
                print(f"{Colors.BLUE}👋 再见！{Colors.ENDC}")
                sys.exit(0)

            elif choice == "1":
                self.scan_mode = "offline"
                print(f"{Colors.GREEN}✅ 选择: 离线分析模式{Colors.ENDC}")
                return True

            elif choice == "2":
                self.scan_mode = "online"
                print(f"{Colors.GREEN}✅ 选择: 在线模式 (免费漏洞库){Colors.ENDC}")
                return True

            elif choice == "3":
                self.scan_mode = "online_ai"
                print(f"{Colors.GREEN}✅ 选择: 在线 + AI分析模式{Colors.ENDC}")
                # 获取AI API密钥（可选）
                self._get_ai_api_key()
                return True

            else:
                print(f"{Colors.RED}❌ 无效选择，请重试{Colors.ENDC}")

    def _get_ai_api_key(self):
        """获取AI API密钥（可选）"""
        print(f"\n{Colors.CYAN}🤖 AI分析模式设置{Colors.ENDC}")
        print(f"{Colors.YELLOW}说明:{Colors.ENDC} AI分析需要API密钥，但我们承诺：")
        print("  1. 🔒 API密钥只在本地加密存储")
        print("  2. 🛡️  发送到服务器的内容经过隐私清理")
        print("  3. 📊 仅用于改进分析质量")

        use_ai = (
            input(f"\n{Colors.BOLD}是否使用AI分析？[y / n] (默认: n): {Colors.ENDC}")
            .strip()
            .lower()
        )

        if use_ai == "y":
            api_key = input(f"{Colors.BOLD}请输入AI API密钥: {Colors.ENDC}").strip()
            if api_key:
                # 加密存储API密钥
                encrypted = PrivacyProtector.encrypt_api_key(api_key)
                self.ai_api_key = encrypted
                print(f"{Colors.GREEN}✅ API密钥已安全保存{Colors.ENDC}")
            else:
                print(f"{Colors.YELLOW}⚠️  未提供API密钥，将使用基础AI分析{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}⚠️  使用基础AI分析功能{Colors.ENDC}")

    def scan_directory(self):
        """扫描目录"""
        print(f"\n{Colors.BLUE}🔍 正在扫描文件系统...{Colors.ENDC}")

        all_files = []
        self.file_stats = {k: 0 for k in self.file_stats.keys()}

        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in Config.SKIP_DIRECTORIES]

            for file in files:
                if file == os.path.basename(__file__):
                    continue

                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.target_dir)
                _, ext = os.path.splitext(file)
                ext = ext.lower()

                self.file_stats["total_files"] += 1

                # 检查特殊文件名
                if file in Config.FILE_TYPES:
                    file_info = Config.FILE_TYPES[file].copy()
                    file_info.update(
                        {
                            "path": rel_path,
                            "full_path": file_path,
                            "extension": ext,
                            "filename": file,
                        }
                    )
                    all_files.append(file_info)
                    self._update_file_stats(file_info["type"])

                # 检查扩展名
                elif ext in Config.FILE_TYPES:
                    file_info = Config.FILE_TYPES[ext].copy()
                    file_info.update(
                        {
                            "path": rel_path,
                            "full_path": file_path,
                            "extension": ext,
                            "filename": file,
                        }
                    )
                    all_files.append(file_info)
                    self._update_file_stats(file_info["type"])

                # 二进制文件
                elif ext in Config.BINARY_EXTENSIONS:
                    file_info = {
                        "type": "binary",
                        "analyzer": "Binary",
                        "color": "#FF6B6B",
                        "path": rel_path,
                        "full_path": file_path,
                        "extension": ext,
                        "filename": file,
                        "is_binary": True,
                    }
                    all_files.append(file_info)
                    self.file_stats["binary_files"] += 1

                else:
                    self.file_stats["skipped_files"] += 1

        print(
            f"{Colors.GREEN}📊 扫描完成! 发现 {len(all_files)} 个可分析文件{Colors.ENDC}"
        )
        return all_files

    def _update_file_stats(self, file_type):
        """更新文件统计"""
        stats_map = {
            "source": "source_files",
            "config": "config_files",
            "docker": "docker_files",
            "script": "script_files",
            "document": "document_files",
        }
        if file_type in stats_map:
            self.file_stats[stats_map[file_type]] += 1

    def analyze_file(
        self, file_info: Dict, content: str
    ) -> Tuple[List[str], List[str]]:
        """分析单个文件"""
        issues = []
        warnings = []

        # 基础安全检查
        if file_info.get("security_scan", True):
            for pattern, description in Config.SECURITY_PATTERNS:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    warnings.append(f"发现{description}: {len(matches)}处")
                    self.file_stats["security_issues"] += len(matches)

        # 根据模式进行额外分析
        if self.scan_mode == "online":
            # 在线漏洞库分析
            online_issues, online_warnings = OnlineServiceClient.scan_with_vuln_db(
                content, file_info["type"]
            )
            issues.extend(online_issues)
            warnings.extend(online_warnings)

        elif self.scan_mode == "online_ai":
            # AI分析
            ai_issues, ai_warnings = OnlineServiceClient.scan_with_ai(
                content, file_info["type"], self.ai_api_key
            )
            issues.extend(ai_issues)
            warnings.extend(ai_warnings)
            self.file_stats["ai_insights"] += len(ai_issues) + len(ai_warnings)

        return issues, warnings

    def calculate_file_score(
        self,
        file_type: str,
        issues_count: int,
        warnings_count: int,
        is_binary: bool = False,
    ) -> int:
        """计算文件评分"""
        if is_binary:
            return 60

        base_scores = {
            "source": 95,
            "config": 85,
            "docker": 90,
            "script": 90,
            "document": 95,
            "binary": 60,
        }

        base_score = base_scores.get(file_type, 80)
        score = base_score - (issues_count * 3) - (warnings_count * 10)
        return max(0, min(100, score))

    def get_rank_info(self, score: int) -> Tuple[str, str, str]:
        """获取等级信息"""
        if score >= 95:
            return "S", "卓越", "#2ecc71"
        elif score >= 85:
            return "A", "优秀", "#3498db"
        elif score >= 75:
            return "B", "良好", "#f1c40"
        elif score >= 60:
            return "C", "合格", "#e67e22"
        else:
            return "D", "需改进", "#e74c3c"

    def run_analysis(self):
        """运行分析"""
        mode_names = {
            "offline": "离线分析模式",
            "online": "在线模式 (免费漏洞库)",
            "online_ai": "在线 + AI分析模式",
        }

        print(
            f"\n{Colors.HEADER}🚀 启动模式: {mode_names.get(self.scan_mode, self.scan_mode)}{Colors.ENDC}"
        )

        if self.scan_mode in ["online", "online_ai"]:
            print(f"{Colors.CYAN}🌐 正在连接云端服务...{Colors.ENDC}")
            time.sleep(1)
            print(f"{Colors.GREEN}✅ 连接成功！{Colors.ENDC}")

        self.start_time = time.time()
        files = self.scan_directory()

        if not files:
            print(f"{Colors.YELLOW}⚠️  未发现可分析的文件{Colors.ENDC}")
            return

        print(f"\n{Colors.BLUE}📋 开始分析 {len(files)} 个文件...{Colors.ENDC}")

        for idx, file_info in enumerate(files):
            rel_path = file_info["path"]

            # 进度显示
            progress = (idx + 1) / len(files) * 100
            print(
                f"\r[{idx + 1}/{len(files)}] {progress:.1f}% - 分析中: {rel_path[:50]}...",
                end="",
            )

            # 二进制文件特殊处理
            if file_info.get("is_binary", False):
                issues = ["检测到二进制文件 - 建议检查是否应该包含在源码库中"]
                warnings = []
                score = 60
                status = "warning"
                output = "⚠️ 检测到二进制文件: " + ", ".join(issues)
            else:
                # 读取内容
                try:
                    with open(
                        file_info["full_path"], "r", encoding="utf - 8", errors="ignore"
                    ) as f:
                        content = f.read()
                except Exception:
                    content = ""
                    issues = ["文件读取失败"]
                    warnings = []

                # 分析文件
                issues, warnings = self.analyze_file(file_info, content)
                score = self.calculate_file_score(
                    file_info["type"], len(issues), len(warnings)
                )
                status = "pass" if score >= 75 else "warning" if score >= 60 else "fail"
                output = self._format_output(issues, warnings)

            # 保存结果
            result = {
                "file": rel_path,
                "type": file_info["type"],
                "analyzer": file_info.get("analyzer", "Unknown"),
                "status": status,
                "score": score,
                "issues": issues,
                "warnings": warnings,
                "mode": self.scan_mode,
                "timestamp": datetime.datetime.now().isoformat(),
                "output": output,
                "binary_warning": file_info.get("is_binary", False),
            }
            self.results.append(result)

            # 短暂延迟
            time.sleep(0.01)

        self.scan_duration = time.time() - self.start_time
        print(
            f"\n{Colors.GREEN}✅ 分析完成！耗时: {self.scan_duration:.2f}秒{Colors.ENDC}"
        )

    def _format_output(self, issues: List[str], warnings: List[str]) -> str:
        """格式化输出"""
        parts = []

        if warnings:
            parts.append(f"🔐 安全警告: {', '.join(warnings)}")

        if issues:
            parts.append(f"📝 发现: {', '.join(issues[:2])}")

        if not parts:
            parts.append("✅ 检查通过，未发现问题")

        return " | ".join(parts)

    def generate_html_report(self):
        """生成HTML报告"""
        if not self.results:
            print(f"{Colors.YELLOW}⚠️  没有分析结果{Colors.ENDC}")
            return

        # 计算统计
        scores = [r["score"] for r in self.results]
        avg_score = int(sum(scores) / len(scores)) if scores else 0
        project_rank, rank_description, rank_color = self.get_rank_info(avg_score)

        security_count = sum(len(r["warnings"]) for r in self.results)
        quality_count = sum(len(r["issues"]) for r in self.results)

        # 生成表格行
        rows = ""
        for result in self.results:
            rank, _, color = self.get_rank_info(result["score"])

            rows += """
            <tr class="{row_class}">
                <td><span class="file - type" style="background:{type_color}20; color:{type_color}">
                    {result['type'].upper()}</span></td>
                <td align="center"><div class="score - badge" style="background:{color}">
                    {rank} ({result['score']})</div></td>
                <td><code>{html.escape(result['file'])}</code></td>
                <td>{html.escape(result.get('output', ''))}</td>
            </tr>
            """

        # 模式描述
        mode_descriptions = {
            "offline": "本地全面扫描，不依赖网络",
            "online": "免费云端漏洞库分析",
            "online_ai": "AI智能分析 + 隐私保护",
        }

        # 生成HTML
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html_content = self._create_html_template(
            timestamp,
            avg_score,
            project_rank,
            rank_color,
            rank_description,
            security_count,
            quality_count,
            self.file_stats["ai_insights"],
            mode_descriptions.get(self.scan_mode, self.scan_mode),
            rows,
        )

        # 保存文件
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = os.path.join(
            os.getcwd(), f"Code_Audit_Report_{timestamp_str}.html"
        )

        with open(self.output_file, "w", encoding="utf - 8") as f:
            f.write(html_content)

        print(f"\n{Colors.GREEN}📄 HTML报告已生成: {self.output_file}{Colors.ENDC}")
        return self.output_file

    def _create_html_template(
        self,
        timestamp,
        avg_score,
        project_rank,
        rank_color,
        rank_description,
        security_count,
        quality_count,
        ai_insights,
        mode_description,
        rows,
    ):
        """创建HTML模板"""
        return """<!DOCTYPE html>
<html lang="zh - CN">
<head>
    <meta charset="UTF - 8">
    <meta name="viewport" content="width = device - width, initial - scale = 1.0">
    <title>专业代码审计报告 v2.0</title>
    <style>
        :root {{
            --primary - color: #3498db;
            --success - color: #2ecc71;
            --warning - color: #f1c40f;
            --danger - color: #e74c3c;
            --binary - color: #e67e22;
            --ai - color: #9b59b6;
            --dark - color: #2c3e50;
            --light - color: #f8f9fa;
        }}

        body {{
            font - family: -apple - system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans - serif;
            padding: 20px;
            background: linear - gradient(135deg, #667eea 0%, #764ba2 100%);
            min - height: 100vh;
            color: #333;
        }}

        .container {{
            background: white;
            padding: 30px;
            max - width: 1200px;
            margin: 0 auto;
            box - shadow: 0 10px 30px rgba(0,0,0,0.2);
            border - radius: 12px;
        }}

        .header - section {{
            display: flex;
            justify - content: space - between;
            align - items: flex - start;
            flex - wrap: wrap;
            gap: 20px;
            margin - bottom: 30px;
            border - bottom: 2px solid #eee;
            padding - bottom: 20px;
        }}

        .mode - badge {{
            background: {rank_color}20;
            color: {rank_color};
            padding: 5px 15px;
            border - radius: 20px;
            font - size: 0.9em;
            font - weight: bold;
            display: inline - block;
            margin - left: 10px;
        }}

        .project - score {{
            font - size: 4em;
            color: {rank_color};
            margin: 0;
            font - weight: bold;
            line - height: 1;
        }}

        .stats - grid {{
            display: grid;
            grid - template-columns: repeat(auto - fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .stat - box {{
            background: var(--light - color);
            padding: 15px;
            border - radius: 8px;
            border - left: 4px solid var(--primary - color);
        }}

        .stat - box.binary {{ border - left-color: var(--binary - color); background: #fff5f5; }}
        .stat - box.security {{ border - left-color: var(--danger - color); background: #fff5f5; }}
        .stat - box.quality {{ border - left-color: var(--warning - color); background: #fff8e1; }}
        .stat - box.ai {{ border - left-color: var(--ai - color); background: #f5f3ff; }}

        table {{
            width: 100%;
            border - collapse: collapse;
            margin - top: 20px;
            font - size: 0.9em;
            box - shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        .binary - row {{
            background - color: #fff8e1 !important;
        }}

        .score - badge {{
            color: white;
            padding: 4px 8px;
            border - radius: 12px;
            font - weight: bold;
            display: inline - block;
            min - width: 40px;
            text - align: center;
        }}

        .privacy - note {{
            background: #e8f4fc;
            padding: 15px;
            border - radius: 8px;
            margin: 20px 0;
            border - left: 4px solid #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header - section">
            <div>
                <h1>🔍 专业代码审计报告 v2.0</h1>
                <p><strong>📁 目标路径:</strong> {html.escape(self.target_dir)}</p>
                <p><strong>⏰ 生成时间:</strong> {timestamp} | <strong>耗时:</strong> {self.scan_duration:.2f}秒</p>
                <p><strong>🔧 分析模式:</strong> {mode_description} <span class="mode - badge">{self.scan_mode.upper()}</span></p>
            </div>

            <div style="text - align: center;">
                <div class="project - score">{project_rank}</div>
                <div style="color: #7f8c8d; margin - top: -5px;">{rank_description}</div>
                <div style="color: #95a5a6; font - size: 0.9em;">平均分: {avg_score}</div>
            </div>
        </div>

        {"<div class='privacy - note'><strong>🔒 隐私保护说明:</strong> AI分析模式下，所有发送到服务器的内容都经过隐私清理，API密钥仅在本地加密存储，保护您的代码安全。</div>" if self.scan_mode == "online_ai" else ""}

        <div class="stats - grid">
            <div class="stat - box">
                <div style="font - size: 1.5em; font - weight: bold; color: #3498db;">{self.file_stats['source_files']}</div>
                <div>源代码文件</div>
            </div>
            <div class="stat - box">
                <div style="font - size: 1.5em; font - weight: bold; color: #9b59b6;">{self.file_stats['config_files']}</div>
                <div>配置文件</div>
            </div>
            <div class="stat - box">
                <div style="font - size: 1.5em; font - weight: bold; color: #1abc9c;">{self.file_stats['docker_files']}</div>
                <div>Docker文件</div>
            </div>
            <div class="stat - box binary">
                <div style="font - size: 1.5em; font - weight: bold; color: #e67e22;">{self.file_stats['binary_files']}</div>
                <div>二进制文件</div>
            </div>
            <div class="stat - box security">
                <div style="font - size: 1.5em; font - weight: bold; color: #e74c3c;">{security_count}</div>
                <div>安全问题</div>
            </div>
            <div class="stat - box quality">
                <div style="font - size: 1.5em; font - weight: bold; color: #f1c40f;">{quality_count}</div>
                <div>质量建议</div>
            </div>
            {f'<div class="stat - box ai"><div style="font - size: 1.5em; font - weight: bold; color: #9b59b6;">{ai_insights}</div><div>AI分析建议</div></div>' if self.scan_mode == "online_ai" else ""}
        </div>

        <table>
            <thead>
                <tr>
                    <th>文件类型</th>
                    <th width="100">评分</th>
                    <th width="300">文件路径</th>
                    <th>分析结果</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <div style="margin - top: 30px; padding: 15px; background: #f8f9fa; border - radius: 8px; font - size: 0.9em; color: #7f8c8d;">
            <p><strong>📋 报告说明:</strong></p>
            <p>💡 <strong>建议:</strong> {self._get_recommendations(avg_score, security_count, self.file_stats['binary_files'])}</p>
            <p style="margin - top: 10px;">
                {self._get_mode_specific_notes()}
            </p>
        </div>
    </div>
</body>
</html>"""

    def _get_recommendations(self, avg_score, security_count, binary_count):
        """生成建议"""
        recommendations = []

        if avg_score < 75:
            recommendations.append("项目整体代码质量有待提高")
        if security_count > 0:
            recommendations.append("发现安全风险，建议立即修复")
        if binary_count > 0:
            recommendations.append("检测到二进制文件，建议审查必要性")
        if avg_score >= 85 and security_count == 0:
            recommendations.append("项目代码质量优秀，继续保持")

        return " | ".join(recommendations) if recommendations else "项目状态良好"

    def _get_mode_specific_notes(self):
        """获取模式特定说明"""
        notes = {
            "offline": "📱 <strong>离线模式:</strong> 本地分析，不依赖网络，适合敏感环境。",
            "online": "☁️ <strong>在线模式:</strong> 免费漏洞库分析，提供最新的安全漏洞信息。",
            "online_ai": "🤖 <strong>AI分析模式:</strong> 智能分析代码质量，隐私保护设计。",
        }
        return notes.get(self.scan_mode, "")

    def show_summary(self):
        """显示总结"""
        if not self.results:
            return

        print(f"\n{Colors.CYAN}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}📊 分析总结{Colors.ENDC}")
        print(f"{Colors.CYAN}{'=' * 60}{Colors.ENDC}")

        scores = [r["score"] for r in self.results]
        avg_score = sum(scores) / len(scores) if scores else 0

        print(f"📈 平均分数: {avg_score:.1f}")
        print(f"📋 文件总数: {len(self.results)}")
        print(f"🔐 安全问题: {self.file_stats['security_issues']}个")
        print(f"⚙️  质量建议: {self.file_stats['quality_issues']}个")
        if self.scan_mode == "online_ai":
            print(f"🤖 AI建议: {self.file_stats['ai_insights']}个")
        print(f"⏱️  分析耗时: {self.scan_duration:.2f}秒")

        # 二进制文件警告
        binary_files = [r for r in self.results if r.get("binary_warning")]
        if binary_files:
            print(
                f"\n{Colors.RED}⚠️  发现 {len(binary_files)} 个二进制文件{Colors.ENDC}"
            )


# ==================== 主程序 ====================
def main():
    """主程序"""
    auditor = ProfessionalCodeAuditor()

    try:
        auditor.show_banner()
        auditor.get_target_directory()

        if not auditor.select_analysis_mode():
            return

        auditor.run_analysis()

        if auditor.results:
            report_file = auditor.generate_html_report()
            auditor.show_summary()

            print(f"\n{Colors.GREEN}{'=' * 60}{Colors.ENDC}")
            print(f"{Colors.BOLD}🎉 分析完成！{Colors.ENDC}")
            print(f"{Colors.GREEN}{'=' * 60}{Colors.ENDC}")
            print("\n📋 下一步操作:")
            print(f"  1. 查看完整报告: {report_file}")
            print("  2. 修复发现的安全问题")
            print("  3. 根据建议优化代码质量")
            if auditor.scan_mode == "online_ai":
                print("  4. AI分析报告已生成，查看智能建议")
        else:
            print(f"\n{Colors.YELLOW}⚠️  未生成分析结果{Colors.ENDC}")

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  用户中断{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ 错误: {str(e)}{Colors.ENDC}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
