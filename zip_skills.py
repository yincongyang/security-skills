import os
import zipfile

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(base_dir, 'skills')
    
    if not os.path.exists(skills_dir):
        print("找不到 skills 目录")
        return

    # 遍历 skills 目录下的每个 skill
    for skill_name in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, skill_name)
        
        # 只处理目录
        if os.path.isdir(skill_path):
            zip_name = f"{skill_name}.zip"
            zip_path = os.path.join(base_dir, zip_name)
            
            print(f"正在生成 {zip_name} ...")
            
            # 创建 zip 文件
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(skill_path):
                    for file in files:
                        # 忽略不必要的文件
                        if file == '.DS_Store' or file.endswith('.pyc') or '__pycache__' in root:
                            continue
                        
                        file_path = os.path.join(root, file)
                        # 计算相对于 skills_dir 的路径，以保证压缩包内不再包含 'skills/' 目录
                        arcname = os.path.relpath(file_path, skills_dir)
                        zf.write(file_path, arcname)
                        
            print(f"✅ {zip_name} 生成完毕")

if __name__ == '__main__':
    main()