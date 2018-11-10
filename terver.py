from math import gcd, pow, sqrt, log2, isclose
from prettytable import PrettyTable
from fractions import Fraction as f

def lcm(a, b):
    return a * b / gcd(a, b)


def make_random_var(xi, eta, func):
    result = {}
    for k, v in xi.items():
        for k1, v1 in eta.items():
            new_key = func(k, k1)
            if new_key in result.keys():
                result[new_key] += v * v1
            else:
                result[new_key] = v * v1
    return result


def compute_average(random_var, _pow = 1):
    result = 0
    for k, v in random_var.items():
        result += pow(k, _pow) * v
    return result


def compute_variance(random_var):
    return compute_average(random_var, 2) - compute_average(random_var)**2


def compute_less_more(keys, random_var):
    p = 0
    for key in keys:
        p += random_var[key]
        if p > 0.5 or p == 0.5: return key


def compute_middle(random_var):
    keys = sorted(random_var.keys())
    m_down = None
    m_up = None
    for key in keys:
        if m_down: break
        m_down = compute_less_more(keys[:keys.index(key)+1], random_var)
    keys.reverse()
    for key in keys:
        if m_up: break
        m_up = compute_less_more(keys[keys.index(key):], random_var)
    return max(m_up, m_down)


def compute_covariance(xi, eta, xi_eta):
    return compute_average(xi_eta) - compute_average(xi)*compute_average(eta)


def compute_correlation(xi, eta, xi_eta):
    return compute_covariance(xi, eta, xi_eta)/sqrt(compute_variance(xi)*compute_variance(eta))


def compute_entropy(xi_keys, eta_keys, xi_eta):
    result = 0
    for xi_i in xi_keys:
        for eta_i in eta_keys:
            p =  xi_eta.get((xi_i, eta_i))
            result -= p*log2(p)
    return result


if __name__ == '__main__':
    xi = {1: f(1, 6), 2: f(1, 6), 3: f(1, 6), 4: f(1, 6), 5: f(1, 6), 6: f(1, 6)}

    eta = {1: f(1, 12), 2: f(1, 12), 3: f(1, 3), 4: f(1, 3), 5: f(1, 12), 6: f(1, 12)}

    theta_ft = make_random_var(xi, eta, lambda x, y: gcd(x**2, 3*y))

    theta_kn = make_random_var(xi, eta, lambda x, y: lcm(x + 2, x*y))

    table_kn = PrettyTable()
    table_ft = PrettyTable()

    table_kn.add_column("x", list(map(int, theta_kn.keys())))
    table_kn.add_column("p", list(theta_kn.values()))
    table_ft.add_column("x", list(map(int, theta_ft.keys())))
    table_ft.add_column("p", list(theta_ft.values()))

    theta_kn_ft = make_random_var(xi, eta, lambda x, y: lcm(x + 2, x*y)*gcd(x**2, 3*y))

    print(f"Для 8 недели: №1:\n"
          f"Равны ли суммы вероятностей одному у получившихся распределений?\n "
          f"ФТ: {sum(theta_ft.values()) == 1}\n "
          f"КН: {sum(theta_kn.values()) == 1}")

    print(f"a)\n"
          f"Распределение КН:\n{table_kn} \n"
          f"Среднеквадратичное отклонение: {sqrt(compute_variance(theta_kn))}\n"
          f"Медиана: {compute_middle(theta_kn)}\n"
          f"Распределение ФТ:\n{table_ft}\n"
          f"b)\n"
          f"Ковариация: {compute_covariance(theta_kn, theta_ft, theta_kn_ft)}\n"
          f"Корреляция: {compute_correlation(theta_ft, theta_kn, theta_kn_ft)}\n")


    #для задачи на 9 неделю
    xi_eta = {(1, 1) : f(3, 24), (1, 2) : f(2, 24), (1, 3) : f(5, 24),
              (2, 1) : f(2, 24), (2, 2) : f(2, 24), (2, 3) : f(3, 24),
              (3, 1) : f(3, 24), (3, 2) : f(2, 24), (3, 3) : f(2, 24)}
    print(f"Для 9 недели\n"
          f"Энтропия: {compute_entropy([1,2, 3], [1,2,3], xi_eta)}")
