from math import gcd, pow, sqrt


def lcm(a, b):
    return a * b / gcd(a, b)

def make_random(xi, eta, func):
    result = {}
    for k, v in xi.items():
        for k1, v1 in eta.items():
            new_key = func(k, k1)
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

def compute_covariance(xi, eta):
    return compute_average(make_random(xi, eta, lambda x, y: x * y)) - compute_average(xi)*compute_average(eta)

def compute_correlation(xi, eta):
    return compute_covariance(xi, eta)/sqrt(compute_variance(xi)*compute_variance(eta))


xi = {1: 1 / 6, 2: 1 / 6, 3: 1 / 6, 4: 1 / 6, 5: 1 / 6, 6: 1 / 6}

eta = {1: 1 / 12, 2: 1 / 12, 3: 1 / 3, 4: 1 / 3, 5: 1 / 12, 6: 1 / 12}

xi_plus_two = {k + 2: v for k, v in xi.items()}

eta_multiply_xi = make_random(xi, eta, lambda x, y: x*y)

xi_pow_two = {k**2: v for k, v in xi.items()}

three_eta = {3*k: v for k, v in eta.items()}

theta_ft = make_random(xi_pow_two, three_eta, gcd)

theta_kn = make_random(xi_plus_two, eta_multiply_xi, lcm)

theta_kn_sigma = sqrt(compute_variance(theta_kn))

theta_kn_middle = compute_middle(theta_kn)

covariance = compute_covariance(theta_kn, theta_ft)

correlation = compute_correlation(theta_ft, theta_kn)

print(f"Среднеквадратичное отклонение: {theta_kn_sigma}\nМедиана: {theta_kn_middle}\nКовариация: {covariance}\n"
      f"Корреляция: {correlation}")
