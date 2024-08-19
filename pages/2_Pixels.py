import Focus
import streamlit as st



Focus.adjust_width_of_page()

Focus.load_session_state_button()
Focus.save_session_state_button()

data = Focus.read_json('data.json')
criterias = Focus.read_json('criteria.json')

st.title('Оптический калькулятор')

st.markdown('Расчёт количества пикселей, которые будет занимать объект на матрице для заданной матрицы, размера цели, дальности до цели и фокуса (или углового поля) объектива.')

pixel_horizontal, pixel_vertical, pixel_size = Focus.head_and_matrix(data)
pixel_size = pixel_size / 1000000

target_size = Focus.target_size_block()

distance = Focus.distance_block()

focus = Focus.focus_or_field(pixel_horizontal, pixel_vertical, pixel_size)

col_resolving_rad = Focus.resolving_rad_calc(focus / 1000, pixel_size)
col_resolving_minutes = Focus.resolving_minutes_calc(col_resolving_rad)

st.subheader('Расчитанные данные')

col_pixels, col_resolving_power_lines, col_resolving_power_minutes = st.columns(3)

threshold_pixel_count = Focus.pixel_count_calc(focus / 1000, target_size, distance, pixel_size, list(criterias)[-1])


with col_pixels:
    st.markdown('Количество пикселей', help='Количество пикселей, которые занимает цель на матрице')
    st.markdown('### ' + str(round(threshold_pixel_count, 2)) + ' пикс')

with col_resolving_power_lines:
    st.markdown('Разрешающая способность', help='Эта величина нужна для правильного выбора оптической миры, необходимой для проверки качества сборки канала')
    st.markdown('### ' + str(round(col_resolving_rad)) + ' мрад⁻¹')
with col_resolving_power_minutes:
    st.markdown('Разрешающая способность', help='Эта величина нужна для правильного выбора оптической миры, необходимой для проверки качества сборки канала')
    st.markdown('### ' + str(round(col_resolving_minutes, 2)) + ' мин⁻¹')


Focus.resolving_disclaimer()
Focus.pdf_block()