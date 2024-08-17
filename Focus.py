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


def field_calc(pixel_count, pixel_size, focus):
    field = 2 * math.atan((pixel_count * pixel_size) / (2 * focus))
    field = math.degrees(field)
    return field


def resolving_rad_calc(focus, pixel_size):
    return focus / (2 * pixel_size)

def resolving_minutes_calc(col_resolving_rad):
    return col_resolving_rad * math.pi / 180

def distance_calc(focus, threshold_pixel_count, pixel_size, target_size):
    distance = (focus * target_size) / (pixel_size * threshold_pixel_count)
    return distance

def pixel_count_calc(focus, target_size, distance, pixel_size):
    threshold_pixel_count = (focus * target_size) / (distance * pixel_size)
    threshold_pixel_count = threshold_pixel_count
    st.session_state['threshold_pixel_count'] = threshold_pixel_count
    st.session_state['threshold_enable'] = 'Свой критерий'
    return threshold_pixel_count

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
        default_matrix_type = get_variable_from_session_state('matrix_type', 'ТВ')
        st.session_state['matrix_type'] = default_matrix_type
        matrix_type = st.radio('Выберите тип матрицы', matrix_types, key='matrix_type')

    with col_select_tool:
        matrixes = list(data[matrix_type])
        if matrix_type == 'Своя':
            matrix_args_enable = False
            default_pixel_horizontal = get_variable_from_session_state('previous_pixel_horizontal', 1920)
            default_pixel_vertical = get_variable_from_session_state('previous_pixel_vertical', 1080)
            pixel_horizontal = st.number_input('Количество пикселей в матрице по горизонтали [шт] (n)', min_value=1,
                                               max_value=10000, value=default_pixel_horizontal, step=1, disabled=False)
            pixel_vertical = st.number_input('Количество пикселей в матрице по вертикали [шт] (n)', min_value=1,
                                             max_value=10000, value=default_pixel_vertical, step=1, disabled=False)
        else:
            matrix_args_enable = True
            if st.session_state.pop('previous_matrix_type', 'NO') == matrix_type:
                default_matrix_index = get_variable_from_session_state('matrix_index', 0)
            else:
                default_matrix_index = 0


            matrix = st.selectbox('Выберите матрицу', options=matrixes, index=default_matrix_index,
                                  disabled=not matrix_args_enable, placeholder='Выберите матрицу')

            previous_matrix_index = st.session_state.pop('matrix_index', 'none')
            if st.session_state.pop('previous_matrix_type', 'NO') == matrix_type and matrixes.index(matrix) == previous_matrix_index:
                default_resolution_index = get_variable_from_session_state('resolution_index', 0)
            else:
                default_resolution_index = 0
            resolutions = list(data[matrix_type][matrix])

            resolution = st.selectbox('Выберите разрешение', options=resolutions, index=default_resolution_index,
                                      disabled=len(resolutions) == 1)

    with col_data:
        if matrix_args_enable:
            pixel_horizontal = int(resolution.split()[0])
            pixel_vertical = int(resolution.split()[2])
            pixel_size = float(list(data[matrix_type][matrix][resolution])[0])
            st.session_state['pixel_size'] = pixel_size
            st.number_input('Размер пиксела [мкм] (ax)', min_value=0.01, max_value=100.0, step=0.01,
                            disabled=True, key='pixel_size')
        else:
            default_pixel_size = get_variable_from_session_state('previous_pixel_size', 3.45)
            pixel_size = st.number_input('Размер пиксела [мкм] (ax)', min_value=0.01, max_value=100.0, value=default_pixel_size,
                                         step=0.01, disabled=False, key='pixel_size')
    st.session_state['previous_matrix_type'] = matrix_type
    if matrix_type != 'Своя':
        st.session_state['matrix_index'] = matrixes.index(matrix)
        st.session_state['resolution_index'] = resolutions.index(resolution)
    st.session_state['previous_pixel_size'] = pixel_size
    st.session_state['previous_pixel_horizontal'] = pixel_horizontal
    st.session_state['previous_pixel_vertical'] = pixel_vertical
    return pixel_horizontal, pixel_vertical, pixel_size
def target_size_block():
    default_target_size = get_variable_from_session_state('target_size', 1.6)
    st.session_state['target_size'] = default_target_size
    target_size = st.number_input('Размер цели [м] (h)', min_value=0.01, max_value=1000.0, step=0.01, key='target_size')
    st.session_state['previous_target_size'] = target_size
    return target_size
def criteria_block(criterias):
    col_criteria, col_threshold = st.columns(2)

    with col_criteria:
        default_criteria = get_variable_from_session_state('threshold_enable', 'Обнаружение 2')
        st.session_state['threshold_enable'] = default_criteria
        criteria = st.selectbox('Выберите критерий', options=criterias, placeholder='Выберите матрицу',
                                key='threshold_enable')

    with col_threshold:
        if criteria == 'Свой критерий':
            default_threshold_pixel_count = get_variable_from_session_state('threshold_pixel_count', 18)
        else:
            default_threshold_pixel_count = float(criteria.split()[1])

        st.session_state['threshold_pixel_count'] = default_threshold_pixel_count

        threshold_pixel_count = st.number_input('Сколько пикселей должна занимать цель на матрице [шт]', min_value=0.1,
                                                max_value=10000.0, step=1.0,
                                                disabled=st.session_state.threshold_enable != 'Свой критерий',
                                                key='threshold_pixel_count')
    return threshold_pixel_count

def distance_block():
    default_distance = get_variable_from_session_state('distance', 1000)
    st.session_state['distance'] = default_distance
    distance = st.number_input('Требуемая дальность [м] (L)', min_value=0.1, max_value=99999.0, step=50.0, key='distance')
    return  distance


def focus_or_field(pixel_horizontal, pixel_vertical, pixel_size):

    col_select, col_focus, col_field = st.columns([1, 2, 2])

    with col_select:

        focus_or_field_selection = st.radio('Расчёт по', ['Фокус','Угловое поле'], index=0)


    if focus_or_field_selection == 'Фокус':

        with col_focus:
            default_focus = get_variable_from_session_state('focus', 100)
            st.session_state['focus'] = default_focus

            focus = st.number_input('Фокусное расстояние [мм] (f)', min_value=0.1,
                                    max_value=10000.0, step=10.0,
                                    disabled=focus_or_field_selection == 'Угловое поле', key='focus')

        st.session_state['field_h'] = field_calc(pixel_horizontal, pixel_size, focus / 1000)
        st.session_state['field_v'] = field_calc(pixel_vertical, pixel_size, focus / 1000)

        with col_field:

            st.number_input('Угловое поле по горизонтали [°] (w)', min_value=0.01,
                                               max_value=359.0, step=0.01, disabled=True, key='field_h')

            st.number_input('Угловое поле по вертикали [°] (w)', min_value=0.01,
                                               max_value=359.0, step=0.01, disabled=True, key='field_v')
    else:

        with col_field:
            default_field_h = get_variable_from_session_state('field_h', 3.0)
            st.session_state['field_h'] = default_field_h
            st.number_input('Угловое поле по горизонтали [°] (w)', min_value=0.01,
                                               max_value=359.0, step=1.0, key='field_h')

            st.session_state['field_v'] = st.session_state.field_h * pixel_vertical / pixel_horizontal
            st.session_state['focus'] = focus_calc_alt(st.session_state.field_h, pixel_horizontal, pixel_size) * 1000

            st.number_input('Угловое поле по вертикали [°] (w)', min_value=0.01,
                                               max_value=359.0, step=0.01, disabled=True, key='field_v')
        with col_focus:
            focus = st.number_input('Фокусное расстояние [мм] (f)', min_value=0.1,
                                    max_value=10000.0, step=10.0,
                                    disabled=True, key='focus')
    return focus






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

    distance = distance_block()


    pixel_size = pixel_size / 1000000

    focus = focus_calc(pixel_size, threshold_pixel_count, distance, target_size) * 1000

    st.session_state['focus'] = focus

    field_h = field_calc(pixel_horizontal, pixel_size, focus / 1000)

    field_v = field_calc(pixel_vertical, pixel_size, focus / 1000)

    col_resolving_rad = resolving_rad_calc(focus / 1000, pixel_size)
    col_resolving_minutes = resolving_minutes_calc(col_resolving_rad)

    st.subheader('Расчитанные данные')
    col_focus, col_field, col_resolving_power_lines, col_resolving_power_minutes = st.columns(4)
    with col_focus:
        st.markdown('Фокусное расстояние (f)')
    with col_field:
        st.markdown('Угловое поле (w)')
    with col_resolving_power_lines:
        st.markdown('Разрешающая способность')
    with col_resolving_power_minutes:
        st.markdown('Разрешающая способность')

    col_focus2, col_field2, col_resolving_power_lines2, col_resolving_power_minutes2 = st.columns(4)
    with col_focus2:
        st.markdown('### ' + str(round(focus, 1)) + ' мм')
    with col_field2:
        st.markdown('### ' + str(round(field_h, 2)) + '° х ' + str(round(field_v, 2)) + '°')
    with col_resolving_power_lines2:
        st.markdown('### ' + str(round(col_resolving_rad, 2)) + ' мрад⁻¹')
    with col_resolving_power_minutes2:
        st.markdown('### ' + str(round(col_resolving_minutes * 60, 2)) + ' мин⁻¹')

    st.markdown(':small_blue_diamond: Реальное угловое поле будет отличаться от расчитанного из-за оптических абераций объектива')
    st.markdown(':small_blue_diamond: Реальная разрешающая способность будет всегда ниже расчётной из-за оптических абераций объектива')
