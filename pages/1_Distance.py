import Focus
import streamlit as st



Focus.adjust_width_of_page()

data = Focus.read_json('data.json')
criterias = list(Focus.read_json('criteria.json'))

st.title('Оптический калькулятор')

st.markdown('Расчёт предельной дистанции наблюдения цели для заданной матрицы, размера цели, критерия наблюдения (обнаружение, распознавание) и фокуса (или углового поля) объектива.')

pixel_horizontal, pixel_vertical, pixel_size = Focus.draw_head(data)
pixel_size = pixel_size / 1000000

target_size = Focus.target_size_block()

threshold_pixel_count = Focus.criteria_block(criterias)
st.markdown('\n')
default_focus = Focus.get_variable_from_session_state('default_focus', 0.1) * 1000

focus = Focus.focus_or_field(pixel_horizontal, pixel_vertical, pixel_size, accuracy=2, default_focus=int(default_focus))

st.session_state['default_focus'] = focus

distance = Focus.distance_calc(focus, threshold_pixel_count, pixel_size, target_size)

st.subheader('Расчитанные данные')
st.markdown('Дальность наблюдения согласно выбранному критерию (L)')
st.markdown('### ' + str(round(distance, 1)) + ' м')

