from math import gcd, pow, sqrt


def lcm(a, b):
    return a * b / gcd(a, b)


def multiply_random(xi, eta):
    result = {}
    for k, v in xi.items():
        for k1, v1 in eta.items():
            if k * k1 in result.keys():
                result[k * k1] += v * v1
            else:
                result[k * k1] = v * v1
    return result

def make_theta(xi, eta):
    result = {}
    for k, v in xi.items():
        for k1, v1 in eta.items():
            new_key = lcm(k, k1)
            if new_key in result.keys():
                result[new_key] += v * v1
            else:
                result[new_key] = v * v1
    return result

def compute_average(random_var: dict, _pow: int = 1):
    result = 0
    for k, v in random_var.items():
        result += pow(k, _pow)*v
    return result


def compute_variance(random_var: dict):
    return compute_average(random_var, 2) - compute_average(random_var)**2


def compute_less_more(keys: list, random_var: dict):
    p = 0
    for key in keys:
        p += random_var[key]
        if p > 0.5 or p == 0.5: return key


def compute_middle(random_var: dict):
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


xi = {1: 1 / 6, 2: 1 / 6, 3: 1 / 6, 4: 1 / 6, 5: 1 / 6, 6: 1 / 6}

eta = {1: 1 / 12, 2: 1 / 12, 3: 1 / 3, 4: 1 / 3, 5: 1 / 12, 6: 1 / 12}

# lcm(xi+2, eta*xi)

xi_plus_two = {k + 2: v for k, v in xi.items()}

eta_multiply_xi = multiply_random(xi, eta)

theta = make_theta(xi_plus_two, eta_multiply_xi)

theta_sigma = sqrt(compute_variance(theta))

theta_middle = compute_middle(theta)

print(f"Среднеквадратичное отклонение: {theta_sigma}\nМедиана: {theta_middle}")
