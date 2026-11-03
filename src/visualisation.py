import matplotlib.pyplot as plt

def plot_series(data, x, y, title, ylabel):
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(data[x], data[y], linewidth=1.6)
    ax.set(title=title, xlabel="Reporting date", ylabel=ylabel)
    ax.grid(alpha=.25)
    fig.tight_layout()
    return fig
