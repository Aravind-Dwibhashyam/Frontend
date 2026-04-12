import glob
import os

for f in glob.glob("models/*.py"):
    if f.endswith("__init__.py"): continue
    
    with open(f, "r") as file:
        content = file.read()
        
    if "BeforeValidator" not in content:
        content = content.replace(
            "from pydantic import BaseModel, Field", 
            "from pydantic import BaseModel, Field, BeforeValidator\nfrom typing import Annotated"
        )
        content = content.replace(
            'id: str = Field(alias="_id")', 
            'id: Annotated[str, BeforeValidator(str)] | None = Field(alias="_id", default=None)'
        )
        
        # Some models use Optional, so let's import it if not present, but using `| None` works in modern python
        
        with open(f, "w") as file:
            file.write(content)
            
print("Models fixed!")
