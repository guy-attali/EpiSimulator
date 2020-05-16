def prob_over_time(probability_per_time_step, n_time_steps):
    return 1 - ((1 - probability_per_time_step) ** n_time_steps)
