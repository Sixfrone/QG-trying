# 基础绘制图表
## 折线图（曲线图）
plt.plot(x, y, color='red', linestyle='--', marker='o', label='数据系列')
* color：颜色，如 'blue', '#FF00AA'
* linestyle：线型，如 '-' 实线，'--' 虚线，':' 点线
* marker：数据点标记，如 'o' 圆点，'^' 三角形
* label：图例标签

## 散点图 -用于查看两个变量之间的关系
plt.scatter(x, y, color='green', s=50, alpha=0.5)
* s：点的大小
* alpha：透明度（0~1）


## 条形图 -用于比较分类数据
* 垂直条形：plt.bar(x, y)
* 水平条形：plt.barh(x, y)
eg.
categories = ['A', 'B', 'C']
values = [5, 7, 3]
plt.bar(categories, values, color='skyblue')
|现象：
x轴上有三个类别标签：A、B、C。每个条形的高度对应 values 列表中的数值：A 的高度为 5，B 的高度为 7，C 的高度为 3。所有条形的颜色均为浅蓝色（skyblue）。

## 扇形图（饼图）
eg.
sizes = [15, 30, 45, 10]
labels = ['类别1', '类别2', '类别3', '类别4']
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  # 使饼图为正圆
|startangle：起始角度 90°是从y轴正半轴开始算


# 图表装饰与定制
## 坐标轴
* plt.xlim(0, 10)：设置x轴范围
* plt.ylim(0, 50)
* plt.xticks(rotation=45)：倾斜x轴上的标签（防止重叠）
* plt.yticks([0, 20, 40])：自定义刻度

## 图例 -自动根据这些 label 生成图例，显示每条线对应的颜色、样式和名称
* 调用plt.legend()
eg.
plt.legend(loc='upper left') #loc 参数用于控制图例显示在图表中的位置-左上角

## 网格
plt.grid(True)：显示网格

## 保存图形
plt.savefig('output.png', dpi=300, bbox_inches='tight')
* dpi：分辨率
* bbox_inches='tight'：裁剪多余空白

## 综合示例
生成数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
创建画布和子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,4))
左子图：折线图 + 散点叠加
ax1.plot(x, y1, 'b-', label='sin')
ax1.scatter(x[::10], y1[::10], color='red', s=30, label='sin 采样')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('正弦曲线')
ax1.legend()
ax1.grid(True)
右子图：条形图
categories = ['A', 'B', 'C', 'D']
values = [15, 24, 18, 30]
ax2.bar(categories, values, color='orange', alpha=0.7)
ax2.set_xlabel('类别')
ax2.set_ylabel('数值')
ax2.set_title('分类数据')
ax2.set_ylim(0, 35)
整体
plt.tight_layout()
plt.savefig('combined_plot.png', dpi=200)
plt.show()






