import json

with open("ingredients.json", "r") as read_file:
	data = json.load(read_file)
result = []
pk_num = 1

for item in data:
	result.append({"pk": pk_num , "model": "recipes.ingredients", "fields":
		item })
	pk_num += 1

new_data = json.dumps(result, indent=4)
f = open("ingredients2.json", "w")
f.write(new_data)
f.close()