import equation as eq

diff = eq.Diffusion1D(max_x = 1.5, nx = 50,  max_t=2, nt=100, alpha=0.01, b_val=90.0)



diff.solve()
diff.plot_animation()

