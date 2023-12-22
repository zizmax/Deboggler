import streamlit as st
import boggle
import time

# set page title
st.title('Boggle UI :game_die: :rocket:')

#my_select_box = st.sidebar.selectbox('Select country:', list(['US', 'UK', 'DE', 'FR', 'JP']) )
#my_slider = st.sidebar.slider('Temperature C')
#st.sidebar.write(f'Temperature F: {my_slider * 1.8 + 32}')

def custom_key(str):
   return -len(str), str.lower()


boardstring = st.text_input("Enter Boggle board letters:")

valid_string = True
if boardstring:
    if len(boardstring) < 16:
        st.error("Must enter exactly 16 letters!")
        valid_string = False
    if not boardstring.isalpha():
        st.error("Must only enter letters!")
        valid_string = False
    if valid_string:
        start = time.time()
        found, board = boggle.crunch(boardstring)
        end = time.time()
        st.write("Found " + str(len(found)) + " words in " + str(round((end-start) * 1000, 2)) + "ms :zap:")

        st.header("**Board:**")

        for row in range(0, 4):
            st.subheader("| " + board[0][row] + " | " + board[1][row] + " | " + board[2][row] + " | " + board[3][row] + " |")
        with st.expander("Show all words"):
            st.table(sorted(found, key=custom_key))



# Run it: streamlit run .\file.py
