import re
import os 
import glob
import shutil

# 该脚本功能：清理 Typora markdown笔记中未被引用的图片
# 1.递归遍历目录中的所有md文档，获取md文档中被引用的图片地址
# 2.获取md文档所在目录下的assets文件夹中所有图片地址
# 3.比较两者，将未被引用的图片移动到根目录的 未引用/{md文档名称}_assets
# 4.若被引用的图片地址不存在，则打印文档名称和图片地址，提示用户检查图片地址是否正确

# md文档所在目录
ROOT_DIR = os.path.normpath(".")

# 忽略的md文档名称
IGNORED_MD_LIST = []

# 存储图片的文件夹名称
ASSETS_NAME = "assets"
 
# 定义一个正则表达式，匹配md文档中被引用的图片地址
# 这个很重要，尽可能地匹配到所有typora的图片引用，否则匹配不全将导致很多图片误判为未被引用，导致误删或误移动
pattern = r'\!\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)' # 形如 ![alt text](path) 或 ![alt text](path "title")
pattern2 = r'<img\s+[^>]*src=["\']([^"\']*)["\'][^>]*/?>' # 形如 <img src="path">

# 存储图片地址的提醒
warn_total_list = []

# 遍历目录下的所有md文档
for md_path in glob.glob(os.path.join(ROOT_DIR, "**", "*.md"), recursive=True):
    # print("正在处理md文档：" + md_path)
    md_dir = os.path.dirname(md_path)
    md_name = os.path.basename(md_path)
    if (md_name in IGNORED_MD_LIST):
        continue
    # 相关容器
    img_set = set()
    img_dict = {}
    asset_set = set()
    text=""
    warn_list=[]
    # 获取存储这个md文档图片文件夹下所有图片名称
    img_suffix = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg')
    assets_dir = os.path.join(md_dir, ASSETS_NAME)
    for asset_path in glob.glob(os.path.join(assets_dir, '*')):
        if asset_path.lower().endswith(img_suffix):
            # print(asset_path)
            format_asset_path = os.path.join(ASSETS_NAME, os.path.basename(asset_path))
            # print(format_asset_path)
            asset_set.add(format_asset_path)
	# 读取文件 匹配获取图片引用
    with open(md_path,"r",encoding="utf-8") as f:
        text+=f.read()
    for matche in re.findall(pattern, text) + re.findall(pattern2, text):
        # print(matche)
        if not matche:
            warn_list.append("空的图片地址,"+ matche)
            continue
        if "http" in matche:
            warn_list.append("网络图片,"+ matche)
            continue
        if ":" in matche:
            warn_list.append("使用了绝对路径,"+ matche)
            continue
        if "\\/" in matche or "/\\" in matche:
            warn_list.append("格式不规范的图片地址,"+ matche)
            continue
        format_img = os.path.normpath(matche)
        # print(format_img)
        img_set.add(format_img)
        img_dict[format_img] = matche

    # 对比筛选出 被引用的图片 和 可能无效的图片地址
    for abandon_asset in (asset_set-img_set):
        old_asset = os.path.join(md_dir, abandon_asset)
        new_asset = os.path.join(ROOT_DIR, "未被引用的图片", md_name.split('.')[0] + "_" + abandon_asset)
        new_dir = os.path.dirname(new_asset)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        shutil.move(old_asset, new_asset)
        warn_list.append("未被引用的图片," + old_asset + "\n移动至," + new_asset)
    for non_img in (img_set-asset_set):
        warn_list.append("无效的图片地址,"+ img_dict[non_img])
    if warn_list:
        warn_total_list.append(f"------------------------ {md_path} ------------------------")
        for warn in warn_list:
            warn_total_list.append(warn)

        
# 打印提醒 可能无效的图片地址
for warn in warn_total_list:
    print(warn)
