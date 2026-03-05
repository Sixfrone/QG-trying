import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows 常见黑体
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('train.csv')
##可以利用分组进一步可视化
bins = [0,12,18,35,60,100]
labels = ['儿童','青少年','青年','中年','老年']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins,labels=labels)
df['fareGroup']=pd.qcut(df['Fare'], q=4,labels=['低','中低','中高','高'])

plt.figure(figsize = (14,12))
#整个绘图区域划分为 3 行 3 列 的网格（共 9 个小图），然后激活第 2 个子图作为当前绘图的目标
plt.subplot(3,3,1)
sns.barplot(x='Sex', y='Survived', data=df)
plt.title('性别与生还率')
plt.ylabel('生还率')

plt.subplot(3, 3, 2)
sns.barplot(x='Pclass', y='Survived', data=df)
plt.title('船舱等级与生还率')
plt.ylabel('生还率')

plt.subplot(3, 3, 3)
sns.barplot(x='AgeGroup', y='Survived', data=df)
plt.title('年龄与生还率')
plt.ylabel('生还率')

plt.subplot(3, 3, 4)
sns.barplot(x='SibSp', y='Survived', data=df)
plt.title('兄弟姐妹/配偶数与生还率')
plt.ylabel('生还率')

plt.subplot(3, 3, 5)
sns.barplot(x='Parch', y='Survived', data=df)
plt.title('父母/子女数与生还率')
plt.ylabel('生还率')

plt.subplot(3, 3, 6)
sns.barplot(x='Embarked', y='Survived', data=df)
plt.title('登船港口与生还率')
plt.ylabel('生还率')

plt.subplot(3, 3, 7)
sns.barplot(x='fareGroup', y='Survived', data=df)
plt.title('票价与生还率')
plt.ylabel('生还率')
#绘制年龄与幸存与否的核密度估计图
plt.subplot(3, 3, 8)
sns.kdeplot(df[df['Survived']==1]['Age'], label='幸存者', fill=True) #fill用于控制是否在密度曲线下方填充颜色
sns.kdeplot(df[df['Survived']==0]['Age'], label='遇难者', fill=True)
plt.title('幸存者与遇难者年龄分布')
plt.xlabel('年龄')
plt.ylabel('密度')
plt.legend()

plt.subplot(3, 3, 9)
sns.kdeplot(df[df['Survived']==1]['Fare'], label='幸存者', fill=True)
sns.kdeplot(df[df['Survived']==0]['Fare'], label='遇难者', fill=True)
plt.title('幸存者与遇难者票价分布')
plt.xlabel('票价')
plt.ylabel('密度')
plt.legend()

#智能地调整子图之间的间距、边距等，使得轴标签、刻度标签、标题等元素不会重叠，整个图形看起来更紧凑、美观
plt.tight_layout()
plt.show()