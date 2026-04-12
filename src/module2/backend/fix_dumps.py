import glob
import os

for f in glob.glob("routes/*.py"):
    with open(f, "r") as file:
        content = file.read()
        
    old_code = ".model_dump()"
    new_code = ".model_dump(mode='json')"
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        with open(f, "w") as file:
            file.write(content)
            
print("Dumps fixed!")
