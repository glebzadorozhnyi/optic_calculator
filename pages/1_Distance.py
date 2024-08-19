import streamlit as st
st.set_page_config("Оптический калькулятор")
import Focus

Focus.adjust_width_of_page()
Focus.draw_side_bar()

Focus.load_session_state_button()
Focus.save_session_state_button()

data = Focus.read_json('data.json')
criterias = Focus.read_json('criteria.json')

st.title('Дальность')

st.markdown('Расчёт предельной дальности наблюдения объекта для заданной матрицы, размера цели, критерия наблюдения (обнаружение, распознавание) и фокуса (или углового поля) объектива.')

pixel_horizontal, pixel_vertical, pixel_size = Focus.head_and_matrix(data)
pixel_size = pixel_size / 1000000

target_size = Focus.target_size_block()

threshold_pixel_count = Focus.criteria_block(criterias)
st.markdown('\n')

focus = Focus.focus_or_field(pixel_horizontal, pixel_vertical, pixel_size)

distance = Focus.distance_calc(focus / 1000, threshold_pixel_count, pixel_size, target_size)

st.session_state['distance'] = distance

col_resolving_rad = Focus.resolving_rad_calc(focus / 1000, pixel_size)
col_resolving_minutes = Focus.resolving_minutes_calc(col_resolving_rad)

st.subheader('Расчитанные данные')

col_distance, col_resolving_power_lines, col_resolving_power_minutes = st.columns(3)


with col_distance:
    st.markdown('Дальность наблюдения (L)', help='Дальность наблюдения согласно выбранному критерию')
    st.markdown('### ' + str(round(distance, 1)) + ' м')

with col_resolving_power_lines:
    st.markdown('Разрешающая способность', help='Эта величина нужна для правильного выбора оптической миры, необходимой для проверки качества сборки канала')
    st.markdown('### ' + str(round(col_resolving_rad)) + ' мрад⁻¹')
with col_resolving_power_minutes:
    st.markdown('Разрешающая способность', help='Эта величина нужна для правильного выбора оптической миры, необходимой для проверки качества сборки канала')
    st.markdown('### ' + str(round(col_resolving_minutes, 2)) + ' мин⁻¹')



Focus.resolving_disclaimer()
Focus.pdf_block()