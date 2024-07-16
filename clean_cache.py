import shutil
from pathlib import Path

def remove_pycache():
    current_dir = Path('.')
    pycache_dirs = current_dir.rglob('__pycache__')
    
    for dir in pycache_dirs:
        shutil.rmtree(dir)
        print(f"삭제됨: {dir}")

if __name__ == "__main__":
    remove_pycache()
    print("모든 __pycache__ 폴더가 삭제되었습니다.")