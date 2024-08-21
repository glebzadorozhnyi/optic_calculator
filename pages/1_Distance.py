import streamlit as st
st.set_page_config("Оптический калькулятор")
import Focus

Focus.adjust_width_of_page()
Focus.draw_side_bar(page_2=True)

data = Focus.read_json('data.json')
criterias = Focus.read_json('criteria.json')
keys_to_save = list(Focus.read_json('keys_to_save.json'))

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

resolving_rad = Focus.resolving_rad_calc(focus / 1000, pixel_size)
degree_resolving = Focus.degree_resolution_calc(pixel_size, focus / 1000)

st.subheader('Расчитанные данные')

col_distance, col_resolving_power_lines, col_degree_resolving = st.columns(3)


with col_distance:
    st.markdown('Дальность наблюдения (L)', help='Дальность наблюдения согласно выбранному критерию')
    st.markdown('### ' + str(round(distance, 1)) + ' м')

Focus.resolving_power_block(col_resolving_power_lines, resolving_rad)
Focus.degree_resolution_block(col_degree_resolving, degree_resolving)



Focus.resolving_disclaimer()

Focus.load_session_state_button()
Focus.save_session_state_button(keys_to_save)
Focus.pdf_block()

