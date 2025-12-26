#!/bin/bash
# 代码分析项目管理脚本

PROJECT_DIR=$(pwd)

show_help() {
    echo "📁 代码分析项目管理工具"
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  analyze [目录]    - 分析代码目录（默认当前目录）"
    echo "  clean            - 清理有问题的文件"
    echo "  stats            - 显示项目统计"
    echo "  test             - 运行测试"
    echo "  help             - 显示此帮助"
}

analyze_code() {
    local dir="${1:-.}"
    echo "🔍 分析目录: $dir"
    
    if [ -f "enhanced_analyzer.py" ]; then
        python3 enhanced_analyzer.py "$dir"
    elif [ -f "final_local_analyzer.py" ]; then
        python3 final_local_analyzer.py "$dir"
    else
        echo "❌ 找不到可用的分析器"
    fi
}

clean_project() {
    echo "🧹 清理项目..."
    
    # 创建备份目录
    mkdir -p backup/problematic
    
    # 移动有语法错误的文件
    for file in *.py; do
        if [ -f "$file" ] && ! python3 -m py_compile "$file" 2>/dev/null; then
            echo "移动有问题的文件: $file"
            mv "$file" backup/problematic/
        fi
    done
    
    # 保留关键文件
    important_files=("final_local_analyzer.py" "enhanced_analyzer.py" "manage_project.sh")
    for file in "${important_files[@]}"; do
        if [ -f "$file" ]; then
            cp "$file" backup/
        fi
    done
    
    echo "✅ 清理完成"
}

show_stats() {
    echo "📊 项目统计:"
    echo "  文件总数: $(find . -name "*.py" -o -name "*.md" -o -name "*.sh" | wc -l)"
    echo "  Python文件: $(find . -name "*.py" | wc -l)"
    echo "  文档文件: $(find . -name "*.md" | wc -l)"
    echo "  脚本文件: $(find . -name "*.sh" | wc -l)"
    
    echo -e "\n✅ 可用的分析器:"
    for file in *.py; do
        if python3 -m py_compile "$file" 2>/dev/null; then
            size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file")
            lines=$(wc -l < "$file")
            echo "  ✓ $file ($lines 行, $size bytes)"
        fi
    done
}

run_tests() {
    echo "🧪 运行测试..."
    
    # 测试语法
    echo "1. 语法检查:"
    for file in *.py; do
        if python3 -m py_compile "$file" 2>/dev/null; then
            echo "  ✅ $file"
        else
            echo "  ❌ $file"
        fi
    done
    
    # 测试分析器功能
    echo -e "\n2. 功能测试:"
    if [ -f "enhanced_analyzer.py" ]; then
        python3 enhanced_analyzer.py . --quick-test 2>/dev/null && echo "  ✅ enhanced_analyzer.py" || echo "  ❌ enhanced_analyzer.py"
    fi
}

case "${1:-help}" in
    "analyze")
        analyze_code "$2"
        ;;
    "clean")
        clean_project
        ;;
    "stats")
        show_stats
        ;;
    "test")
        run_tests
        ;;
    "help"|*)
        show_help
        ;;
esac
