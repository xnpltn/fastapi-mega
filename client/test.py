import os
from dotenv import load_dotenv
load_dotenv("../app/variables/.env")

name  = os.getenv("NAME")
age = os.getenv("AGE")

print(name)
print(age)