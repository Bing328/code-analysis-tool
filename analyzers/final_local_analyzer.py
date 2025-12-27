#!/usr / bin/env python3
import os
import glob
import ast
from pathlib import Path


def detect_language(file_path):
    """检测编程语言"""
    ext_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JSX",
        ".ts": "TypeScript",
        ".tsx": "TSX",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".html": "HTML",
        ".css": "CSS",
        ".php": "PHP",
        ".rb": "Ruby",
        ".go": "Go",
        ".rs": "Rust",
        ".sql": "SQL",
        ".sh": "Shell",
    }
    ext = Path(file_path).suffix.lower()
    return ext_map.get(ext, "Unknown")


def analyze_python_code(content):
    """分析Python代码"""
    analysis = []
    try:
        tree = ast.parse(content)

        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]

        analysis.append(f"  函数数量: {len(functions)}")
        analysis.append(f"  类数量: {len(classes)}")
        analysis.append(f"  导入数量: {len(imports)}")

        if functions:
            analysis.append("  主要函数:")
            for func in functions[:3]:
                analysis.append(f"    - {func.name}")

        if classes:
            analysis.append("  类:")
            for cls in classes[:3]:
                analysis.append(f"    - {cls.name}")

    except SyntaxError as e:
        analysis.append(f"  ⚠️ 语法错误: {e}")

    return analysis


def analyze_javascript_code(content):
    """分析JavaScript代码"""
    analysis = []
    analysis.append(f"  函数定义: {content.count('function ')} 处")
    analysis.append(f"  箭头函数: {content.count('=>')} 处")
    analysis.append(f"  Class定义: {content.count('class ')} 处")
    return analysis


def analyze_general_code(content):
    """通用代码分析"""
    analysis = []
    lines = content.splitlines()

    # 基础统计
    analysis.append(f"  行数: {len(lines)}")
    analysis.append(f"  非空行: {len([line_length for line_length in lines if line_length.strip()])}")
    analysis.append(f"  字符数: {len(content)}")

    return analysis


def analyze_file_detail(file_path):
    """详细分析单个文件"""
    try:
        with open(file_path, "r", encoding="utf - 8") as f:
            content = f.read()

        analysis = []
        file_size = os.path.getsize(file_path)
        language = detect_language(file_path)

        # 基础信息
        analysis.append(f"📄 文件: {file_path}")
        analysis.append(f"  语言: {language}")
        analysis.append(f"  大小: {file_size} bytes")

        # 基础统计
        lines_stats = analyze_general_code(content)
        analysis.extend(lines_stats)

        # 语言特定分析
        if file_path.endswith(".py"):
            python_analysis = analyze_python_code(content)
            analysis.append("🐍 Python分析:")
            analysis.extend(python_analysis)
        elif file_path.endswith((".js", ".jsx")):
            js_analysis = analyze_javascript_code(content)
            analysis.append("📜 JavaScript分析:")
            analysis.extend(js_analysis)
        else:
            analysis.append("🔍 通用代码分析")

        return "\n".join(analysis)

    except Exception as e:
        return f"📄 文件: {file_path}\n  ❌ 分析错误: {e}"


def find_all_code_files(directory="."):
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
        "**/*.sql",
        "**/*.sh",
        "**/*.bash",
    ]

    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, recursive=True))

    # 去重并排序
    files = list(set(files))
    files.sort()

    return files


def main():
    print("=== 最终版代码分析器 ===")
    print("🎯 无需API，本地深度分析")
    print("=" * 50)

    # 查找文件
    code_files = find_all_code_files()

    if not code_files:
        print("❌ 未找到代码文件")
        print("当前目录内容:")
        for item in Path(".").iterdir():
            if item.is_dir():
                print(f"📁 {item}/")
            else:
                print(f"📄 {item}")
        return

    print(f"✅ 找到 {len(code_files)} 个代码文件")

    # 显示文件列表
    print("\n📋 文件列表:")
    for i, file_path in enumerate(code_files, 1):
        print(f"  {i:2d}. {file_path}")

    # 选择分析方式
    print("\n🎮 选择分析方式:")
    print("  1. 分析所有文件")
    print("  2. 分析单个文件")
    print("  3. 快速统计")

    choice = input("请输入选择 (1 / 2/3): ").strip()

    if choice == "1":
        # 分析所有文件
        print(f"\n📊 开始分析 {len(code_files)} 个文件...")
        print("=" * 60)

        for file_path in code_files:
            result = analyze_file_detail(file_path)
            print(result)
            print("-" * 40)

    elif choice == "2":
        # 分析单个文件
        try:
            file_num = input("请输入文件编号: ").strip()
            file_num = int(file_num) - 1

            if 0 <= file_num < len(code_files):
                file_path = code_files[file_num]
                print(f"\n🔍 详细分析: {file_path}")
                print("=" * 50)

                result = analyze_file_detail(file_path)
                print(result)
            else:
                print("❌ 无效的文件编号")
        except ValueError:
            print("❌ 请输入有效的数字")

    elif choice == "3":
        # 快速统计
        print("\n📈 快速统计报告")
        print("=" * 40)

        total_lines = 0
        total_size = 0
        language_count = {}

        for file_path in code_files:
            try:
                with open(file_path, "r", encoding="utf - 8") as f:
                    content = f.read()

                lines = len(content.splitlines())
                size = os.path.getsize(file_path)
                language = detect_language(file_path)

                total_lines += lines
                total_size += size
                language_count[language] = language_count.get(language, 0) + 1

            except Exception:
                continue

        print(f"📁 文件总数: {len(code_files)}")
        print(f"📏 总行数: {total_lines}")
        print(f"💾 总大小: {total_size} bytes")
        print(f"📊 平均大小: {total_size // len(code_files) if code_files else 0} bytes")

        print("\n🌐 语言分布:")
        for lang, count in sorted(language_count.items()):
            print(f"  {lang}: {count} 个文件")

    else:
        print("❌ 无效的选择")


if __name__ == "__main__":
    main()
