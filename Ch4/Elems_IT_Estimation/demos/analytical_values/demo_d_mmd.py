#!/usr/bin/env python3

""" Demo for maximum mean discrepancy (MMD) estimators.

Analytical vs estimated value is illustrated for normal random variables.

"""

from numpy.random import rand, multivariate_normal
from numpy import arange, zeros, ones
from scipy import dot
import matplotlib.pyplot as plt

from ite.cost.x_factory import co_factory
from ite.cost.x_analytical_values import analytical_value_d_mmd
from ite.cost.x_kernel import Kernel


def main():
    # parameters:
    dim = 1  # dimension of the distribution
    num_of_samples_v = arange(100, 3 * 1000 + 1, 100)
    cost_name = 'BDMMD_UStat'  # dim >= 1
    # cost_name = 'BDMMD_VStat'  # dim >= 1
    # cost_name = 'BDMMD_UStat_IChol'  # dim >= 1
    # cost_name = 'BDMMD_VStat_IChol'  # dim >= 1

    # initialization:
    distr = 'normal'  # fixed
    num_of_samples_max = num_of_samples_v[-1]
    length = len(num_of_samples_v)
    d_hat_v = zeros(length)  # vector of estimated divergence values

    # RBF kernel (sigma = std / bandwith parameter):
    kernel = Kernel({'name': 'RBF', 'sigma': 1})
    # polynomial kernel (quadratic / cubic; c = offset parameter = 1):
    # kernel = Kernel({'name': 'polynomial', 'exponent': 2, 'c': 1})
    # kernel = Kernel({'name': 'polynomial', 'exponent': 3, 'c': 1})

    co = co_factory(cost_name, mult=True, kernel=kernel)  # cost object

    # distr, dim -> samples (y1<<y2), distribution parameters (par1,par2), 
    # analytical value (d):
    if distr == 'normal':
        # mean (m1,m2):
        m1 = rand(dim)
        m2 = rand(dim)

        # (random) linear transformation applied to the data (l1,l2) ->
        # covariance matrix (c1,c2):
        l2 = rand(dim, dim)
        l1 = rand(dim, dim)
        c1 = dot(l1, l1.T)
        c2 = dot(l2, l2.T)

        # generate samples (y1~N(m1,c1), y2~N(m2,c2)):
        y1 = multivariate_normal(m1, c1, num_of_samples_max)
        y2 = multivariate_normal(m2, c2, num_of_samples_max)

        par1 = {"mean": m1, "cov": c1}
        par2 = {"mean": m2, "cov": c2}

    else:
        raise Exception('Distribution=?')        
    
    d = analytical_value_d_mmd(distr, distr, kernel, par1, par2)
    
    # estimation:
    for (tk, num_of_samples) in enumerate(num_of_samples_v):
        d_hat_v[tk] = co.estimation(y1[0:num_of_samples],
                                    y2[0:num_of_samples])  # broadcast
        print("tk={0}/{1}".format(tk+1, length))
    
    # plot:    
    plt.plot(num_of_samples_v, d_hat_v, num_of_samples_v, ones(length)*d)
    plt.xlabel('Number of samples')
    plt.ylabel('MMD')
    plt.legend(('estimation', 'analytical value'), loc='best')
    plt.title("Estimator: " + cost_name)
    plt.show()


if __name__ == "__main__":
    main()
