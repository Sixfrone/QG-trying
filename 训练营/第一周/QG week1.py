#写在开始任务之前
#线性代数里矩阵到底在干嘛 * 旋转* 压缩* 剪切（斜着推）* 投影（压扁到平面）
#为啥要坐标系变换 |换个角度看数据 * 把数据转到方差最大的方向，更容易分类* 把数据挪到原点附近更容易训练* 把高维数据压到低维
# 在视觉AI里  * 像素坐标—相机坐标-世界坐标 让模型理解真实的物理位置* 应用： 相机标定，姿态估计，点云配准，PCA数据降维，图像反射变换
# 向量转移的本质  基：每个坐标系由一组基向量（通常是三个线性无关的向量）定义；  坐标：向量在坐标系下的坐标基向量上的线性组合系数

#数学基础
#如果A坐标系基向量是矩阵[a1,a2,a3](3*3矩阵) 若此时一个向量在其中的坐标是Xa=(x1,x2,x3)'T
# 此时这个向量在公共参考系的实际几何坐标为 Vworld = A⋅Xa(即基矩阵乘以坐标列向量)
#我们想求：已知Xa,要求Xb使得B⋅Xb=Vworld 即有 B*Xb = A * Xa 两边都左乘一个B-1有
#Xb=B-1*A*Xa 因此从A到B的坐标变换矩阵就Ta-b = B-1*A
#求坐标在新基向量下坐标就计算 Xb
##特殊情况 如果两个坐标系都是单位正交 则有B-1 = B.T
#对应的代码：transform_matrix = np.linalg.inv(new_axis) @ self.axis_vectors
#self.axis_vectors 对应A new_axis 对应B（目标坐标系的基向量在公共参考系中的表示）
#transform_matrix就是坐标变换矩阵
import json

import numpy as np

class CoordinateSystem:
    def __init__(self,name,axis_vectors,vectors):  #初始化坐标系，把数据转化为类属性
        self.name = name
        self.axis_vectors = np.array(axis_vectors,dtype=float).T   #这里要把输入的基向量转置 因为数组默认列向量是基向量
        self.vectors = np.array(vectors,dtype=float)   #普通向量不需要转置
        self.dimension = self.axis_vectors.shape[0]
        if len(self.vectors) > 0:
            assert self.vectors.shape[1] == self.dimension, \
                f"向量维度({self.vectors.shape[1]})与坐标系维度({self.dimension})不一致"
        ######向量可以进行坐标系转移的条件：
        #1.维度匹配 2.基向量线性无关

    def is_valid_coordinate(self,tolerance: float = 1e-10):
        if self.axis_vectors.shape[0] != self.axis_vectors.shape[1]: #检查维度是否匹配，是否是个方阵
            return False, f"基向量个数({self.axis_vectors.shape[1]})不等于维度({self.axis_vectors.shape[0]})"
        det = np.linalg.det(self.axis_vectors) #在计算行列式绝对值 行列式是否是0 是否线性无关
        if abs(det) < tolerance:
            return False, f"基向量线性相关，行列式 = {det:.2e}"
        return True, f"有效坐标系，行列式={det:.4f}"

    def change_axis(self,new_axis_vectors,vectors_to_transform=None):
        new_axis = np.array(new_axis_vectors, dtype=float).T # 转换目标基为列向量矩阵
        if new_axis.shape[0] != self.dimension:
            raise ValueError(f"目标基维度({new_axis.shape[0]})与当前坐标系维度({self.dimension})不匹配")
        if vectors_to_transform is None:
            vecs = self.vectors
        else:
            vecs = vectors_to_transform
        if vecs.shape[1] != self.dimension:
            raise ValueError(f"待转换向量维度({vecs.shape[1]})与当前坐标系维度({self.dimension})不匹配")
        transform_matrix = np.linalg.inv(new_axis) @ self.axis_vectors #计算旧坐标系到新坐标系的“单位换算矩阵”
        transformed_vectors = (transform_matrix @ vecs.T).T #批量对目标向量进行操作
        return  CoordinateSystem(f"{self.name}_transformed",new_axis_vectors,transformed_vectors) #创建一个新的坐标系对象返回
        #可以通过这个打包看出来新对象的名字是f"{self.name}_transformed"，通常是原名字加上后缀，便于识别

    def axis_angle(self,in_degrees=False):
        n = self.axis_vectors.shape[1]
        angles = []
        for i in range(n):
            for j in range(i+1,n):
                v1 = self.axis_vectors[:, i]
                v2 = self.axis_vectors[:, j]
                cos = np.dot(v1,v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)) #计算余弦值
                angle = np.arccos(np.clip(cos, -1, 1)) #定最大最小值 保证数值的稳定
                angles.append((i,j,np.degrees(angle)))
        return angles


    def axis_projection(self,vector_idx:int): #计算投影长度
        v = self.vectors[vector_idx]
        projections = []
        for i in range(self.axis_vectors.shape[1]): #动态获取每个向量的维数
            axis = self.axis_vectors[:,i]
            proj_len = np.dot(v,axis) / np.linalg.norm(axis) #计算标量土投影，返回的是一个数字
            projections.append((i,proj_len))
        return projections

    def area(self):
        return abs(np.linalg.det(self.axis_vectors)) #直接计算体积，数学上是行列式的绝对值


    def get_vector_coordinates(self,vector_idx:int,in_standard_basis:bool=True): #获取指定向量的坐标表示
        v = self.vectors[vector_idx]
        if in_standard_basis :
            return v
        else:
            coords = np.linalg.solve(self.axis_vectors,v)
            return coords


def load_and_process_json(filename): #加载文件并且处理所有任务
    with open(filename,'r',encoding='utf-8') as f: #打开文件并且设置为只读模式 后面的是中文显示正确读取中文字符
        data = json.load(f)
    all_results =[]
    for group in data:
        group_name = group['group_name']
        vectors = group['vectors']
        ori_axis = group['ori_axis']
        tasks = group['tasks'] #从文件里读取任务 方便后续任务对应每个模块的代码
        print(f"\n{'='*60}")
        print(f"处理组: {group_name}")
        print(f"{'='*60}")

        # 创建原始坐标系
        original_system = CoordinateSystem(f"{group_name}_original", ori_axis, vectors)
        print(original_system)
        is_valid, reason = original_system.is_valid_coordinate()
        print(f"坐标系有效性检查: {reason}")

        if not is_valid:
            print("原始坐标系无效，跳过")
            continue

        group_result = {
            "group_name": group_name,
            "original_valid": is_valid,
            'tasks': []
        }

        #处理每个任务
        for i,task in enumerate(tasks,1):
            task_type = task['type']
            print(f"\n--- 任务 {i}: {task_type} ---")
            task_result = {'type': task_type}

            try:
                if task_type == 'axis_angle':
                    # 计算基向量夹角
                    angles = original_system.axis_angle()
                    print("基向量夹角结果:")
                    for idx1, idx2, angle in angles:
                        print(f"  基向量{idx1}与基向量{idx2}的夹角: {angle:.2f}°")
                    task_result['angles'] = [(int(idx1), int(idx2), float(angle))
                                             for idx1, idx2, angle in angles]

                elif task_type == 'area':
                    # 计算面积/体积
                    area = original_system.area()
                    dim = original_system.dimension
                    unit = "面积" if dim == 2 else "体积" if dim == 3 else "超体积"
                    print(f"{unit}: {area:.4f}")
                    task_result['area'] = float(area)

                elif task_type == 'axis_projection':
                    # 计算向量投影（默认计算第一个向量）
                    if len(vectors) > 0:
                        projections = original_system.axis_projection(0)
                        print(f"向量{vectors[0]}在各基向量上的投影:")
                        for axis_idx, proj_len in projections:
                            print(f"  基向量{axis_idx}: {proj_len:.4f}")
                        task_result['projections'] = [(int(axis_idx), float(proj_len)) for axis_idx,proj_len in projections] #将投影结果存储到结果字典里

                elif task_type == 'change_axis':
                    if 'obj_axis' in task:
                        obj_axis = task['obj_axis']
                        print(f"目标基向量: {obj_axis}")
                        new_system = original_system.change_axis(obj_axis) #执行转移
                        print(new_system)
                        is_new_valid, new_reason = new_system.is_valid_coordinate () #检查坐标系是否有效
                        print(f"目标坐标系有效性：{new_reason}")
                        task_result['target_valid'] = is_new_valid #将新坐标系的有效性检查结果保存到任务字典里，以便于后续的统一输出
                        task_result['target_reason'] = new_reason

                        if is_new_valid and len(new_system.vectors) > 0: #如果有效
                            task_result['transformed_vectors'] = new_system.vectors.tolist() #将坐标系转换后的向量数据存储到结果字典里，new_system.vectors 是一个 NumPy 数组来存储
                            print("转换后的向量:")
                            for j, vec in enumerate(new_system.vectors):
                                coords = new_system.get_vector_coordinates(j, in_standard_basis=False) #打印在字典里存储的结果
                                print(f"  向量{j}在新基下的坐标: {coords}")
            except Exception as e:
                print(f"任务执行出错：{e}")
                task_result['error'] = str(e)

            group_result['tasks'].append(task_result)
        all_results.append(group_result)
    return all_results

def main():
    results = load_and_process_json('QG data(1).json')
    with open('results.json','w',encoding='utf-8') as f:  #打开文件，是可以写的形式
        json.dump(results,f,indent=2,ensure_ascii=False) #result是要写入的数据 f是已经打开的文件对象 2是缩进 False是允许输出非ASCII字符
    print("\n结果已保存到results.json")

if __name__ == '__main__':
    main()






























































































