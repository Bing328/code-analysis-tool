#!/usr/bin/env python3
"""
增强版代码分析器 - 基于 final_local_analyzer.py 优化
支持更多功能和更好的错误处理
"""

import os
import glob
import ast
import re
from pathlib import Path
from collections import defaultdict


def detect_language(file_path):
    """增强的语言检测"""
    ext = Path(file_path).suffix.lower()
    language_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript (JSX)",
        ".ts": "TypeScript",
        ".tsx": "TypeScript (TSX)",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".h": "C/C++ Header",
        ".html": "HTML",
        ".css": "CSS",
        ".php": "PHP",
        ".rb": "Ruby",
        ".go": "Go",
        ".rs": "Rust",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".scala": "Scala",
    }
    return language_map.get(ext, "Unknown")


def analyze_python_code(file_path, content):
    """增强的Python代码分析"""
    analysis = {
        "functions": [],
        "classes": [],
        "imports": [],
        "decorators": [],
        "docstrings": 0,
        "error": None,
    }

    try:
        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "lineno": node.lineno,
                    "args": len(node.args.args),
                    "decorators": len(node.decorator_list),
                }
                analysis["functions"].append(func_info)

            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "lineno": node.lineno,
                    "methods": len(
                        [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    ),
                }
                analysis["classes"].append(class_info)

            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                import_info = {
                    "module": getattr(node, "module", ""),
                    "names": [alias.name for alias in node.names],
                }
                analysis["imports"].append(import_info)

            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                analysis["docstrings"] += 1

    except SyntaxError as e:
        analysis["error"] = f"语法错误: {e}"
    except Exception as e:
        analysis["error"] = f"分析错误: {e}"

    return analysis


def analyze_javascript_code(file_path, content):
    """JavaScript代码分析"""
    analysis = {
        "functions": [],
        "classes": [],
        "arrow_functions": 0,
        "imports": 0,
        "exports": 0,
    }

    # 简单的正则匹配（实际项目中应使用专业解析器）
    analysis["functions"] = re.findall(r"function\s+(\w+)\s*\(", content)
    analysis["classes"] = re.findall(r"class\s+(\w+)\s*{", content)
    analysis["arrow_functions"] = len(re.findall(r"(\w+)\s*=>\s*{", content))
    analysis["imports"] = len(re.findall(r"import\s+.*from", content))
    analysis["exports"] = len(
        re.findall(r"export\s+(default\s+)?(function|class|const|let)", content)
    )

    return analysis


def get_file_stats(file_path, content):
    """获取文件统计信息"""
    lines = content.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]

    return {
        "size": len(content.encode("utf-8")),
        "lines": len(lines),
        "non_empty": len(non_empty_lines),
        "chars": len(content),
        "encoding": "utf-8",
    }


def analyze_file(file_path):
    """分析单个文件"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        language = detect_language(file_path)
        stats = get_file_stats(file_path, content)

        analysis = {"language": language, "stats": stats}

        # 语言特定分析
        if language == "Python":
            analysis.update(analyze_python_code(file_path, content))
        elif "JavaScript" in language:
            analysis.update(analyze_javascript_code(file_path, content))

        return analysis

    except Exception as e:
        return {"error": str(e), "language": "Unknown"}


def find_code_files(directory="."):
    """查找所有代码文件"""
    patterns = [
        "**/*.py",
        "**/*.js",
        "**/*.jsx",
        "**/*.ts",
        "**/*.tsx",
        "**/*.java",
        "**/*.cpp",
        "**/*.c",
        "**/*.h",
        "**/*.html",
        "**/*.css",
        "**/*.php",
        "**/*.rb",
        "**/*.go",
        "**/*.rs",
        "**/*.swift",
        "**/*.kt",
        "**/*.scala",
    ]

    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, recursive=True))

    # 排除隐藏文件和生成的文件
    files = [
        f
        for f in sorted(set(files))
        if not any(part.startswith(".") for part in Path(f).parts)
        and not any(part.startswith("__") for part in Path(f).parts)
    ]

    return files


def generate_report(files_data):
    """生成详细报告"""
    print(f"=== 代码分析报告 ===")
    print(f"📊 分析文件数量: {len(files_data)}")
    print("=" * 60)

    language_stats = defaultdict(lambda: {"count": 0, "size": 0, "lines": 0})
    total_files = 0
    total_size = 0
    total_lines = 0

    for file_path, analysis in files_data:
        if "error" in analysis:
            print(f"❌ {file_path}")
            print(f"   错误: {analysis['error']}")
        else:
            lang = analysis["language"]
            stats = analysis["stats"]

            language_stats[lang]["count"] += 1
            language_stats[lang]["size"] += stats["size"]
            language_stats[lang]["lines"] += stats["lines"]

            total_files += 1
            total_size += stats["size"]
            total_lines += stats["lines"]

            print(f"📄 {file_path}")
            print(f"  语言: {lang}")
            print(f"  大小: {stats['size']} bytes")
            print(f"  行数: {stats['lines']} (非空: {stats['non_empty']})")

            if lang == "Python" and "error" not in analysis:
                print(f"  🐍 函数: {len(analysis['functions'])}")
                print(f"  🐍 类: {len(analysis['classes'])}")
                print(f"  🐍 导入: {len(analysis['imports'])}")
                if analysis["error"]:
                    print(f"  ⚠️ {analysis['error']}")

            elif "JavaScript" in lang:
                print(f"  📜 函数: {len(analysis['functions'])}")
                print(f"  📜 类: {len(analysis['classes'])}")

            print("-" * 40)

    # 语言统计摘要
    print("\n=== 语言统计摘要 ===")
    for lang, stats in sorted(language_stats.items()):
        print(
            f"  {lang}: {stats['count']} 文件, {stats['lines']} 行, {stats['size']} bytes"
        )

    print(f"\n=== 总体统计 ===")
    print(f"📈 总文件数: {total_files}")
    print(f"📈 总代码行数: {total_lines}")
    print(f"📈 总大小: {total_size} bytes")
    print(
        f"📈 平均文件大小: {total_size // total_files if total_files > 0 else 0} bytes"
    )


def main():
    import sys

    directory = sys.argv[1] if len(sys.argv) > 1 else "."

    if not os.path.exists(directory):
        print(f"❌ 目录不存在: {directory}")
        return

    print("🚀 增强版代码分析器启动...")
    print(f"📂 分析目录: {os.path.abspath(directory)}")

    files = find_code_files(directory)
    if not files:
        print("❌ 未找到代码文件")
        return

    print(f"🔍 找到 {len(files)} 个文件，开始分析...")
    print("=" * 60)

    files_data = []
    for file_path in files:
        analysis = analyze_file(file_path)
        files_data.append((file_path, analysis))

    generate_report(files_data)


if __name__ == "__main__":
    main()
