import streamlit as st
import math

st.title('Оптический калькулятор')
pixel_horizontal = st.number_input('Пикселей в матрице по горизонтали [шт]', min_value=1, max_value=10000, value=1920, step=1)
pixel_size = st.number_input('Размер пиксела [мкм]', min_value=0.01, max_value=100.0, value=3.45, step=0.01)
target_size = st.number_input('Размер цели [м]', min_value=0.01, max_value=1000.0, value=0.2, step=0.01)
threshold_pixel_count = st.number_input('Сколько пикселей должна занимать цель [шт]', min_value=1, max_value=10000, value=12, step=1)
distance = st.number_input('Требуемая дальность [м]', min_value=1, max_value=99999, value=1000, step=1)
pixel_size = pixel_size / 1000000
focus = (pixel_size * threshold_pixel_count * distance) / target_size
field = 2 * math.atan((pixel_horizontal * pixel_size) / (2 * focus))
field = round(math.degrees(field), 1)
col1, col2 = st.columns(2)
with col1:
    st.markdown('Угловое поле')
    st.subheader(str(field) + '°')
with col2:
    st.markdown('Фокусное расстояние')
    st.subheader(str(round(focus * 1000, 2)) + ' мм')