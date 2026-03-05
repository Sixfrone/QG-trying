## Pandas 基础数据结构
### Series（带索引的一维数组）
eg.
* 从列表创建（默认索引 0,1,2...）
s1 = pd.Series([10, 20, 30])
print(s1)
输出：
0    10
1    20
2    30
dtype: int64
* 指定自定义索引
s2 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s2)
输出：
a    10
b    20
c    30
dtype: int64
* 从字典创建（键变成索引
s3 = pd.Series({'apple': 5, 'banana': 3, 'orange': 8})
print(s3)
输出：
apple     5
banana    3
orange    8
dtype: int64

### DataFrame（带行列标签的二维表格）
eg.
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['New York', 'Paris', 'London']
}
df = pd.DataFrame(data)
print(df)
输出：
      name  age      city
0    Alice   25  New York
1      Bob   30     Paris
2  Charlie   35    London

## 数据读取
* CSV
df = pd.read_csv('文件路径.csv')
| 这个文件路径是同一个文件目录下的命名
| 如果不在同一个文件目录就需要复制完整文件地址
* Excel
pd.read_excel('文件路径', sheet_name='工作表名')

## 初步查看数据
* df.head(n)：查看前 n 行（默认5行）
* df.tail(n)：查看后 n 行
* df.info()：查看列名、非空计数、数据类型
* df.describe()：数值列的描述统计（均值、标准差、分位数等）
* df.shape：行数和列数
* df.columns：列名列表

## 数据选择与过滤
* 列选择
| df['列名'] 或 df.列名：选取单列（返回 Series）
| df[['列1', '列2']]：选取多列（返回 DataFrame）
* 行选择
| df.iloc[行索引]（整数位置），df.iloc[开始:结束, 列范围]
| df.loc[行标签, 列标签]，支持切片和条件
* 条件过滤
df[df['年龄'] > 30]                # 年龄大于30的行
df[(df['性别'] == '男') & (df['年龄'] < 20)]   # 多条件

## 处理缺失值
* 检测：df.isnull() 或 df.isna()，配合 sum() 查看每列缺失数
* 删除：df.dropna()：删除包含缺失值的行（可设置 axis=1 删除列，how='all' 仅当全为缺失时删除）
* 填充：df.fillna(value)：用指定值填充
df.fillna(method='ffill')：用前一个值填充（向前填充）
df.fillna(df.mean())：用列均值填充

## 处理重复值
* 检测：df.duplicated() 返回布尔Series，标记重复行（默认除第一次外）
* 删除：df.drop_duplicates() 删除重复行，可指定 subset 列和 keep 参数（first/last/False）

## 数据类型转换
* 查看类型：df.dtypes
* 转换：df['列名'].astype('类型')，如 astype('int'), astype('float'), astype('datetime64')
* 处理日期：pd.to_datetime(df['日期列'])

## 排序
* 按值排序：df.sort_values(by='列名', ascending=True)，多列可用列表
* 按索引排序：df.sort_index()

## 列操作
* 添加新列：直接赋值 df['新列'] = ...，可基于现有列计算
* 删除列：df.drop('列名', axis=1, inplace=True)
* 重命名列：df.rename(columns={'旧名':'新名'}, inplace=True)

## 其他操作
* pd.concat([df1, df2])：合并多个DataFrame
* df.sample(n)：随机抽取n行
* df.nunique()：每列唯一值个数
* df.value_counts()：列中值计数（常用于分类列）

## 综合示例
| 读取数据
df = pd.read_csv('data.csv')
| 查看基本信息
print(df.info())
| 处理缺失值：删除全为空的列，填充年龄缺失值为均值
df.dropna(axis=1, how='all', inplace=True)
df['年龄'].fillna(df['年龄'].mean(), inplace=True)
| 删除重复行
df.drop_duplicates(inplace=True)
| 转换日期格式
df['日期'] = pd.to_datetime(df['日期'])
| 过滤出有效数据
df = df[df['年龄'] > 0]
| 重命名列
df.rename(columns={'姓名':'name', '年龄':'age'}, inplace=True)
| 保存清洗后的数据
df.to_csv('cleaned_data.csv', index=False)





















