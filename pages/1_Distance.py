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

Focus.criteria_block(criterias)
st.markdown('\n')
focus = Focus.focus_or_field(pixel_horizontal, pixel_vertical, pixel_size, accuracy=2)
