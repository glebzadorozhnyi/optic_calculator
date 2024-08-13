import streamlit as st
import math
import json
# Opening JSON file with matrix types
f = open('data.json')
data = json.load(f)
f.close()
f = open('criteria.json')
criterias = list(json.load(f))
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

col_matrix_type, col_select_tool, col_data = st.columns([1,1.9,1.2])

matrix_types = list(data)
with col_matrix_type:
    matrix_type = st.radio('Выберите тип матрицы', matrix_types, index=0)
with col_select_tool:
    matrixes = list(data[matrix_type])

    if matrix_type == 'Своя':
        matrix_args_enable = False
        pixel_horizontal = st.number_input('Количество пикселей в матрице по горизонтали [шт] (n)', min_value=1, max_value=10000, value=1920, step=1, disabled=False)
        pixel_vertical = st.number_input('Количество пикселей в матрице по вертикали [шт] (n)', min_value=1, max_value=10000, value=1080, step=1, disabled=matrix_args_enable)
    else:
        matrix_args_enable = True

        matrix = st.selectbox('Выберите матрицу', options=matrixes, index=0,
                    disabled=not matrix_args_enable, placeholder='Выберите матрицу')
        resolution = st.selectbox('Выберите разрешение', options=data[matrix_type][matrix], index=0,
                     disabled=not matrix_args_enable or len(data[matrix_type][matrix]) == 1, placeholder='Выберите разрешение')



with col_data:

    if matrix_args_enable:
        pixel_horizontal = int(resolution.split()[0])
        pixel_vertical = int(resolution.split()[2])
        pixel_size = float(list(data[matrix_type][matrix][resolution])[0])
        st.number_input('Размер пиксела [мкм] (ax)', min_value=0.01, max_value=100.0, value=pixel_size, step=0.01, disabled=True, key='pixel_size')
    else:
        pixel_size = st.number_input('Размер пиксела [мкм] (ax)', min_value=0.01, max_value=100.0, value=3.45, step=0.01, disabled=False, key='pixel_size2')

target_size = st.number_input('Размер цели [м] (h)', min_value=0.01, max_value=1000.0, value=0.2, step=0.01)
col_criteria, col_threshold = st.columns(2)

with col_criteria:
    criteria = st.selectbox('Выберите критерий', options=criterias, index=0, disabled=not matrix_args_enable, placeholder='Выберите матрицу', key='threshold_enable')

with col_threshold:
    if criteria == 'Свой':
        threshold_pixel_count_init = 12
    else:
        threshold_pixel_count_init = int(criteria.split()[1])
    threshold_pixel_count = st.number_input('Сколько пикселей должна занимать цель на матрице [шт]', min_value=1, max_value=10000, value=threshold_pixel_count_init, step=1, disabled=st.session_state.threshold_enable != 'Свой')

distance = st.number_input('Требуемая дальность [м] (L)', min_value=1, max_value=99999, value=1000, step=1)
pixel_size = pixel_size / 1000000
focus = (pixel_size * threshold_pixel_count * distance) / target_size
field_h = 2 * math.atan((pixel_horizontal * pixel_size) / (2 * focus))
field_v = 2 * math.atan((pixel_vertical * pixel_size) / (2 * focus))
field_h = round(math.degrees(field_h), 1)
field_v = round(math.degrees(field_v), 1)
st.subheader('Расчитанные данные')
col_focus, col_field, col_resolving_power_lines, col_resolving_power_minutes = st.columns(4)
with col_focus:
    st.markdown('Фокусное расстояние (f)')
    st.markdown('### ' + str(round(focus * 1000, 1)) + ' мм')
with col_field:
    st.markdown('Угловое поле (w)')
    st.markdown('### ' + str(field_h) + '° х ' + str(field_v) + '°')
with col_resolving_power_lines:
    st.markdown('Разрешающая способность')
    st.markdown('### ' + str(field_h) + '° х ' + str(field_v) + '°')
with col_resolving_power_minutes:
    st.markdown('Разрешающая способность')
    st.markdown('### ' + str(field_h) + '° х ' + str(field_v) + '°')