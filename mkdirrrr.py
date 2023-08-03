import os

# 清理文件夹名称中的非法字符
def clean_folder_name(name):
    invalid_chars = r'<>:"/\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    return name.strip()

# 递归创建文件夹结构
def create_folders_recursive(folder_dict, parent_path="", level_numbers=None):
    if level_numbers is None:
        level_numbers = []

    # 遍历当前层级的文件夹
    for i, (folder_name, subfolders) in enumerate(folder_dict.items(), start=1):
        current_level_number = str(i)
        if len(level_numbers) > 0:
            current_level_number = '-'.join(level_numbers + [current_level_number])
        folder_name = f"{current_level_number} {folder_name}"
        folder_name = clean_folder_name(folder_name)
        folder_path = os.path.join(parent_path, folder_name)
        
        # 创建文件夹并输出提示信息
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        
        # 继续处理下一级子文件夹
        if subfolders:
            create_folders_recursive(subfolders, folder_path, level_numbers + [str(i)])

# 从文本文件读取内容并生成文件夹结构
def read_folder_structure_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        folder_structure = {}
        stack = [(0, folder_structure)]
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(maxsplit=1)
                if len(parts) < 2:
                    continue
                try:
                    level = len(parts[0].split('-'))
                    name = parts[1].strip()
                except ValueError:
                    continue

                # 根据层级关系构建文件夹结构
                while len(stack) > 1 and level <= stack[-1][0]:
                    stack.pop()
                parent_level, parent_folder = stack[-1]
                parent_folder[name] = {}
                stack.append((level, parent_folder[name]))

        return folder_structure

# 主程序
if __name__ == "__main__":
    # 设置根目录和文本文件路径
    root_directory = "C:/Users/tong/Desktop/gg"
    file_path = "C:/Users/tong/Desktop/folder_structure.txt"
    
    # 读取文本文件并生成文件夹结构
    folder_structure = read_folder_structure_from_file(file_path)
    create_folders_recursive(folder_structure, root_directory)


