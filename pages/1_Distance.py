from Focus import read_json, focus_calc, field_calc, resolving_rad_calc, resolving_minutes_calc, adjust_width_of_page, draw_head, criteria_block, target_size_block
import streamlit as st



adjust_width_of_page(st)

data = read_json('data.json')
criterias = list(read_json('criteria.json'))

st.title('Оптический калькулятор')

st.markdown('Расчёт предельной дистанции наблюдения цели для заданной матрицы, размера цели, критерия наблюдения (обнаружение, распознавание) и фокуса (или углового поля) объектива.')

pixel_horizontal, pixel_vertical, pixel_size = draw_head(st, data)

target_size = target_size_block(st)

criteria_block(st,criterias)
