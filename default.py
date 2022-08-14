Diffusion_default = {
'Initial condition:': 0.01,
'Number of Cells (nx):': 50,
'x_max:': 1.5,
'Boundary value at x0:': 100.0,
'Number cycles:': 100,
'Final time:': 3,
'Alpha:': 0.01
}

subPAD = 2
subPAD_out = 2

# Assertion checks Variables.
max_t_min = 0
nt_min = 30
nt_max = 20000
max_ratio = 150
max_x_min = 0
nx_min = 30
nx_max = 1000
wave_vector_sigma_max_gauss_wave = 5
wave_vector_sigma_max_sin_sinc_wave = 15
wave_vector_sigma_max_gauss_sh = 5
wave_vector_sigma_max_sin_sinc_sh = 10
velocity_min = 0
velocity_max = 0.01
phase_mu_max = 15
amplitude_max = 100
amplitude_min = 0
min_ratio_time_dif = 20
min_ratio_dif = 20
max_ratio_dif = 50
nt_max_dif = 400
nt_min_dif = 10
max_t_min_dif = 1
b_val_min = 1
b_val_max = 1000
alpha_min = 0.001
alpha_max = 0.01
nx_max_dif = 2000
nx_min_dif = 10
init_val_min = 0
stability_wave_lower_bound = 0
stability_wave_upper_bound = 1

# Dictionaries for default values.
default_Schrodinger_dict = {'nx': 400, 'x_max': 20, 'nt': 400, 't_max': 5}
default_wave_dict = {'nx': 100, 'x_max': 10, 'nt': 500, 't_max': 30, 'velocity': 0.006}
default_heat_dict = {'init': 0.01, 'nx': 50, 'x_max': 1.5, 'b_val': 100.0, 'nt': 100, 't_max': 3, 'alpha': 0.01}
default_init_condition = {'amplitude': 10, 'phase/sigma': 1, 'wave_vector/mu': -5}
