import streamlit as st
# from llm import agent


# Set app title and layout
st.set_page_config(page_title="Travel Planning Assistant", layout="wide")
st.title("🌍 Travel Planning Assistant")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("How can I help you with your travel plans?"):
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display assistant response
    with st.chat_message("assistant"):
        try:
            # Use LLM agent for response (Commented for now)
            # response = agent.run(prompt)
            
            # Constant placeholder response for now
            response = "🌟 I'm here to assist you with travel-related queries. For now, this is a placeholder response. 😊"

            st.markdown(response)
        except Exception as e:
            response = f"❗ Error: {e}"
            st.markdown(response)

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()
