import Focus
import streamlit as st



Focus.adjust_width_of_page()

data = Focus.read_json('data.json')
criterias = list(Focus.read_json('criteria.json'))

st.title('Оптический калькулятор')

st.markdown('Расчёт размера цели, для которой будет выполнен критерий наблюдения при заданной матрице, дальности до цели и фокуса (или углового поля) объектива.')

pixel_horizontal, pixel_vertical, pixel_size = Focus.draw_head(data)
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
    st.markdown('Разрешающая способность')
with col_resolving_power_minutes:
    st.markdown('Разрешающая способность')

col_pixels2, col_resolving_power_lines2, col_resolving_power_minutes2 = st.columns(3)
with col_pixels2:
    if target_size < 1:
        st.markdown('### ' + str(round(target_size*100, 2)) + ' см')
    else:
        st.markdown('### ' + str(round(target_size, 2)) + ' м')
with col_resolving_power_lines2:
    st.markdown('### ' + str(round(col_resolving_rad, 2)) + ' мрад⁻¹')
with col_resolving_power_minutes2:
    st.markdown('### ' + str(round(col_resolving_minutes * 60, 2)) + ' мин⁻¹')

st.markdown(':small_blue_diamond: Реальная разрешающая способность будет всегда ниже расчётной из-за оптических абераций объектива')