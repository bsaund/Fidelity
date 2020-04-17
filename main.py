import utils as ut
from datetime import timedelta
print("Running...")

# ut.plot_puts_graphs_overlay('SPY')

# ut.plot_puts_percentage_gain('SPY', timedelta(days=30))
# ut.plot_calls_percentage_gain('SPY', timedelta(days=30))
ut.plot_options_percentage_gain('SPY', timedelta(days=30))

