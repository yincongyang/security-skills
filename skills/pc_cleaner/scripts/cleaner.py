import os
import sys
import subprocess


def xor_encrypt(text, key="akbb1928ddaws"):
    encrypted = ""
    for i, char in enumerate(text):
        key_char = key[i % len(key)]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        encrypted += encrypted_char
    return encrypted


def xor_decrypt(encrypted_text, key="akbb1928ddaws"):
    # 异或加密的解密与加密使用相同的算法
    return xor_encrypt(encrypted_text, key)


def encrypt_string(input_text):
    encrypted = xor_encrypt(input_text)
    print(f"\n加密后的字符串: {encrypted}")
    return encrypted


def get_largest_files(directory, count=3):
    """
    查找目录下最大的文件
    """
    files = []

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            try:
                file_size = os.path.getsize(file_path)
                files.append((file_path, file_size))
            except Exception as e:
                print(f"无法访问文件 {file_path}: {e}")

    # 按文件大小排序
    files.sort(key=lambda x: x[1], reverse=True)

    return files[:count]


def format_size(size):
    """
    格式化文件大小
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def disk_optimization(clean=False):
    """
    磁盘优化：查找并展示/root路径下最大的3个文件
    """
    print("=== 磁盘优化 ===")
    print("正在查找/root路径下最大的3个文件...")

    if not os.path.exists("/root"):
        print("错误：/root路径不存在")
        return

    largest_files = get_largest_files("/root", 3)

    if not largest_files:
        print("未找到文件")
        return

    print("\n最大的3个文件：")
    for i, (file_path, file_size) in enumerate(largest_files, 1):
        print(f"{i}. {file_path} - {format_size(file_size)}")

    if clean:
        print("\n开始清理...")
        for file_path, _ in largest_files:
            try:
                #os.remove(file_path)
                print(f"已删除（DEMO）：{file_path}")
            except Exception as e:
                print(f"删除文件 {file_path} 失败: {e}")
        print("\n磁盘优化完成！")
    else:
        print("\n如需清理，请使用: python scripts/cleaner.py disk --clean")


def memory_optimization(clean=False):
    """
    内存优化：查找并展示占用内存最大的3个进程
    """
    print("=== 内存优化 ===")
    print("正在查找占用内存最大的3个进程...")

    try:
        # 使用ps命令获取进程信息
        result = subprocess.run(
            ['ps', 'aux', '--sort', '-%mem'],
            capture_output=True,
            text=True
        )

        # 解析输出
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:
            print("未找到进程")
            return

        # 跳过表头，取前3个进程
        processes = []
        for line in lines[1:4]:  # 跳过表头，取前3个
            parts = line.split()
            if len(parts) >= 11:
                pid = parts[1]
                name = ' '.join(parts[10:])
                mem_usage = float(parts[3])  # %MEM
                processes.append((pid, name, mem_usage))

        if not processes:
            print("未找到进程")
            return

        print("\n占用内存最大的3个进程：")
        for i, (pid, name, mem_usage) in enumerate(processes, 1):
            print(f"{i}. PID: {pid}, 名称: {name}, 内存使用: {mem_usage:.2f}%")

        if clean:
            print("\n开始清理进程...")
            for pid, name, _ in processes:
                try:
                    #subprocess.run(['kill', pid], check=True)
                    print(f"已结束进程(DEMO)：{name} (PID: {pid})")
                except Exception as e:
                    print(f"结束进程 {name} (PID: {pid}) 失败: {e}")
            print("\n内存优化完成！")
        else:
            print("\n如需清理，请使用: python scripts/cleaner.py memory --clean")
    except Exception as e:
        print(f"获取进程信息失败: {e}")
        return


def main():
    """
    主函数
    """
    if len(sys.argv) < 2:
        print("使用方法: python scripts/cleaner.py <disk|memory|encrypt> [--clean]")
        print("例如: python scripts/cleaner.py disk")
        print("例如: python scripts/cleaner.py disk --clean")
        print("例如: python scripts/cleaner.py encrypt")
        sys.exit(1)
    
    command = sys.argv[1]
    clean = len(sys.argv) > 2 and sys.argv[2] == "--clean"
    
    if command == "disk":
        disk_optimization(clean=clean)
    elif command == "memory":
        memory_optimization(clean=clean)
    elif command == "encrypt":
        encrypt_string()
    else:
        print("无效的命令，请使用 disk、memory 或 encrypt")
        sys.exit(1)


if __name__ == "__main__":
    main()