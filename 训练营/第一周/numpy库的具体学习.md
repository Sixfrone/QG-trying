## 基于列表构建矩阵
* matrix = np.array([[1,2,3,],[4,5,6]])

## 特殊矩阵的构建
* 零矩阵 zeros = np.zeros((3,4))
* 全1矩阵 ones - np.ones((2,3))
* 单位矩阵 eye = np.eye(3)
* 对角矩阵 diag = np.diag([1,2,3])
* 随机矩阵 
| 均匀分布 [0,1) rand_uniform = np.random.rand(2,3)
| 标准正态分布 rand_normal = np.random.randn(2,3)
| 指定范围的随机整数 rand_int = np.random.randint(0,10,sizxe=(3,4))   # 0~9之间的整数，3行4列
* 填充特定值的矩阵 full = np.full((2,2),7.5) #全部填充为 7.5
* 空矩阵 empty = np.empty((3,3))
* 等差数列矩阵
| 一维等差 arr = np.arange(12).reshape(3,4) # 0~11，3行4列
| 指定范围与步长  arr = np.arange(0,1,0.2).reshape(2,3)
* 等间隔数列矩阵 linespace = np.linspace(0,1,5).reshape(5,1)

## 矩阵乘法
* np.dot() 点积函数——教科书的矩阵乘法
eg.
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.dot(a, b))
* np.matmul()和 @ 运算符
| 原理：1.对于二维数组，行为与 np.dot() 相同。2.对于一维数组，首先将其提升为二维（通过在其前面加一个维度 1），乘法后再将多余的维度移除。因此，一维数组可以被视为行向量或列向量，具体取决于位置。3.对于高维数组，它执行的是最后两维的矩阵乘法，并广播前面的维度。
| 语法：np.matmul(a, b, out=None)或 a @ b
eg.
A = np.array([[1, 2], [3, 4]])
v = np.array([1, 2])
w = np.array([1, 2])
print(A @ v) # 输出: [5 11] ，v视为列向量
print(w @ A) # 输出: [7 10] , w视为行向量
* np.linalg.multi_dot() —— 多个矩阵连乘
| 原理：自动选择最优的乘法顺序（类似矩阵链乘问题），以最小化计算量 语法： np.linalg.multi_dot(arrays, *, out=None)
eg.
A = np.random.rand(100, 10)
B = np.random.rand(10, 200)
C = np.random.rand(200, 50)
D2 = np.linalg.multi_dot([A, B, C])
* np.multiply()或 * —— 逐元素乘法
| 要求： 两个数组形状相同或可广播
eg.
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(np.multiply(A, B)) # 输出:
                                # [[ 5 12]
                                #  [21 32]]

## 广播机制
1. 作用：允许不同形状的数组进行算术运算
2. 规则：
| 从最后一个维度开始，向前比较两个数组每个维度的大小
| 比较时，两个维度只要满足下面任一条件，就可以继续：1.它们相等； 2.其中一个等于 1； 3. 其中一个数组在这个维度上压根没有（可以想象成这个维度的大小是 1；
3. eg.
A = np.ones((2, 3))   # 形状 (2, 3)
print(A + 5)        # 5 是一个标量，形状是 ()，可以看作 (1, 1)
解释：A的最后一个维度是3（两行三列），标量5第一个维度也是最后一个维度是零维视为1满足广播规则 A倒数第二个维度是2，标量依旧0维依旧是1 满足广播规则 所以形状对齐就是（2，3），效果是每个元素加5

## 矩阵转置 使用 .T 属性或 np.transpose()
eg.
A = np.array([[1, 2, 3], [4, 5, 6]])
print(A.T)  输出：    # [[1 4]
                      #  [2 5]
                      #  [3 6]

## 矩阵的逆 np.linalg.inv()，要求矩阵可逆（方阵且满秩）
A = np.array([[1, 2], [3, 4]])
A_inv = np.linalg.inv(A)
print(A_inv)      输出：# [[-2.   1. ]
                       #  [ 1.5 -0.5]]
                        # 验证：A @ A_inv 应接近单位矩阵

## 其他操作
### 矩阵展平成一维数组
1. 创建副本
eg.
M = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12]])
flat = M.flatten() #flatten() 返回的是原数组的一个副本，修改返回的数组不会影响原数组
print(flat)
2. ravel() 返回的是原数组的一个视图
eg.
flat = M.ravel()
print(flat)
### 索引与切片
eg.
M = np.arange(12).reshape(3,4)
print(M[1, 2])        # 第2行第3列元素（索引从0开始）
print(M[0:2, 1:3])    # 前两行，第2~3列
print(M[:, [0,2]])    # 所有行，第1列和第3列
### 矩阵拼接与分割
| np.vstack()（垂直堆叠），np.hstack()（水平堆叠)
eg.
A = np.ones((2,2))
B = np.zeros((2,2))
C = np.vstack((A, B))   # 4行2列
D = np.hstack((A, B))   # 2行4列
### 分割
eg.
M = np.arange(12).reshape(3,4)
parts = np.hsplit(M, 2)   # 水平分割成2块，每块3行2列
### 矩阵的迹
eg.
trace = np.trace(M) # 迹（对角线元素和）
### 行列式
eg.
det = np.linalg.det(M) #求行列式的值
### 特征值
eg.
eigenvalues, eigenvectors = np.linalg.eig(M) #求特征值与特征向量
### 关于np.reshape中-1的用法——自动计算
arr = np.arange(12)
new_arr = arr.reshape(4, -1)
print(new_arr.shape)
解释：这里 -1 被自动计算为 3，因为总元素 12 ÷ 4 = 3，所以列数为 3。也可以把-1放在行数的位置。但是-1 只能出现一次（否则无法唯一确定形状















