import streamlit as st
import math
import json


@st.cache_data
def adjust_width_of_page():
    css = '''
    <style>
        section.main > div {max-width:60rem}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)
def draw_side_bar(page_1=False, page_2=False, page_3=False, page_4=False):
    with st.sidebar:
        icon = ':material/calculate:'
        st.page_link('Focus.py', label='Фокус', icon=icon if page_1 else None)
        st.page_link('pages/1_Distance.py', label='Дальность', icon=icon if page_2 else None)
        st.page_link('pages/2_Pixels.py', label='Пиксели', icon=icon if page_3 else None)
        st.page_link('pages/3_Target_size.py', label='Размер объекта', icon=icon if page_4 else None)


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

def degree_resolution_calc(pixel_size, focus):
    return math.degrees(math.atan(pixel_size / focus) * 2 * 3600)

def distance_calc(focus, threshold_pixel_count, pixel_size, target_size):
    distance = (focus * target_size) / (pixel_size * threshold_pixel_count)
    return distance

def pixel_count_calc(focus, target_size, distance, pixel_size, custom_criteria):
    threshold_pixel_count = (focus * target_size) / (distance * pixel_size)
    threshold_pixel_count = threshold_pixel_count
    st.session_state['threshold_pixel_count'] = threshold_pixel_count
    st.session_state['threshold_enable'] = custom_criteria
    return threshold_pixel_count

def target_size_calc(focus, threshold_pixel_count, pixel_size, distance):
    target_size = distance * threshold_pixel_count * pixel_size / focus
    return target_size

def diagonal_matrix_pixel_calc(pixel_horizontal, pixel_vertical):
    diagonal = math.sqrt(pixel_horizontal ** 2 + pixel_vertical ** 2)
    return diagonal

def dd2dms(decimaldegree):
    if type(decimaldegree) != 'float':
        try:
            decimaldegree = float(decimaldegree)
        except:
            return 0
    minutes = decimaldegree % 1.0 * 60

    return '{0}°{1}\''.format(int(math.floor(decimaldegree)), int(math.floor(minutes)))


def get_variable_from_session_state(variable_name, default_value=None):
    if variable_name in st.session_state:
        return st.session_state[variable_name]
    else:
        return default_value

def head_and_matrix(data):
    st.image('shema.jpg', )

    st.subheader('Входные данные')

    col_matrix_type, col_matrix_and_resolution, col_pixel_size = st.columns([1, 1.9, 1.2])

    matrix_types = list(data)

    with col_matrix_type:
        default_matrix_type = get_variable_from_session_state('matrix_type', matrix_types[0])
        st.session_state['matrix_type'] = default_matrix_type
        matrix_type = st.radio('Выберите тип матрицы', matrix_types, key='matrix_type')

    with col_matrix_and_resolution:
        matrixes = list(data[matrix_type])
        if matrix_type == matrix_types[-1]:
            default_pixel_horizontal = get_variable_from_session_state('pixel_horizontal', 1920)
            default_pixel_vertical = get_variable_from_session_state('pixel_vertical', 1080)
            st.session_state['pixel_horizontal'] = default_pixel_horizontal
            st.session_state['pixel_vertical'] = default_pixel_vertical
            pixel_horizontal = st.number_input('Количество пикселей в матрице по горизонтали [шт] (n)', min_value=1,
                                               max_value=10000, step=1, disabled=False, key='pixel_horizontal')
            pixel_vertical = st.number_input('Количество пикселей в матрице по вертикали [шт] (n)', min_value=1,
                                             max_value=10000, step=1, disabled=False, key='pixel_vertical')
        else:
            previous_matrix_type = get_variable_from_session_state('previous_matrix_type', 'NO')
            if previous_matrix_type == matrix_type:
                default_matrix = get_variable_from_session_state('matrix', matrixes[0])
                previous_matrix = st.session_state.pop('previous_matrix')
            else:
                default_matrix = matrixes[0]
                previous_matrix = 'none'

            st.session_state['matrix'] = default_matrix

            matrix = st.selectbox('Выберите матрицу', options=matrixes,
                                  disabled=False, placeholder='Выберите матрицу', key='matrix')
            resolutions = list(data[matrix_type][matrix])
            st.session_state['previous_matrix'] = matrix

            if previous_matrix_type == matrix_type and previous_matrix == matrix:
                default_resolution = st.session_state.pop('resolution', resolutions[0])
            else:
                default_resolution = resolutions[0]

            st.session_state['resolution'] = default_resolution

            resolution = st.selectbox('Выберите разрешение', options=resolutions,
                                      disabled=len(resolutions) == 1, key = 'resolution')

    with col_pixel_size:
        if matrix_type == matrix_types[-1]:
            default_pixel_size = get_variable_from_session_state('pixel_size', 3.45)
            st.session_state['pixel_size'] = default_pixel_size
            pixel_size = st.number_input('Размер пиксела [мкм] (ax)', min_value=0.01, max_value=100.0,
                                         step=0.01, disabled=False, key='pixel_size', help= 'Пиксель – мельчайшая часть исходного изображения. Теоретически большее количество мегапикселей позволяет получить более высокое качество видео. На практике имеет значение не только число пикселей, но и их размер.')
        else:
            pixel_horizontal = int(resolution.split()[0])
            pixel_vertical = int(resolution.split()[2])
            pixel_size = float(list(data[matrix_type][matrix][resolution])[0])
            st.session_state['pixel_size'] = pixel_size
            st.session_state['pixel_horizontal'] = pixel_horizontal
            st.session_state['pixel_vertical'] = pixel_vertical

            st.number_input('Размер пиксела [мкм] (ax)', min_value=0.01, max_value=100.0, step=0.01,
                            disabled=True, key='pixel_size', help='Пиксель – мельчайшая часть исходного изображения. Теоретически большее количество мегапикселей позволяет получить более высокое качество видео. На практике имеет значение не только число пикселей, но и их размер.')
    st.session_state['previous_matrix_type'] = matrix_type
    return pixel_horizontal, pixel_vertical, pixel_size
def target_size_block():
    default_target_size = get_variable_from_session_state('target_size', 1.6)
    st.session_state['target_size'] = default_target_size
    target_size = st.number_input('Размер цели [м] (h)', min_value=0.01, max_value=1000.0, step=0.1, key='target_size', help='Характерный размер объекта. Выбирают либо минимальный из наблюдаемых габаритов min(Ш, В), либо средний (Ш + В)*0,5')
    st.session_state['previous_target_size'] = target_size
    return target_size
def criteria_block(criterias):
    col_criteria, col_threshold = st.columns(2)
    options = list(criterias)
    with col_criteria:
        default_criteria = get_variable_from_session_state('threshold_enable', options[0])
        st.session_state['threshold_enable'] = default_criteria
        criteria = st.selectbox('Выберите критерий', options=options,
                                key='threshold_enable', help='Критерий Джонсона - это наиболее часто употребляемый критерий для расчета дальности действия оптико-электронных приборов')

    with col_threshold:
        if criteria == options[-1]:
            default_threshold_pixel_count = get_variable_from_session_state('threshold_pixel_count', 18)
        else:
            default_threshold_pixel_count = float(criterias[criteria])

        st.session_state['threshold_pixel_count'] = default_threshold_pixel_count

        threshold_pixel_count = st.number_input('Сколько пикселей должна занимать цель на матрице [шт]', min_value=0.1,
                                                max_value=10000.0, step=1.0,
                                                disabled=st.session_state.threshold_enable != options[-1],
                                                key='threshold_pixel_count')
    return threshold_pixel_count

def distance_block():
    default_distance = get_variable_from_session_state('distance', 5000)
    st.session_state['distance'] = default_distance
    distance = st.number_input('Требуемая дальность [м] (L)', min_value=0.1, max_value=99999.0, step=50.0, key='distance')
    return  distance


def focus_or_field(pixel_horizontal, pixel_vertical, pixel_size):

    col_select, col_focus, col_field = st.columns([1, 2, 2])

    with col_select:

        focus_or_field_selection = st.radio('Расчёт по', ['Фокус','Угол обзора'], index=0, help='Фокусное расстояние и угол обзора это зависимые друг от друга величины, поэтому задать можно только одну, а вторая будет рассчитана')


    if focus_or_field_selection == 'Фокус':

        with col_focus:
            default_focus = get_variable_from_session_state('focus', 100)
            st.session_state['focus'] = default_focus

            focus = st.number_input('Фокусное расстояние [мм] (f)', min_value=0.1,
                                    max_value=10000.0, step=10.0,
                                    disabled=focus_or_field_selection == 'Угол обзора', key='focus', help='Чем меньше фокусное расстояние, тем больше угол обзора (и наоборот)')

        st.session_state['field_h'] = field_calc(pixel_horizontal, pixel_size, focus / 1000)
        st.session_state['field_v'] = field_calc(pixel_vertical, pixel_size, focus / 1000)

        with col_field:

            st.number_input('Угол обзора по горизонтали [°] (w)', min_value=0.01,
                                               max_value=359.0, step=0.01, disabled=True, key='field_h', help= "Ввод только в десятичном формате. Снизу отображение в формате [Градусы° Угловые минуты']")

            st.number_input('Угол обзора по вертикали [°]', min_value=0.01,
                                               max_value=359.0, step=0.01, disabled=True, key='field_v')
            st.markdown(dd2dms(st.session_state.field_h) + ' х ' + dd2dms(st.session_state.field_v))
    else:

        with col_field:
            default_field_h = get_variable_from_session_state('field_h', 3.0)
            st.session_state['field_h'] = default_field_h
            st.number_input('Угол обзора по горизонтали [°] (w)', min_value=0.01,
                                               max_value=359.0, step=1.0, key='field_h', help= "Ввод только в десятичном формате. Снизу отображение в формате [Градусы° Угловые минуты']")

            st.session_state['field_v'] = st.session_state.field_h * pixel_vertical / pixel_horizontal
            st.session_state['focus'] = focus_calc_alt(st.session_state.field_h, pixel_horizontal, pixel_size) * 1000

            st.number_input('Угол обзора по вертикали [°]', min_value=0.01,
                                               max_value=359.0, step=0.01, disabled=True, key='field_v')

            st.markdown(dd2dms(st.session_state.field_h) + ' х ' + dd2dms(st.session_state.field_v))

        with col_focus:
            focus = st.number_input('Фокусное расстояние [мм] (f)', min_value=0.1,
                                    max_value=10000.0, step=10.0,
                                    disabled=True, key='focus')
    return focus

def resolving_power_block(column, resolving_power):
    with column:
        st.markdown('Разрешающая способность',
                    help='Эта величина нужна для правильного выбора оптической миры, необходимой для проверки качества сборки канала')
        st.markdown('### ' + str(round(resolving_power)) + ' рад⁻¹')

def degree_resolution_block(column, degree_resolution):
    with column:
        st.markdown('Угловое разрешение', help='[угловые секунды] Минимальный угол между объектами, который может различить оптическая система')
        st.markdown('### ' + str(round(degree_resolution, 2)) + '"')



def save_session_state_button():
    with st.sidebar:
        data_to_save = st.session_state.to_dict()
        data_to_save.pop('upload_file', None)
        st.download_button('Экспорт расчёта', json.dumps(data_to_save), file_name='optic_calculator.json')

def load_session_state_button():
    def update_session_state():
        upload_file = get_variable_from_session_state('upload_file', None)
        if upload_file is not None:
            try:
                data = json.load(st.session_state['upload_file'])
                for key, value in data.items():
                    if key == 'upload_file':
                        continue
                    st.session_state[key] = value
            except:
                with st.sidebar:
                    st.warning('Не удалось считать файл')


    with st.sidebar:
        st.file_uploader('Импорт расчёта', type='json', on_change=update_session_state, key='upload_file',)



def pdf_block():
    with st.sidebar:
        st.markdown('''Чтобы сохранить страницу в pdf нажмите на меню в правом верхнем углу - Print - Save as PDF. \n 
Измените формат листа или масштба страницы, если она не поместилась целиком''')

def resolving_disclaimer():
    st.markdown(
        ':small_blue_diamond: Реальная разрешающая способность будет всегда ниже расчётной из-за оптических абераций объектива')



if __name__ == "__main__":
    st.set_page_config("Оптический калькулятор")
    data = read_json('data.json')
    criterias = read_json('criteria.json')
    adjust_width_of_page()
    draw_side_bar(page_1=True)


    st.title('Фокусное расстояние и Угол обзора')

    st.markdown('''Расчёт фокусного расстояния объектива для заданной матрицы, размера объекта, критерия наблюдения (обнаружение, распознавание) и дальности наблюдения.\n
Угол обзора рассчитывается исходя из получившегося фокусного расстояния и заданой матрицы.''')

    pixel_horizontal, pixel_vertical, pixel_size = head_and_matrix(data)

    target_size = target_size_block()

    threshold_pixel_count = criteria_block(criterias)

    distance = distance_block()

    pixel_size = pixel_size / 1000000

    focus = focus_calc(pixel_size, threshold_pixel_count, distance, target_size) * 1000
    st.session_state['focus'] = focus

    field_h = field_calc(pixel_horizontal, pixel_size, focus / 1000)
    field_v = field_calc(pixel_vertical, pixel_size, focus / 1000)

    diagonal_pixel = diagonal_matrix_pixel_calc(pixel_horizontal, pixel_vertical)

    field_d = field_calc(diagonal_pixel, pixel_size, focus / 1000)

    resolving_rad = resolving_rad_calc(focus / 1000, pixel_size)
    degree_resolving = degree_resolution_calc(pixel_size, focus / 1000)

    st.subheader('Расчитанные данные')
    col_focus, col_field, diag_field, col_resolving_power_lines  = st.columns([0.9, 1.1, 1, 1])
    with col_focus:
        st.markdown('Фокусное расстояние (f)', help='Чем меньше фокусное расстояние, тем больше угол обзора (и наоборот)')
        st.markdown('### ' + str(round(focus, 1)) + ' мм')
    with col_field:
        st.markdown('Угол обзора ШхВ (w)', help= 'Чем шире угол обзора - тем большее пространство захватывает камера и в то же время мельче получаются изображения отдельных предметов в кадре')
        st.markdown('### ' + dd2dms(field_h) + ' х ' + dd2dms(field_v))
    with diag_field:
        st.markdown('Угол обзора по диагонали')
        st.markdown('### ' + dd2dms(field_d))
    resolving_power_block(col_resolving_power_lines, resolving_rad)


    _, _, _, col_degree_resolving = st.columns([0.9, 1.1, 1, 1])

    degree_resolution_block(col_degree_resolving, degree_resolving)


    st.markdown(':small_blue_diamond: Реальный угол обзора будет отличаться от расчитанного из-за оптических абераций объектива')
    resolving_disclaimer()

    load_session_state_button()
    save_session_state_button()
    pdf_block()



