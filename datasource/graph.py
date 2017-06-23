from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file
from itertools import izip


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)


def draw_graph(ticker, df, lines):
    df["date"] = pd.to_datetime(df.index)

    inc = df.trend == 1
    dec = df.trend == -1
    w = 12*60*60*1000 # half day in ms

    df['open'] = df['high']
    df['close'] = df['low']

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = ticker + " Candlestick")
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3

    p.segment(df.date, df.high, df.date, df.low, color="black")
    p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="red")

    # p.line(df.date[inc], df.open[inc], line_width=3)

    x = []
    y = []
    for start, end in pairwise(lines):
        start_time, start_price = start
        end_time, end_price = end
        x.append([start_time, end_time])
        y.append([start_price, end_price])
    p.multi_line(x, y, line_width=3)

    output_file("candlestick.html", title="candlestick.py example")

    show(p)
