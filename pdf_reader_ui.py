import streamlit as st
from llama_pdf_analyser import read_pdf, summarize_pdf, qa_session
from io import BytesIO
import time

# st.title("Hello human,")

welcome_msg = "Open the pages of your PDF and let's dive into the story together!"
welcome_msg2 = "Welcome to the PDF Reader – where every page is a new adventure, and every error message is a plot twist!"
st.header(welcome_msg)

st.write("\n")
upload_msg = "Got problems? Upload them here! Just like your ex's photos, PDF format works best for maximum drama! 😄"
pdf_file = st.file_uploader(upload_msg, type="PDF")

# file_uploaded = st.checkbox("upload file")
file_uploaded = st.button("upload file")

if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

if pdf_file is not None and (file_uploaded or st.session_state.file_uploaded):
    st.session_state.file_uploaded = True
   
    # Read the contents of the file
    pdf_txt = read_pdf(pdf_file)
    st.write("PDF uploaded successfully !")

    # Add a horizontal line
    st.markdown('<hr>', unsafe_allow_html=True)


    opn = st.selectbox("Select what you want us to do with the file ;)", options=["Do nothing", "Summarize", "Start a QA session"])
    st.write(f"You have selected to : {opn}")
    
    # Add a horizontal line
    st.markdown('<hr>', unsafe_allow_html=True)

    if opn == "Summarize":
        
        with st.spinner("summarizing the pdf so that you can relax 😉 ..."):
            summarized_txt = summarize_pdf(pdf_txt)
            # st.markdown('Summarized pdf content: </b>')
            st.write(summarized_txt)

    elif opn == "Start a QA session":
        
        st.write("Let us try to find the answers to your questions 😉 ")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # place = "Feel free to quiz me about your doc or simply bid me farewell, just like you did to your ex. 😄"
        # k = "Feel free to grill me about your doc or just give me the ol' ex goodbye treatment. 🤣"

        prompt = st.chat_input("Feel free to quiz me about your doc or simply bid me farewell, just like you did to your ex. 😄")
        
        if prompt:

            st.chat_message("user").markdown(prompt)
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            if prompt.lower() == "bye":
                with st.chat_message("assistant"):
                    st.write("Have a good day, you cute, lazy human :D")
                    # st.rerun()
                    exit()

            with st.spinner("Sit back, we are finding the answer for you"):
                response = qa_session(question=prompt, text_to_be_summarized=pdf_txt)

            def response_generator(response):
                for word in response.split():
                    yield word + " "
                    time.sleep(0.05)

            with st.chat_message("assistant"):
                # st.markdown(response)
                st.write_stream(response_generator(response))
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})

    elif opn == "do nothing":
        st.write("doing nothing")
    
   
    


