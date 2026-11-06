import streamlit as st 
nombre=st.text_input("Introduce tu nombre")
edad=st.number_input("Introduce tu edad",value=0) # con value=0 sale los números enteros
                                                  # si no pones nada son nuúmeros float
afiliado=st.checkbox("Afiliado")
curso=st.radio("Elige curso: ", ["Python","C++","Java"])
centro=st.selectbox("Elige centro:",["Leganés","Getafe","Alcobendas","San Blas"])
if st.button("Pulsar"):
        st.success(f"Te llamas {nombre}, tienes {edad} años, has elegido el curso {curso} y en el centro de {centro}")

aula = [ 
    {"id": 1, "nombre": "Juan", "edad": 25}, 
    {"id": 2, "nombre": "Ana", "edad": 30}, 
    {"id": 3, "nombre": "Pedro", "edad": 22} 
] 
st.table(aula) 


# st.number_input("Insert a number", value=0, placeholder="Type a number...") 
