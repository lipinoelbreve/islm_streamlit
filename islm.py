import streamlit as st
import numpy as np
import plotly.graph_objects as go

def overview_info(users_joined):
    fig = px.line(
        users_joined,
        title="Crecimiento de Usuarios por Fecha",
        x="date_joined",
        y="number_of_users"
    )
    # write to gui
    st.subheader("Información general sobre API")
    st.plotly_chart(fig)

st.title("Modelo Simple IS - LM")

caso = st.sidebar.radio(label='Caso', options=['Keynesiano','Clásico'], index=0)

st.sidebar.header("Parámetros")

with st.sidebar.beta_expander('Mercado de Bienes'):
    A = st.number_input('Consumo Autónomo', min_value = 0.0, value = 20.0, step = 1.0)
    c = st.number_input('Propensión Marginal a Consumir', min_value = 0.0, max_value = 1.0, value = 0.7, step = 0.01)
    H = st.number_input('Inversión Autónoma', min_value = 0.0, value = 15.0, step = 1.0)
    b = st.number_input('Sensibilidad Inversión - Tasa', min_value = 0.0, value = 0.25, step = 0.5)
    G = st.number_input('Gasto Público', min_value = 0.0, value = 17.0, step = 1.0)


with st.sidebar.beta_expander('Mercado de Dinero'):
    M = st.number_input('Oferta de Dinero', min_value = 0.0, value = 250.0, step = 10.0)
    P = st.number_input('Nivel General de Precios', min_value = 0.0, value = 2.0, step = 1.0)
    k = st.number_input('Sensibilidad Demanda de Dinero - Ingreso', min_value = 0.0, value = 50.0, step = 0.5)
    h = st.number_input('Sensibilidad Demanda de Dinero - Tasa', min_value = 0.0, value = 60.0, step = 1.0)

if caso == 'Clásico':
    st.sidebar.subheader('Oferta')
    Ys = st.sidebar.number_input('Oferta Agregada', min_value = 0.0, value = 100.0, step=1.0)

Y_range = np.arange(0,200,10)

IS = (A + H + G - (1-c)*Y_range) / b
LM = (k*Y_range + M/P)/h

gamma = k*b + h*(1-c)
Y_eq = h*(A + H + G)/gamma + b*M/P/gamma
i_eq = (k*Y_eq + M/P)/h

C = A + c*Y_range
I = H - b*i_eq
Yd = C + I + G

i_range = np.arange(0,300,1)
M_d = k*Y_eq - h*i_range

P_range = np.arange(0.01,50,0.5)
Yd_P = h*(A + H + G)/gamma + b*M/P_range/gamma

demanda = go.Figure()
demanda.add_trace(go.Scatter(x=Y_range, y=Yd, mode='lines', name='Demanda', line=dict(width=4)))
demanda.add_trace(go.Scatter(x=Y_range, y=Y_range, mode='lines', name="Yd = Ys", line=dict(width=4)))
demanda.update_layout(
    width=535,
    yaxis_range=[0,200],
    xaxis_range=[0,200],
    title='Mercado de Bienes'
    )
demanda.update_xaxes(title_text='Ys')
demanda.update_yaxes(title_text='Yd')

islm = go.Figure()
islm.add_trace(go.Scatter(x=Y_range, y=IS, mode='lines', name='IS', line=dict(width=4)))
islm.add_trace(go.Scatter(x=Y_range, y=LM, mode='lines', name="LM", line=dict(width=4)))
islm.update_layout(
    width=500,
    yaxis_range=[0,200],
    xaxis_range=[0,200],
    title='IS - LM'
    )
islm.update_xaxes(title_text='Y')
islm.update_yaxes(title_text='i')

dinero = go.Figure()
dinero.add_trace(go.Scatter(x=M_d, y=i_range, mode='lines', name='Md', line=dict(width=4)))
dinero.add_trace(go.Scatter(x=[M/P]*len(M_d), y=i_range, mode='lines', name='Ms', line=dict(width=4)))
dinero.update_layout(
    width=500,
    yaxis_range=[0,200],
    xaxis_range=[0,200],
    title='Mercado de Dinero'
    )
dinero.update_xaxes(title_text='m')
dinero.update_yaxes(title_text='i')

oferta_demanda = go.Figure()
oferta_demanda.add_trace(go.Scatter(x=Yd_P, y=P_range, mode='lines', name='DA', line=dict(width=4)))
oferta_demanda.add_trace(go.Scatter(x=Y_range, y=[P]*len(Yd_P), mode='lines', name='OA', line=dict(width=4)))
oferta_demanda.update_layout(
    width=500,
    yaxis_range=[0,10],
    xaxis_range=[0,200],
    title='Demanda & Oferta Agregadas'
    )
oferta_demanda.update_xaxes(title_text='Y')
oferta_demanda.update_yaxes(title_text='P')

st.subheader("nicolupi.2@gmail.com - github.com/lipinoelbreve")

col1, _ = st.beta_columns([2,1])
col1.plotly_chart(demanda, use_column_width=True)

col1, col2 = st.beta_columns([2,1])
col1.plotly_chart(islm, use_column_width=True)
col2.plotly_chart(dinero, use_column_width=True)

col1, _ = st.beta_columns([2,1])
col1.plotly_chart(oferta_demanda, use_column_width=True)