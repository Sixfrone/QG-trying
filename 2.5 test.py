raw_data = ["85", "92", "ERROR", "105", "78", "WARNING", "99","120"]

num_list = []
for x in raw_data:
    try:
        num = int(x) / 100
        num_list.append(num)
        if (num > 1):
            print(f'{num}:负载运行')
        if (num < 1):
            print(f'{num}:正常运行')
    except ValueError:
        pass

print(num_list)

