import streamlit as st
st.set_page_config("Оптический калькулятор")
import Focus

Focus.adjust_width_of_page()
Focus.draw_side_bar(page_3=True)


data = Focus.read_json('data.json')
criterias = Focus.read_json('criteria.json')
keys_to_save = list(Focus.read_json('keys_to_save.json'))

st.title('Пиксели')

st.markdown('Расчёт количества пикселей, которые будет занимать объект на матрице для заданной матрицы, размера цели, дальности до цели и фокуса (или углового поля) объектива.')

pixel_horizontal, pixel_vertical, pixel_size = Focus.head_and_matrix(data)
pixel_size = pixel_size / 1000000

target_size = Focus.target_size_block()

distance = Focus.distance_block()

focus = Focus.focus_or_field(pixel_horizontal, pixel_vertical, pixel_size)

resolving_rad = Focus.resolving_rad_calc(focus / 1000, pixel_size)
degree_resolving = Focus.degree_resolution_calc(pixel_size, focus / 1000)

st.subheader('Расчитанные данные')

col_pixels, col_resolving_power_lines, col_degree_resolving = st.columns(3)

threshold_pixel_count = Focus.pixel_count_calc(focus / 1000, target_size, distance, pixel_size, list(criterias)[-1])


with col_pixels:
    st.markdown('Количество пикселей', help='Количество пикселей, которые занимает цель на матрице')
    st.markdown('### ' + str(round(threshold_pixel_count, 2)) + ' пикс')

Focus.resolving_power_block(col_resolving_power_lines, resolving_rad)
Focus.degree_resolution_block(col_degree_resolving, degree_resolving)


Focus.resolving_disclaimer()

Focus.load_session_state_button()
Focus.save_session_state_button(keys_to_save)
Focus.pdf_block()

