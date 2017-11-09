import site
site.addsitedir(r'C:\Users\Ciaran\Documents\pycotools')
from pycotools import model, viz, tasks
import os


"""
The Lotka Volterra System
=========================

\begin{equation}
    \begin{aligned}
    \frac{d[X]}{dt} &= \alpha \cdot X - \beta \cdot X \cdot Y
    \frac{d[Y]}{dt} &= - \gamma \cdot Y + \delta \cdot X \cdot Y
    \end{aligned}
\end{equation}

where:

\begin{equation}
    \begin{aligned}
    X_0 = 
    Y_0 = 
    \end{aligned}
\end{equation}

and 

\begin{equation}
    \begin{aligned}
        \alpha &= 1.5
        \beta  &= 1
        \gamma &= 3
        \delta = & 1
    \end{aligned}
\end{equation}

"""

cps_file = r'C:\Users\Ciaran\Documents\pycotools\docs\source\Examples\LotkaVolterra.cps'
if os.path.isfile(cps_file):
    os.remove(cps_file)

with model.Build(cps_file) as m:
    m.name = 'LotkaVolterra'
    X = model.Reaction(m, 'X', '-> X ; Y', 'alpha*X - beta*X*Y')
    Y = model.Reaction(m, 'Y', '-> Y ; X', '-gamma*Y + delta*X*Y')

    m.add('reaction', X)
    m.add('reaction', Y)


lotka = model.Model(cps_file)

model.InsertParameters(lotka, parameter_dict={
    '(X).alpha': 1.5,
    '(X).beta': 1,
    '(Y).gamma': 3,
    '(Y).delta': 1
})
# lotka.open()

TC = tasks.TimeCourse(
    lotka, end=100, intervals=0.0001*100, step_size=0.0001
)


viz.PlotTimeCourse(
    TC, show=True, separate=True
)


















