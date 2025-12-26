import os
import glob
import shutil

def perform_cleanup():
    targets = {
        "报告文件": "Code_Audit_Report_*.html",
        "Python缓存": "**/__pycache__",
        "字节码": "**/*.pyc"
    }
    
    print("🚀 开始自动化清理...")
    
    for label, pattern in targets.items():
        files = glob.glob(pattern, recursive=True)
        for f in files:
            try:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.remove(f)
                print(f"  [已移除] {label}: {os.path.basename(f)}")
            except Exception as e:
                print(f"  [失败] 无法移除 {f}: {e}")

if __name__ == "__main__":
    perform_cleanup()