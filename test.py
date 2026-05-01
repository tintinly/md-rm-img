import re
import os 

# pattern = r'\!\[.*]\((.*)\)' 
pattern = r'\!\[[^\]]*\]\(([^)]*)\)'
pattern2 = r'<img\s+[^>]*src=["\']([^"\']*)["\'][^>]*/>'

for matche in re.findall(pattern, '![image-20220418121435746](assets/image-20220418121435746.png)![image-20220418121507799](assets/image-20220418121507799.png)'):
    print(matche)

print(os.path.normpath("./\\assets\/logo.png"))