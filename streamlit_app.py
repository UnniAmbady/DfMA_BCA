import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot -->🍎")
st.write("Chatbot on DfMA ")

context = """
        [Building and Construction Authority (BCA), Singapore Building Regulations, and DfMA]
        [You are an intelligent assistant trained to provide detailed and 
        accurate information about "Design for Manufacturing and Assembly (DFMA)" principles, 
        as outlined by the Building and Construction Authority (BCA) of Singapore.]
        [Here is information directly from the official BCA DFMA website:
        "https://www1.bca.gov.sg/buildsg/productivity/design-for-manufacturing-and-assembly-dfma]
        [Based on the above information, answer the following question from the user:]      
        """
suffix = "Please provide a concise and clear response not exceeding 100 words."
# Ask user for their OpenAI API key via `st.text_input`.

# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
#openai_api_key = st.text_input("OpenAI API Key", type="password")

openai_api_key = st.secrets["openai"]["secret_key"]
client = OpenAI(api_key=openai_api_key)

if not client:
    st.info("API Key is missing.", icon="🗝️")
else:

    # OpenAI client already exists
    # client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": context+prompt+suffix}) #concat 3 things
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
