# -*- coding: utf-8 -*-

from brainpy._src.math.random import (
  DEFAULT as DEFAULT,
  RandomState as RandomState,
  Generator as Generator,

  seed as seed,
  split_key as split_key,
  default_rng as default_rng,

  # numpy compatibility
  rand as rand,
  randint as randint,
  random_integers as random_integers,
  randn as randn,
  random as random,
  random_sample as random_sample,
  ranf as ranf,
  sample as sample,
  choice as choice,
  permutation as permutation,
  shuffle as shuffle,
  beta as beta,
  exponential as exponential,
  gamma as gamma,
  gumbel as gumbel,
  laplace as laplace,
  logistic as logistic,
  normal as normal,
  pareto as pareto,
  poisson as poisson,
  standard_cauchy as standard_cauchy,
  standard_exponential as standard_exponential,
  standard_gamma as standard_gamma,
  standard_normal as standard_normal,
  standard_t as standard_t,
  uniform as uniform,
  truncated_normal as truncated_normal,
  bernoulli as bernoulli,
  lognormal as lognormal,
  binomial as binomial,
  chisquare as chisquare,
  dirichlet as dirichlet,
  geometric as geometric,
  f as f,
  hypergeometric as hypergeometric,
  logseries as logseries,
  multinomial as multinomial,
  multivariate_normal as multivariate_normal,
  negative_binomial as negative_binomial,
  noncentral_chisquare as noncentral_chisquare,
  noncentral_f as noncentral_f,
  power as power,
  rayleigh as rayleigh,
  triangular as triangular,
  vonmises as vonmises,
  wald as wald,
  weibull as weibull,
  weibull_min as weibull_min,
  zipf as zipf,
  maxwell as maxwell,
  t as t,
  orthogonal as orthogonal,
  loggamma as loggamma,
  categorical as categorical,

  # pytorch compatibility
  rand_like as rand_like,
  randint_like as randint_like,
  randn_like as randn_like,

)
