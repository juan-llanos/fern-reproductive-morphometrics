# src/plotting.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath
from matplotlib import colors, cm


def heatmap_frond_ax(individual_id, ax, df_source, is_imputed=False, is_knn_neighbor=False):
    """
    Draws the reproductive map (sori-per-row heatmap) of an individual
    on a given axis (ax), using data from df_source.

    Parameters
    ----------
    individual_id : str
        individual_id to plot (e.g. "H15").
    ax : matplotlib.axes.Axes
        Axis to draw on.
    df_source : pd.DataFrame
        Table with columns individual_id, row_id, n_sori_per_row.
    is_imputed : bool
        If True, highlights the panel as an imputed value (gold border/title).
    is_knn_neighbor : bool
        If True, highlights the panel as a KNN neighbor (blue border/title).
    """
    d = df_source[df_source["individual_id"] == individual_id].sort_values("row_id", ascending=True)
    sori_counts = d["n_sori_per_row"].values
    num_levels = len(sori_counts)

    df_mapping = pd.DataFrame({
        'Level': np.arange(1, num_levels + 1),
        'Sori_Count': sori_counts
    })

    cmap = plt.get_cmap('YlOrRd')
    cmap.set_under('whitesmoke')
    norm = colors.Normalize(vmin=0.1, vmax=64)

    rachis_width = 0.12
    max_base_length = 5.0

    ax.plot([0, 0], [0, num_levels + 2], color='#5c3a21', linewidth=3, zorder=1)

    def add_pinna(ax, level, length, color, side=1):
        tip_y = level + 0.3
        path_data = [
            (mpath.Path.MOVETO, (side * rachis_width, level)),
            (mpath.Path.CURVE3, (side * length * 0.4, level + 0.7)),
            (mpath.Path.CURVE3, (side * length, tip_y)),
            (mpath.Path.CURVE3, (side * length * 0.4, level - 0.2)),
            (mpath.Path.CURVE3, (side * rachis_width, level)),
        ]
        codes, verts = zip(*path_data)
        path = mpath.Path(verts, codes)
        patch = mpatches.PathPatch(path, facecolor=color, edgecolor='#1a1a1a',
                                    lw=0.5, alpha=0.9, zorder=2)
        ax.add_patch(patch)

    for i, row in df_mapping.iterrows():
        level = row['Level']
        sori_row = row['Sori_Count']
        pinna_color = cmap(norm(sori_row))
        pinna_length = max_base_length * (1 - (level / (num_levels + 1)) ** 0.7)
        if pinna_length > 0.1:
            add_pinna(ax, level, pinna_length, pinna_color, side=1)
            add_pinna(ax, level, pinna_length, pinna_color, side=-1)

    ax.set_xlim(-7, 7)
    ax.set_ylim(-2, num_levels + 4)
    ax.set_aspect('equal')
    ax.axis('off')

    if is_imputed:
        title = f'{individual_id} (imputed)'
        title_color = '#ffcc66'
    elif is_knn_neighbor:
        title = f'{individual_id} (KNN neighbor)'
        title_color = '#7ec8e3'
    else:
        title = individual_id
        title_color = 'white'
    ax.set_title(title, fontsize=11, fontweight='bold', color=title_color)

    if is_imputed or is_knn_neighbor:
        border_color = '#ffcc66' if is_imputed else '#7ec8e3'
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(border_color)
            spine.set_linewidth(2.5)


def heatmap_frond(individual_id, df_source):
    """Draws a single individual on its own figure, with a color bar."""
    sori_counts = df_source.loc[df_source["individual_id"] == individual_id, "n_sori_per_row"].values
    num_levels = len(sori_counts)

    fig, ax = plt.subplots(figsize=(10, 18), facecolor="black")
    cmap = plt.get_cmap('YlOrRd')
    cmap.set_under('whitesmoke')
    norm = colors.Normalize(vmin=0.1, vmax=64)

    heatmap_frond_ax(individual_id, ax, df_source)

    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.04, extend='min')
    cbar.set_label('Sori Count per Row', rotation=270, labelpad=20, fontsize=12, color="white")
    cbar.set_ticks([0.1, 10, 20, 30, 40, 50, 60])
    cbar.set_ticklabels(['0', '10', '20', '30', '40', '50', '60'])
    cbar.ax.tick_params(labelcolor='white', color='white')
    cbar.outline.set_edgecolor('white')

    fig.suptitle(f'REPRODUCTIVE MAP: {individual_id}\nSori Distribution ({num_levels} levels)',
                 fontsize=14, fontweight='bold', color='#1B4D3E', y=0.995)

    plt.tight_layout()
    plt.show()