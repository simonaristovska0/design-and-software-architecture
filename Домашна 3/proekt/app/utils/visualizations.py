import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def plot_gauge(signal_counts, title, ax):
    """
    Create a gauge chart for sentiment analysis.
    :param signal_counts: Dictionary with counts for 'Buy', 'Neutral', and 'Sell'.
    :param title: Title of the gauge.
    :param ax: Matplotlib Axes object.
    """
    # Define the categories and their colors
    categories = ['Strong sell', 'Sell', 'Neutral', 'Buy', 'Strong buy']
    colors = ['darkred', 'red', 'gray', 'violet', 'purple']
    num_categories = len(categories)

    # Normalize signal counts
    total_signals = sum(signal_counts.values())
    if total_signals == 0:
        needle_position = 2  # Default to neutral
    else:
        weighted_sum = (signal_counts.get('Sell', 0) * 1 +
                        signal_counts.get('Neutral', 0) * 2 +
                        signal_counts.get('Buy', 0) * 3)
        needle_position = weighted_sum / total_signals

    # Create the gauge background using wedges
    start_angle = -90
    segment_angles = 180 / num_categories

    for i in range(num_categories):
        if i >= num_categories // 2:  # Color only the right half
            end_angle = start_angle + segment_angles
            ax.pie([1],
                   startangle=start_angle,
                   radius=1.0,
                   colors=[colors[i]],
                   wedgeprops=dict(width=0.3, edgecolor='white'))
            start_angle = end_angle
        else:
            start_angle += segment_angles

    # Add category labels
    label_angles = np.linspace(-90, 90, num_categories)
    for i, angle in enumerate(label_angles):
        ax.text(np.cos(np.radians(angle)) * 1.2, np.sin(np.radians(angle)) * 1.2,
                categories[i], ha='center', va='center', fontsize=10, color=colors[i])

    # Add the needle
    needle_angle = -90 + (needle_position - 1) * (180 / (num_categories - 1))
    ax.arrow(0, 0, 0.8 * np.cos(np.radians(needle_angle)),
             0.8 * np.sin(np.radians(needle_angle)),
             width=0.02, head_width=0.05, head_length=0.1, fc='black', ec='black')

    # Add the title and signal counts
    ax.text(0, -1.5, title, fontsize=14, fontweight='bold', ha='center')
    ax.text(-0.7, -1.9, f"Sell: {signal_counts.get('Sell', 0)}", fontsize=10, color='red', ha='center')
    ax.text(0.7, -1.9, f"Buy: {signal_counts.get('Buy', 0)}", fontsize=10, color='violet', ha='center')

    ax.axis('equal')

def plot_signals_table(df, ax):
    print("Table Data:", df)
    """
    Display a table of indicators and their signals with full indicator names,
    handling NaN values with a custom message.
    :param df: DataFrame containing indicator values and signals.
    :param ax: Matplotlib Axes object.
    """
    # Define a mapping of short indicator names to full indicator names
    indicator_name_mapping = {
        'RSI': 'Relative Strength Index (14)',
        'Stochastic %K': 'Stochastic %K',
        'CCI': 'Commodity Channel Index (20)',
        'ADX': 'Average Directional Index (14)',
        'SMA': 'Simple Moving Average (10)',
        'EMA': 'Exponential Moving Average (10)',
        'WMA': 'Weighted Moving Average (10)',
        'HMA': 'Hull Moving Average (10)',
        'Median Price': 'Typical Price (Median Price)',
        'ROC': 'Rate of Change (10)'
    }

    # Prepare table data
    table_data = []
    for _, row in df.iterrows():
        # Replace short names with full names
        full_name = indicator_name_mapping.get(row['Indicator'], row['Indicator'])  # Default to original name if not found
        value = round(row['Value'], 2) if not pd.isna(row['Value']) else 'Not Available'  # Replace NaN with custom message
        signal = row['Signal']
        table_data.append([full_name, value, signal])

    if not table_data:
        ax.axis('off')
        return

    # Define column labels
    column_labels = ["Indicator", "Value", "Signal"]

    # Create and format the table
    ax.axis('off')
    table = ax.table(
        cellText=table_data,
        colLabels=column_labels,
        loc='center',
        cellLoc='center',
        colWidths=[0.5, 0.2, 0.2]  # Adjust column widths
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)  # Adjust font size for better readability
    table.scale(1.5, 1.5)  # Scale the table to make it larger


def generate_dashboard(signal_data, gauge_titles):
    """
    Generate a full dashboard with gauges and separate tables.
    :param signal_data: List of dictionaries containing signal counts and dataframes.
    :param gauge_titles: Titles for the gauge charts.
    """
    fig, axs = plt.subplots(2, len(signal_data), figsize=(8 * len(signal_data), 12), gridspec_kw={'height_ratios': [3, 2]})

    # Ensure axs is always a 2D array
    if len(signal_data) == 1:
        axs = np.array([[axs[0]], [axs[1]]])

    # Gauges
    # for i, data in enumerate(signal_data):
    #     plot_gauge(data['signal_counts'], gauge_titles[i], axs[0, i])
    #
    # # Separate tables
    # for i, data in enumerate(signal_data):
    #     plot_signals_table(data['details'], axs[1, i])

    # Ensure 'results' is used directly for charts and tables
    for i, data in enumerate(signal_data):
        plot_gauge(data['signal_counts'], gauge_titles[i], axs[0, i])
        plot_signals_table(data['details'], axs[1, i])


    plt.tight_layout()
    plt.show()

def generate_summary(results):
    """
    Generate a summary dictionary based on results.
    """
    summary = {"oscillators": {"Buy": 0, "Neutral": 0, "Sell": 0},
               "movingAverages": {"Buy": 0, "Neutral": 0, "Sell": 0}}

    oscillator_names = [
        "Relative Strength Index (RSI)",
        "Stochastic %K",
        "Commodity Channel Index (CCI)",
        "Average Directional Index (ADX)",
        "Rate of Change (ROC)"
    ]
    moving_average_names = [
        "Simple Moving Average (SMA)",
        "Exponential Moving Average (EMA)",
        "Weighted Moving Average (WMA)",
        "Hull Moving Average (HMA)",
        "Typical Price (Median Price)"
    ]

    for result in results:
        if result["Name"] in oscillator_names:
            summary["oscillators"][result["Action"]] += 1
        elif result["Name"] in moving_average_names:
            summary["movingAverages"][result["Action"]] += 1

    return summary


def generate_gauge(signal_counts, title, sentiment):
    """
    Generate a gauge chart for sentiment analysis.
    :param signal_counts: Dictionary with counts for 'Sell', 'Neutral', and 'Buy'.
    :param title: Title of the gauge.
    :param sentiment: Current sentiment (e.g., 'Sell', 'Buy', 'Neutral').
    :return: Base64-encoded image of the gauge.
    """
    categories = ['Strong sell', 'Sell', 'Neutral', 'Buy', 'Strong buy']
    colors = ['#FF0000', '#FF6666', '#CCCCCC', '#6666FF', '#0000FF']
    needle_position = categories.index(sentiment)

    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.5, 1.5)

    # Draw gauge segments
    for i in range(len(categories)):
        ax.fill_between(
            [i / 2 - 1, (i + 1) / 2 - 1],
            [0, 0],
            [1, 1],
            color=colors[i],
            alpha=0.5,
        )

    # Draw needle
    angle = (needle_position - 2) * 45
    ax.arrow(
        0, 0, np.sin(np.radians(angle)), np.cos(np.radians(angle)),
        width=0.05, head_width=0.1, head_length=0.2, fc='black', ec='black'
    )

    # Add title and category labels
    ax.text(0, -0.5, title, ha='center', va='center', fontsize=14, fontweight='bold')
    for i, category in enumerate(categories):
        angle = (i - 2) * 45
        ax.text(
            np.sin(np.radians(angle)) * 1.1,
            np.cos(np.radians(angle)) * 1.1,
            category,
            ha='center',
            va='center',
            fontsize=10,
        )

    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return image_base64
