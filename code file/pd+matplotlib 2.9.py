import pandas as pd
import matplotlib.pyplot as plt

#懒得下载加州房价了 本地里有个文物数
#基础阅读
df = pd.read_csv('data3.csv')
print('前两行是：',df.head(2))
print('最后两行是：',df.tail(2))
print('数值列的描述统计如下：',df.describe())
print('行数和列数是：',df.shape)
print('列名和列数是：',df.columns)
#处理数据
print('缺失值如下：',df.isnull())
df.fillna(df.mean(numeric_only=True), inplace=True) #直接在原来的数据上修改 这个true
print(df)
#排序
df.sort_values(by=['二氧化硅(SiO2)'],ascending=True,inplace=True) #升序与否 直接在原来的地方修改与否
#保存
df.to_csv('cleaned_data.csv', index=False)


#对于文物数据这里生成了xy轴数据并且绘制的是折线图
x = df['二氧化硅(SiO2)']
y = df['氧化钠(Na2O)']
plt.plot(x, y, color='red', linestyle='--', marker='o', label='文物数据')
plt.show()