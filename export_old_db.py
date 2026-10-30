# -*- coding: utf-8 -*-
"""
기존 Pydroid 앱(recipe_card_app.py)의 레시피를 새 앱용 백업 파일로 바꿔요.
Pydroid에서 이 파일을 실행하면 RecipeCards 폴더에 recipes_backup.json 이 생겨요.
그 파일을 새 앱의 "백업 불러오기"로 선택하세요.
"""
import os, json, base64, sqlite3

for BASE in ("/storage/emulated/0/RecipeCards",
             os.path.join(os.path.expanduser("~"), "RecipeCards")):
    if os.path.exists(os.path.join(BASE, "recipes.db")):
        break
else:
    raise SystemExit("recipes.db 를 찾을 수 없어요 (RecipeCards 폴더 확인)")

con = sqlite3.connect(os.path.join(BASE, "recipes.db"))
con.row_factory = sqlite3.Row
out = []
for r in con.execute("SELECT * FROM recipes ORDER BY id"):
    photo = None
    p = os.path.join(BASE, "photos", f"{r['id']}.jpg")
    if os.path.exists(p):
        with open(p, "rb") as f:
            photo = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    out.append({
        "title": r["title"], "body": r["body"], "tags": r["tags"] or "",
        "prompt": r["prompt"] or "",
        "created": (r["created"] or "").replace(" ", "T") + "Z" if r["created"] else None,
        "photo": photo,
    })

dest = os.path.join(BASE, "recipes_backup.json")
with open(dest, "w", encoding="utf-8") as f:
    json.dump({"version": 1, "recipes": out}, f, ensure_ascii=False)
print(f"{len(out)}개 레시피를 내보냈어요 -> {dest}")
