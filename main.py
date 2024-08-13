import streamlit as st
import math
import json

# Opening JSON file with matrix types
f = open('data.json')
data = json.load(f)
f.close()

# Adjust width of page
css='''
<style>
    section.main > div {max-width:55rem}
</style>
'''
st.markdown(css, unsafe_allow_html=True)


st.title('Оптический калькулятор')

st.markdown('''Расчёт фокусного расстояния объектива для заданной матрицы, размера цели, критерия наблюдения (обнаружение, распознавание) и дальности наблюдения.\n
Угловое поле расчитывается исходя из получившегося фокусного расстояния и заданой матрицы.''')

st.image('shema.jpg',)

st.subheader('Входные данные')

col_matrix_type, col_select_tool, col_data = st.columns([1,1.2,1.9])

matrix_types = list(data)
with col_matrix_type:
    matrix_type = st.radio('Выберите тип матрицы', matrix_types, index=0)
with col_select_tool:
    matrixes = list(data[matrix_type])

    if matrix_type == 'Своя':
        matrix_args_enable = False
    else:
        matrix_args_enable = True

    matrix = st.selectbox('Выберите матрицу', options=matrixes, index=0,
                disabled=not matrix_args_enable, placeholder='Выберите матрицу')
    resolution = st.selectbox('Выберите разрешение', options=data[matrix_type][matrix], index=0,
                 disabled=not matrix_args_enable or len(data[matrix_type][matrix]) == 1, placeholder='Выберите разрешение')



with col_data:
    if matrix_args_enable:
        pixel_horizontal = int(resolution.split()[0])
        pixel_size = float(list(data[matrix_type][matrix][resolution])[0])

    else:
        pixel_horizontal = 1920
        pixel_size = 3.45
    st.number_input('Количество пикселей в матрице по горизонтали [шт] (n)', min_value=1, max_value=10000, value=pixel_horizontal, step=1, disabled=matrix_args_enable)
    st.number_input('Размер пиксела [мкм] (ax)', min_value=0.01, max_value=100.0, value=pixel_size, step=0.01, disabled=matrix_args_enable)
target_size = st.number_input('Размер цели [м] (h)', min_value=0.01, max_value=1000.0, value=0.2, step=0.01)
threshold_pixel_count = st.number_input('Сколько пикселей должна занимать цель на матрице [шт]', min_value=1, max_value=10000, value=12, step=1)
distance = st.number_input('Требуемая дальность [м] (L)', min_value=1, max_value=99999, value=1000, step=1)
pixel_size = pixel_size / 1000000
focus = (pixel_size * threshold_pixel_count * distance) / target_size
field = 2 * math.atan((pixel_horizontal * pixel_size) / (2 * focus))
field = round(math.degrees(field), 1)
st.subheader('Расчитанные данные')
col_focus, col_field = st.columns(2)
with col_focus:
    st.markdown('Фокусное расстояние (f)')
    st.subheader(str(round(focus * 1000, 2)) + ' мм')
with col_field:
    st.markdown('Угловое поле по горизонтали(w)')
    st.subheader(str(field) + '°')