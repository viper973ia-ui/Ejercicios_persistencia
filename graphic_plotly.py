from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

fig = make_subplots(rows=2, cols=2,
    subplot_titles=['Línea', 'Barras', 'Scatter', 'Pie'])

x = np.linspace(0, 10, 50)
fig.add_trace(go.Scatter(x=x, y=np.sin(x), line=dict(color='#7C3AED')), row=1, col=1)
fig.add_trace(go.Bar(x=['A','B','C'], y=[20,35,25], marker_color='#14B8A6'), row=1, col=2)
fig.add_trace(go.Scatter(x=np.random.randn(50), y=np.random.randn(50),
              mode='markers', marker=dict(color='#F97316')), row=2, col=1)
fig.add_trace(go.Pie(values=[40,30,20,10], labels=['A','B','C','D']), row=2, col=2)
fig.update_layout(showlegend=False, height=600)
fig.show()