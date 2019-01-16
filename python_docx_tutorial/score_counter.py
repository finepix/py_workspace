def sc_count(a, b):
    """

    :param a:    基准
    :param b:    待测
    :return:
    """
    count = 0
    for i in range(len(b)):
        if b[i] == -1:
            continue
        else:
            # print(i)
            count += 1 if a[i] == b[i] else 0
    return count
