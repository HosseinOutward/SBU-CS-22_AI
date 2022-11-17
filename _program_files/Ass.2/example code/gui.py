import plotly.express as px
import numpy as np


class Graphics:
    def __init__(self): pass

    def display(self, env):
        flat=np.array(env.stick_together).flatten()
        color=np.zeros(env.coordinates.shape[0])
        color[flat]=1

        flat=list(flat)
        for i, (a,b) in enumerate(zip(env.stick_together[:-1], env.stick_together[1:])):
            a=[a[0]+1, a[1]+1]; b=[b[0]+1, b[1]+1]
            if a[1]+1!=b[0]: continue
            s=b[0]-1
            r=flat.index(s)
            while flat[r-1]==flat[r] or flat[r-1]+1==flat[r]: r+=1
            color[flat[flat.index(s):r]] = (color[s]%2)+1



        fig = px.line_3d(x=env.coordinates[:, 0], y=env.coordinates[:, 1],
                         z=env.coordinates[:, 2])
        fig = fig.add_scatter3d(x=env.coordinates[:, 0], y=env.coordinates[:, 1],
                         z=env.coordinates[:, 2], mode='markers', marker_color=color)

        max_v=env.coordinates.max(); min_v=env.coordinates.min()
        fig.update_layout(scene=dict(
            xaxis=dict(nticks=4, range=[min_v-0.5, max_v+0.5],),
            yaxis=dict(nticks=4, range=[min_v-0.5, max_v+0.5],),
            zaxis=dict(nticks=4, range=[min_v-0.5, max_v+0.5],)
        ))

        fig.show()
