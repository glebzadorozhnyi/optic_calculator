import streamlit as st
import math
import json

@st.cache_data
def adjust_width_of_page():
    css = '''
    <style>
        section.main > div {max-width:55rem}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)


@st.cache_data
def read_json(filename):
    file = open(filename)
    data = json.load(file)
    file.close()
    return data

def focus_calc(pixel_size, threshold_pixel_count, distance, target_size):
    focus = (pixel_size * threshold_pixel_count * distance) / target_size
    return focus

def focus_calc_alt(field_h, pixel_horizontal, pixel_size):
    field_h = math.radians(field_h) / 2
    focus = (pixel_size * pixel_horizontal * 0.5) / math.tan(field_h)
    return focus


def field_calc(pixel_count, pixel_size, focus, accuracy=1):
    field = 2 * math.atan((pixel_count * pixel_size) / (2 * focus))
    field = round(math.degrees(field), accuracy)
    return field


def resolving_rad_calc(focus, pixel_size):
    return focus / (2 * pixel_size * 1000)

def resolving_minutes_calc(col_resolving_rad):
    return col_resolving_rad * math.pi / 180

def distance_calc(focus, threshold_pixel_count, pixel_size, target_size):
    distance = (focus * target_size) / (pixel_size * threshold_pixel_count)
    return distance

def get_variable_from_session_state(variable_name, default_value=None):
    if variable_name in st.session_state:
        return st.session_state[variable_name]
    else:
        return default_value

def draw_head(data):
    st.image('shema.jpg', )

    st.subheader('Входные данные')

    col_matrix_type, col_select_tool, col_data = st.columns([1, 1.9, 1.2])

    matrix_types = list(data)

    with col_matrix_type:
        matrix_type = st.radio('Выберите тип матрицы', matrix_types, index=0)

    with col_select_tool:
        matrixes = list(data[matrix_type])
        if matrix_type == 'Своя':
            matrix_args_enable = False
            pixel_horizontal = st.number_input('Количество пикселей в матрице по горизонтали [шт] (n)', min_value=1,
                                               max_value=10000, value=1920, step=1, disabled=False)
            pixel_vertical = st.number_input('Количество пикселей в матрице по вертикали [шт] (n)', min_value=1,
                                             max_value=10000, value=1080, step=1, disabled=False)
        else:
            matrix_args_enable = True

            matrix = st.selectbox('Выберите матрицу', options=matrixes, index=0,
                                  disabled=not matrix_args_enable, placeholder='Выберите матрицу')
            resolution = st.selectbox('Выберите разрешение', options=data[matrix_type][matrix], index=0,
                                      disabled=len(data[matrix_type][matrix]) == 1)

    with col_data:
        if matrix_args_enable:
            pixel_horizontal = int(resolution.split()[0])
            pixel_vertical = int(resolution.split()[2])
            pixel_size = float(list(data[matrix_type][matrix][resolution])[0])
            st.session_state['pixel_size'] = pixel_size
            st.number_input('Размер пиксела [мкм] (ax)', min_value=0.01, max_value=100.0, step=0.01,
                            disabled=True, key='pixel_size')
        else:
            pixel_size = st.number_input('Размер пиксела [мкм] (ax)', min_value=0.01, max_value=100.0, value=3.45,
                                         step=0.01, disabled=False, key='pixel_size')
    return pixel_horizontal, pixel_vertical, pixel_size
def target_size_block():
    target_size = st.number_input('Размер цели [м] (h)', min_value=0.01, max_value=1000.0, value=1.6, step=0.01)
    return target_size
def criteria_block(criterias):
    col_criteria, col_threshold = st.columns(2)

    with col_criteria:
        criteria = st.selectbox('Выберите критерий', options=criterias, index=0, placeholder='Выберите матрицу',
                                key='threshold_enable')

    with col_threshold:
        if criteria == 'Свой критерий':
            threshold_pixel_count_init = st.session_state.threshold_pixel_count
        else:
            threshold_pixel_count_init = int(criteria.split()[1])
        threshold_pixel_count = st.number_input('Сколько пикселей должна занимать цель на матрице [шт]', min_value=1,
                                                max_value=10000, value=threshold_pixel_count_init, step=1,
                                                disabled=st.session_state.threshold_enable != 'Свой критерий',
                                                key='threshold_pixel_count')
    return threshold_pixel_count

def focus_or_field(pixel_horizontal, pixel_vertical, pixel_size, accuracy=1, default_focus=100):

    col_select, col_focus, col_field = st.columns([1, 2, 2])

    with col_select:

        focus_or_field_selection = st.radio('Расчёт по', ['Фокус','Угловое поле'], index=0)





    if focus_or_field_selection == 'Фокус':

        with col_focus:
            if 'focus' in st.session_state:
                default_focus = st.session_state.focus
            focus = st.number_input('Фокусное расстояние [мм] (f)', min_value=1,
                                    max_value=10000, value=default_focus, step=1,
                                    disabled=focus_or_field_selection == 'Угловое поле', key='focus')

        st.session_state.field_h = field_calc(pixel_horizontal, pixel_size, focus / 1000, accuracy)
        st.session_state.field_v = field_calc(pixel_vertical, pixel_size, focus / 1000, accuracy)

        with col_field:

            st.number_input('Угловое поле по горизонтали [°] (w)', min_value=0.01,
                                               max_value=359.0, step=0.01, disabled=True, key='field_h')

            st.number_input('Угловое поле по вертикали [°] (w)', min_value=0.01,
                                               max_value=359.0, step=0.01, disabled=True, key='field_v')
    else:

        with col_field:
            if 'field_h' in st.session_state:
                default_field_h = st.session_state.field_h
            else:
                default_field_h = 3.0
            st.number_input('Угловое поле по горизонтали [°] (w)', min_value=0.01,
                                               max_value=359.0, value=default_field_h, step=0.01, key='field_h')
            st.session_state.field_v = st.session_state.field_h * pixel_vertical/ pixel_horizontal
            st.session_state.focus = focus_calc_alt(st.session_state.field_h, pixel_horizontal, pixel_size) * 1000

            st.number_input('Угловое поле по вертикали [°] (w)', min_value=0.01,
                                               max_value=359.0, step=0.01, disabled=True, key='field_v')
        with col_focus:
            focus = st.number_input('Фокусное расстояние [мм] (f)', min_value=1,
                                    max_value=10000, step=1,
                                    disabled=True, key='focus')
    return focus / 1000






if __name__ == "__main__":
    data = read_json('data.json')
    criterias = list(read_json('criteria.json'))

    adjust_width_of_page()

    st.title('Оптический калькулятор')

    st.markdown('''Расчёт фокусного расстояния объектива для заданной матрицы, размера цели, критерия наблюдения (обнаружение, распознавание) и дальности наблюдения.\n
Угловое поле расчитывается исходя из получившегося фокусного расстояния и заданой матрицы.''')

    pixel_horizontal, pixel_vertical, pixel_size = draw_head(data)

    target_size = target_size_block()

    threshold_pixel_count = criteria_block(criterias)

    distance = st.number_input('Требуемая дальность [м] (L)', min_value=1, max_value=99999, value=1000, step=1, key='flag')
    pixel_size = pixel_size / 1000000
    focus = focus_calc(pixel_size, threshold_pixel_count, distance, target_size)

    field_h = field_calc(pixel_horizontal, pixel_size, focus)

    field_v = field_calc(pixel_vertical, pixel_size, focus)

    col_resolving_rad = resolving_rad_calc(focus, pixel_size)
    col_resolving_minutes = resolving_minutes_calc(col_resolving_rad)

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
        st.markdown('### ' + str(round(col_resolving_rad, 2)) + ' мрад⁻¹')
    with col_resolving_power_minutes:
        st.markdown('Разрешающая способность')
        st.markdown('### ' + str(round(col_resolving_minutes * 60, 2)) + ' мин⁻¹')

    st.markdown(':small_blue_diamond: Реальное угловое поле будет отличаться от расчитанного из-за оптических абераций объектива')
    st.markdown(':small_blue_diamond: Реальная разрешающая способность будет всегда ниже расчётной из-за оптических абераций объектива')
