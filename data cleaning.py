intel = " Agent:007_Bond; Coords:(40,74); Items:gun,money,gun; Mission:2025-RESCUE-X "

cleaned_intel = intel.strip()
print(f"清洗后的情报是：{cleaned_intel}")

parts = cleaned_intel.split(';')

agent_info = parts[0].split(':')[1]

coords_str = parts[1].split(':')[1].strip()
coords_str = coords_str.replace('(', '')
coords_str = coords_str.replace(')', '')
coords_tuple = tuple(map(int, coords_str.split(',')))

items_str = parts[2].split(':')[1].strip()
items_list = items_str.split(',')
unique_items = set(items_list)
unique_items_list = list(unique_items)

mission_str = parts[3].split(':')[1].strip()

agent_dossier = {
    "Agent": agent_info,
    "Coords": coords_tuple,
    "Item": items_list,
    "Mission": mission_str,
}

print("\n=== 数据清洗结果 ===")
print(f"特工:{agent_dossier['Agent']}")
print(f"坐标:{agent_dossier['Coords']}")
print(f"物品: {agent_dossier['Item']} ")
print(f"任务: {agent_dossier['Mission']}")

print("\n=== 完整档案 ===")
for key, value in agent_dossier.items():
    print(f"{key}: {value}")

