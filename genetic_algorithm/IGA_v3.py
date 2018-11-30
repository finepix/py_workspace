"""
    GA 模型， 用遗传算法求解OTSU
"""
import random
import matplotlib.pyplot as plt
import time
import cv2


class GA:
    def __init__(self, img, fitness, population_num, evolution_times, ga_length=8, crossover_pro=0.5,
                 variation_pro=0.001):
        """
                    GA model，对种群参数以及种群进行初始化
        :param img:                     图像数据
        :param fitness:                 适应度函数
        :param population_num:          种群数量
        :param evolution_times:         种群迭代次数
        :param ga_length:               基因长度
        :param crossover_pro:           交换概率
        :param variation_pro:           变异概率
        """
        # 图像数据
        self.data = img
        # 基因长度
        self.ga_length = ga_length
        # 种群数量
        self.population_num = population_num
        # 适应度函数
        self.fitness = fitness
        # 进化次数（产生多少代后代）
        self.evolution_times = evolution_times
        # 交叉以及变异概率
        self.crossover_pro = crossover_pro
        self.variation_pro = variation_pro
        # 画图参数
        self.plt = plt
        x = range(pow(2, self.ga_length))
        y = [self.fitness(self.data, i) for i in x]
        max_y = max(y)
        index_max = y.index(max_y)
        self.x = x
        self.y = y
        self.max_y = max_y
        self.index_max = index_max
        self.min_y = min(y)

        # 随机产生种群，并且编码
        self.populations = []
        self.new_populations = []
        # todo  pow(2, self.ga_length) - 1
        max_num = pow(2, self.ga_length) - 1
        for i in range(self.population_num):
            pop = random.randint(0, max_num)
            pop = self.num_encode(pop)
            self.populations.append(pop)

        # todo initialize

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
        # todo IGA_v3 和 IGA 不同之处
        # self.populations = remain_populations
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

    def run(self):
        # todo 添加可视化图像
        for i in range(self.evolution_times):

            # view data in plot
            fitness_list = self.calculate_fitness_list()
            max_val = max(fitness_list)
            min_val = min(fitness_list)

            # 绘图
            # if i != 0 and i % 10 == 0:
            if i % 50 == 0:
                self.plot_data(fitness_list, i)
            # 保存绘图
            self.plot_data(fitness_list, i, True)

            gen = self.statistics()
            print('iterations at {}, max is {}, min is {}'.format(i, max_val, min_val))
            # todo delete
            # print('result:', gen)

            # main step
            self.selection()
            # self.selection_v2()
            self.crossover()
            self.variation()

            # stop condition
            flag = False
            for g in gen:
                if g > self.population_num * 0.98:
                    flag = True
                    break
            if flag:
                break
        return max(gen)

    def plot_data(self, fitness_list, it, save_fig=False):
        """
                绘图以及保存图像
        :param fitness_list:
        :param it:
        :param save_fig:
        :return:
        """
        self.plt.figure(1)
        self.plt.clf()
        self.plt.xlabel('Gray scale')
        self.plt.ylabel('Fitness value')
        self.plt.title('Generation at {}'.format(it))

        self.plt.plot(self.x, self.y, '-g')
        y_lim = self.plt.ylim()
        plt.plot([self.index_max, self.index_max], y_lim, 'm--')
        y_min = self.min_y
        y_max = self.max_y + 100
        plt.ylim(y_min, y_max)
        plt.xlim(0, 255)

        populations = [self.num_decode(pop) for pop in self.populations]

        self.plt.scatter(populations, fitness_list)
        self.plt.show()
        if save_fig:
            file_name = 'ga_process/' + 'iter_' + str(it) + '.jpg'
            self.plt.savefig(file_name)

        # time.sleep(0.2)

    def statistics(self):
        """
                    统计每一次迭代的后代结果
        :return:
        """
        populations = self.populations
        populations = [self.num_decode(pop) for pop in populations]

        # 计数
        result_len = pow(2, self.ga_length)
        # 0 * i = 0， 代码洁癖
        result_iter = [0 * i for i in range(result_len)]
        for pop in populations:
            result_iter[pop] += 1

        # print(result_iter)
        return result_iter

    def calculate_fitness_list(self):
        """
            计算适应度值，抽出来利于代码复用
        :return:
        """
        fitness_list = []
        for pop in self.populations:
            p = self.num_decode(pop)
            # 计算适应度值
            p = self.fitness(self.data, p)
            fitness_list.append(p)
        return fitness_list

    def num_encode(self, n):
        """
            对灰度值进行编码（二进制），并且将编码后的值转化为8位的（存在不到8位的情况）
        :param n:
        :return:
        """
        r = bin(n)
        r = r[2:]
        if len(r) < self.ga_length:
            diff = self.ga_length - len(r)
            tmp_r = []
            for j in range(diff):
                zero = str(bin(0)[-1])
                tmp_r.append(zero)

            for s in r:
                tmp_r.append(s)

            r = ''.join(tmp_r)

        return r

    @staticmethod
    def num_decode(bn):
        """
                将二进制数组转化为十进制，解码
        :param bn:
        :return:
        """
        s = ''
        for b in bn:
            s += b
        r = int(s, 2)
        return r


def test_fitness(x):
    return x * x + 2


# if __name__ == '__main__':
#     num = 100
#     file_path = 'images\ship_1.jpg'
#     image = cv2.imread(file_path)
#     model = GA(image, test_fitness, 100, 1000)
#     model.run()
#     # x = range(pow(2, 2))
#     # y = [test_fitness(i) for i in x]
#     # fig = plt.figure(1)
#     # plt.plot(x, y)
#     # fig.show()
