#!/usr/bin/env python3

import sys
import math
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " RESULT_ROOT_DIR")
        sys.exit(-1)

res_root_dir = sys.argv[1]

DEFAULT_PLOT = {
    "markersize": 12.0,
    "markeredgewidth": 2.6,
    "markevery": 1,
    "linewidth": 2.6,
}

plt.rcParams["font.size"] = 14

# Configure grid
plt.grid(axis='y')

### plot TPCC ###
res_csv = res_root_dir + "/tpcc/tpcc.csv"

# Read the CSV file into a Pandas DataFrame
res_df = pd.read_csv(res_csv)

# Extract the data
x = res_df["Remote_Ratio"]

tigon_y = res_df["Tigon"]
sundial_cxl_improved_y = res_df["Sundial-CXL-improved"]
twopl_cxl_improved_y = res_df["TwoPL-CXL-improved"]
motor_y = res_df["Motor"]

plt.xlabel("Multi-partition Transaction Percentage")
plt.ylabel("Throughput (txns/sec)")

# Configure axis range
tmp_list = list()
tmp_list.extend(tigon_y)
tmp_list.extend(sundial_cxl_improved_y)
tmp_list.extend(twopl_cxl_improved_y)
tmp_list.extend(motor_y)

max_y = max(tmp_list)
max_y_rounded_up = math.ceil(max_y / 200000.0) * 200000.0
plt.ylim(0, max_y_rounded_up)

# Transform Y axises
ax = plt.subplot(111)
plt.ylim(0, 800000)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/1000) + 'K' if x != 0 else 0))

# Create the line plot
plt.plot(x, tigon_y, color="#000000", marker="s", **DEFAULT_PLOT, label="Tigon")
plt.plot(x, sundial_cxl_improved_y, color="#4372c4", marker="^", **DEFAULT_PLOT, markerfacecolor="none", label="Sundial+")
plt.plot(x, twopl_cxl_improved_y, color="#ffc003", marker=">", **DEFAULT_PLOT, markerfacecolor="none", label="DS2PL+")
plt.plot(x, motor_y, color="#ed7d31", marker="o", **DEFAULT_PLOT, markerfacecolor="none", label="Motor")

# Configure legend
legend = ax.legend(loc='upper right', bbox_to_anchor=(1.019, 1.026), columnspacing=1, frameon=True, fancybox=False, framealpha=1, ncol=2, edgecolor='black')
legend.get_frame().set_linewidth(0.7)

plt.savefig(res_root_dir + "/tpcc/tpcc.pdf", format="pdf", bbox_inches="tight")
