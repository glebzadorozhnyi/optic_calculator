import Focus
import streamlit as st



Focus.adjust_width_of_page()

Focus.load_session_state_button()
Focus.save_session_state_button()

data = Focus.read_json('data.json')
criterias = Focus.read_json('criteria.json')

st.title('Оптический калькулятор')

st.markdown('Расчёт размера объекта, для которого будет выполнен критерий наблюдения при заданной матрице, дальности до цели и фокуса (или углового поля) объектива.')

pixel_horizontal, pixel_vertical, pixel_size = Focus.head_and_matrix(data)
pixel_size = pixel_size / 1000000

threshold_pixel_count = Focus.criteria_block(criterias)

distance = Focus.distance_block()

focus = Focus.focus_or_field(pixel_horizontal, pixel_vertical, pixel_size)

target_size = Focus.target_size_calc(focus/1000, threshold_pixel_count, pixel_size, distance)

st.session_state['target_size'] = target_size

col_resolving_rad = Focus.resolving_rad_calc(focus / 1000, pixel_size)
col_resolving_minutes = Focus.resolving_minutes_calc(col_resolving_rad)

st.subheader('Расчитанные данные')

col_pixels, col_resolving_power_lines, col_resolving_power_minutes = st.columns(3)


with col_pixels:
    st.markdown('Размер цели для которой будет выполнен критерий наблюдения')

with col_resolving_power_lines:
    st.markdown('Разрешающая способность', help='Эта величина нужна для правильного выбора оптической миры, необходимой для проверки качества сборки канала')
with col_resolving_power_minutes:
    st.markdown('Разрешающая способность', help='Эта величина нужна для правильного выбора оптической миры, необходимой для проверки качества сборки канала')

col_pixels2, col_resolving_power_lines2, col_resolving_power_minutes2 = st.columns(3)
with col_pixels2:
    if target_size < 1:
        st.markdown('### ' + str(round(target_size*100, 2)) + ' см')
    else:
        st.markdown('### ' + str(round(target_size, 2)) + ' м')
with col_resolving_power_lines2:
    st.markdown('### ' + str(round(col_resolving_rad)) + ' мрад⁻¹')
with col_resolving_power_minutes2:
    st.markdown('### ' + str(round(col_resolving_minutes, 2)) + ' мин⁻¹')

Focus.resolving_disclaimer()
Focus.pdf_block()