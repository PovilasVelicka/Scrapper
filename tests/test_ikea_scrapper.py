import os
import sys

# Предположим, ты запускаешь этот скрипт где-то внутри проекта Scrapper
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # или '../..' если глубже
sys.path.append(project_root)

print(project_root)
# # vaa
# res = scrapper.BeautifulSoup
# assert res == 0
