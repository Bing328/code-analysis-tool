#!/bin/bash
echo "Testing built executables..."

# 测试Linux可执行文件（如果存在）
if [ -f "dist/code-analysis-tool" ]; then
    echo "Testing Linux executable:"
    ./dist/code-analysis-tool --help
    echo "Exit code: $?"
fi

# 测试Windows可执行文件（在WSL中）
if [ -f "dist/code-analysis-tool.exe" ]; then
    echo "Windows executable size:"
    ls -lh dist/code-analysis-tool.exe
fi

echo "Build test completed."
