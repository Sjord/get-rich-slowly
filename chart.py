import json
import sys
import pygal

fn = sys.argv[1]
with open(fn) as f:
    data = json.load(f)

chart = pygal.Line()
chart.x_labels = [d['date'] for d in data['prices']]
chart.add(fn, [d['price'] for d in data['prices']])
chart.render_to_file('out.svg')

