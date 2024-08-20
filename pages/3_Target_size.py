import streamlit as st
st.set_page_config("Оптический калькулятор")
import Focus

Focus.adjust_width_of_page()
Focus.draw_side_bar(page_4=True)


data = Focus.read_json('data.json')
criterias = Focus.read_json('criteria.json')

st.title('Размер цели')

st.markdown('Расчёт размера объекта, для которого будет выполнен критерий наблюдения при заданной матрице, дальности до цели и фокуса (или углового поля) объектива.')

pixel_horizontal, pixel_vertical, pixel_size = Focus.head_and_matrix(data)
pixel_size = pixel_size / 1000000

threshold_pixel_count = Focus.criteria_block(criterias)

distance = Focus.distance_block()

focus = Focus.focus_or_field(pixel_horizontal, pixel_vertical, pixel_size)

target_size = Focus.target_size_calc(focus/1000, threshold_pixel_count, pixel_size, distance)

st.session_state['target_size'] = target_size

resolving_rad = Focus.resolving_rad_calc(focus / 1000, pixel_size)
degree_resolving = Focus.degree_resolution_calc(pixel_size, focus / 1000)

st.subheader('Расчитанные данные')

col_pixels, col_resolving_power_lines, col_degree_resolving = st.columns(3)


with col_pixels:
    st.markdown('Размер цели', help='Размер цели для которой будет выполнен критерий наблюдения')
    if target_size < 1:
        st.markdown('### ' + str(round(target_size*100, 2)) + ' см')
    else:
        st.markdown('### ' + str(round(target_size, 2)) + ' м')

Focus.resolving_power_block(col_resolving_power_lines, resolving_rad)
Focus.degree_resolution_block(col_degree_resolving, degree_resolving)

Focus.resolving_disclaimer()

Focus.load_session_state_button()
Focus.save_session_state_button()
Focus.pdf_block()

