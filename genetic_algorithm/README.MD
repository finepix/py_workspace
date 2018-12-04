杭电模式识别课程设计作业

# 最大类间方差法(Otsu)
> 详见https://www.cnblogs.com/xiaomanon/p/4110006.html，这里就不去赘述了。

# 遗传算法策略
> 关于遗传算法的详解什么的，可以参考其他的类似文章，下面讲讲我自己的策略

## 种群编码策略
二进制，优点在于方便理解，缺点在于python对于二进制数的处理有点鸡肋。
## 选择策略
轮盘选择法(有待改进)
缺点在于：若变异产生了一个新的最大值（更接近于最优值），但是其种群数量就只有1，远远比不上当前的最大值（离最优值远一点）。若直接使用轮盘选择法，那么这个新变异出来的值就会被覆盖掉。
改进：强制将上一代中最大的值进行保留，这样使得种群不会退化
## 交换策略
从基因一半往后的位置开始交换，这样有利于保持当前的最优值，使得交换之后的种群不至于很差。（待改进，对于最大值个体不进行交换操作）

 - Step1：产生一个概率，若小于交换概率，那么进行step2往后，否则处理下一个个体；
 -
   Step1：将种群的population乱序排列，取出前一半作为father，后一半作为mother；

   Step2：产生half-end的随机位置，然后从father和mother中各选出一位出来配对，交换。

## 变异策略
对于每一个个体，对于任意位置产生一位变异，但是变异概率不宜设计的很大，这样会导致种群不容易收敛。（待改进，对于最大值个体不进行变异操作）

 - Step1：产生一个概率，若小于变异的概率，那么进行step2往后，否则处理下一个个体；
 - Step2：产生一个随机位置start-end；
 -    Step3：将该个体位置对应的随机位置的值取反。

## 停止条件
需满足以下其一即可：
1：满足种群迭代的最大值；
2：种群的0.98的个体都指向同一个值。
# 核心代码
## otsu
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

GRAY_SCALE = 256


def otsuth(img, threshold):
    image_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # fg_pro = np.zeros((1, GRAY_SCALE))
    # bg_pro = np.zeros((1, GRAY_SCALE))

    # fg_sum = 0
    # bg_sum = 0
    # for col in image_gray:
    #     for pix in col:
    #         if pix > threshold:
    #             fg_pro[0, pix] += 1
    #             fg_sum += pix
    #         else:
    #             bg_pro[0, pix] += 1
    #             bg_sum += pix
    #
    # if fg_sum != 0:
    #     fg_pro = fg_pro / fg_sum
    # if bg_sum != 0:
    #     bg_pro = bg_pro / bg_sum

    fg_pix = image_gray > threshold
    bg_pix = image_gray <= threshold

    w0 = float(np.sum(fg_pix)) / image_gray.size
    w1 = float(np.sum(bg_pix)) / image_gray.size

    u0 = 0
    u1 = 0
    if np.sum(fg_pix) != 0:
        u0 = np.sum(image_gray * fg_pix) / np.sum(fg_pix)
    if np.sum(bg_pix) != 0:
        u1 = np.sum(image_gray * bg_pix) / np.sum(bg_pix)

    val = w0 * w1 * (u0 - u1) * (u0 - u1)
    return val


if __name__ == '__main__':
    file_path = 'images\ship.jpg'
    image = cv2.imread(file_path)
    cv2.imshow('origin_img', image)
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    image_gray[image_gray > 143] = 255

    cv2.imshow('IM_OTSU', image_gray)
    cv2.waitKey(-1)

```
> 将该函数传入GA model，当做适应度函数
## GA

```python
def selection(self):
    """
            通过轮盘法选择(改进算法)，保留最大值对应的个体，防止种群退化
    :return:
    """
    # 计算每一个个体的适应度值
    fitness_list = self.calculate_fitness_list()
    max_fitness = max(fitness_list)

    # step1:将最大值和其余的值分离，并且将populations重新赋值
    new_populations = []
    remain_populations = []
    for i in range(len(fitness_list)):
        if fitness_list[i] == max_fitness:
            new_populations.append(self.populations[i])
        else:
            remain_populations.append(self.populations[i])

    # 将剩下的populations赋值给model
    self.new_populations = new_populations
    self.populations = remain_populations
    fitness_list = self.calculate_fitness_list()

    # step2:计算概率
    fitness_sum = 0.0
    for fit in fitness_list:
        fitness_sum += fit
    fitness_pro = []
    for i in range(len(fitness_list)):
        fitness_pro.append(fitness_list[i] / fitness_sum)

    # step3:计算剩余人口的轮盘选择概率
    pro_sum = 0.0
    for i in range(1, len(fitness_pro)):
        pro_sum += fitness_pro[i]
        fitness_pro[i] = pro_sum
    # 在计算中由于浮点数计算会存在误差导致最后的概率之和不为1，这里纠正
    fitness_pro[-1] = 1

    next_generations = []
    # step4:轮盘选择出与剩下的人数相等的population
    for i in range(len(remain_populations)):
        # 产生一个0 - 1的概率
        pro = random.uniform(0, 1)

        # 可优化（先计算完轮盘选择的全部概率分布，归结子问题），见上
        if pro <= fitness_pro[0]:
            next_generations.append(self.populations[0])
            continue
        for j in range(self.population_num - 1):
            if fitness_pro[j] < pro < fitness_pro[j + 1]:
                next_generations.append(self.populations[j + 1])
                break
    self.populations = next_generations

def crossover(self):
    """
            种群交叉，，先reshuffle截取前面一半用作父亲，后面用作母亲
    :return:
    """
    # # todo delete
    # gen = self.statistics()
    # print('before cross:', gen)

    # reshuffle
    # self.populations = random.shuffle(self.populations)
    random.shuffle(self.populations)

    half = int(len(self.populations) / 2)
    fathers = self.populations[:half]
    mothers = self.populations[half:]

    next_generations = []
    for i in range(half):
        father = fathers[i]
        mother = mothers[i]

        pro = random.uniform(0, 1)
        if pro < self.crossover_pro:
            # todo 位置从一半开始，防止每一次变化过大（待优化，每一次迭代需要将最大的值保留下来，这样能保证种群不会退化）
            index = random.randint(self.ga_length / 2, self.ga_length)
            child_a = father[:index] + mother[index:]
            child_b = mother[:index] + father[index:]

            next_generations.append(child_a)
            next_generations.append(child_b)
        else:
            next_generations.append(father)
            next_generations.append(mother)

    if len(self.populations) % 2 != 0:
        next_generations.append(self.populations[-1])

    self.populations = next_generations

    # # todo delete
    # gen = self.statistics()
    # print('after cross:', gen)

def variation(self):
    """
            变异，没用到左移右移以及取反操作，python无bit类型数据结构
    :return:
    """
    # # todo delete
    # gen = self.statistics()
    # print('before variation:', gen)

    length = len(self.populations)
    for i in range(length):
        pop = self.populations[i]
        # TypeError: 'str' object does not support item assignment
        pop = list(pop)
        pro = random.uniform(0, 1)
        # todo
        if pro < self.variation_pro:  # self.variation_pro
            index = random.randint(0, self.ga_length - 1)
            j = pop[index]
            if int(j) == 0:
                pop[index] = 1
            else:
                pop[index] = 0
            string = "".join('%s' % s for s in pop)
            self.populations[i] = string

    for p in self.new_populations:
        self.populations.append(p)
```
> 以上实现为：选择、交叉、变异 各步骤。

## 博客地址
https://blog.csdn.net/qq_26479655/article/details/84568462