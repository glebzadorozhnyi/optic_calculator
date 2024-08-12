import streamlit as st
import math

st.title('Оптический калькулятор')
st.markdown('''Расчёт фокусного расстояния объектива для заданной матрицы, размера цели, критерия наблюдения (обнаружение, распознавание) и дальности наблюдения.\n
Угловое поле расчитывается исходя из получившегося фокусного расстояния и заданой матрицы.''')

st.image('shema.jpg', width=700)
st.subheader('Входные данные')
pixel_horizontal = st.number_input('Количество пикселей в матрице по горизонтали [шт] (n)', min_value=1, max_value=10000, value=1920, step=1)
pixel_size = st.number_input('Размер пиксела [мкм] (ax)', min_value=0.01, max_value=100.0, value=3.45, step=0.01)
target_size = st.number_input('Размер цели [м] (h)', min_value=0.01, max_value=1000.0, value=0.2, step=0.01)
threshold_pixel_count = st.number_input('Сколько пикселей должна занимать цель на матрице [шт]', min_value=1, max_value=10000, value=12, step=1)
distance = st.number_input('Требуемая дальность [м] (L)', min_value=1, max_value=99999, value=1000, step=1)
pixel_size = pixel_size / 1000000
focus = (pixel_size * threshold_pixel_count * distance) / target_size
field = 2 * math.atan((pixel_horizontal * pixel_size) / (2 * focus))
field = round(math.degrees(field), 1)
st.subheader('Расчитанные данные')
col1, col2 = st.columns(2)
with col1:
    st.markdown('Угловое поле (w)')
    st.subheader(str(field) + '°')
with col2:
    st.markdown('Фокусное расстояние (f)')
    st.subheader(str(round(focus * 1000, 2)) + ' мм')