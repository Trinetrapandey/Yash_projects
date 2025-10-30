import streamlit as st
from document_processor import DocumentProcessor
from chat_engine import ChatEngine
from ui_components import UIComponents
from config import Config

def main():
    # Setup page config and custom CSS
    st.set_page_config(
        page_title="IntelliDoc Analyzer",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    UIComponents.setup_custom_css()
    UIComponents.render_main_header()
    
    # Initialize session state
    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = None
    if 'llm' not in st.session_state:
        st.session_state.llm = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'use_rag' not in st.session_state:
        st.session_state.use_rag = True
    
    # Initialize document processor
    doc_processor = DocumentProcessor()
    chat_engine = ChatEngine()
    
    def process_document_callback(uploaded_file, index_name):
        """Callback function for processing documents"""
        try:
            with st.spinner("Initializing AI Engine..."):
                pc, embeddings, llm = doc_processor.initialize_components()
                
            vectorstore = doc_processor.process_pdf(uploaded_file, index_name)
            st.session_state.vectorstore = vectorstore
            st.session_state.llm = llm
            st.session_state.processed = True
            st.session_state.uploaded_file = uploaded_file
            st.success("🎉 Document processed successfully!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
    
    # Main Layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎯 Analysis Mode")
        
        # Enhanced Mode Toggle
        st.markdown('<div class="mode-toggle">', unsafe_allow_html=True)
        if st.session_state.processed:
            current_mode = "🔍 **Context-Aware Mode**" if st.session_state.use_rag else "🤖 **General Knowledge Mode**"
            new_mode = "General Knowledge" if st.session_state.use_rag else "Context-Aware"
            
            if st.button(
                f"🔄 Switch to {new_mode} Mode",
                use_container_width=True,
                type="primary"
            ):
                st.session_state.use_rag = not st.session_state.use_rag
                st.rerun()
            
            st.markdown(f"**{current_mode}**")
            if st.session_state.use_rag:
                st.caption("🎯 Answers based on your document content")
            else:
                st.caption("💭 Answers from general AI knowledge")
        else:
            st.markdown("**🔍 Context-Aware Mode**")
            st.caption("🎯 Upload a document to enable smart analysis")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # System Status
        st.markdown("### 📊 System Status")
        if st.session_state.processed:
            st.markdown('<div class="status-card">✅ **AI Engine Active**</div>', unsafe_allow_html=True)
            st.markdown('<div class="status-card">📚 **Document Processed**</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="status-card">{"🔍 **RAG Enabled**" if st.session_state.use_rag else "🤖 **Direct AI Mode**"}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-card">⏳ **Ready for Document**</div>', unsafe_allow_html=True)
            st.markdown('<div class="status-card">🔍 **Context Mode Available**</div>', unsafe_allow_html=True)

    with col2:
        # Quick Stats Row
        if st.session_state.processed:
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.markdown('<div class="metric-card">📄<br>Document Ready</div>', unsafe_allow_html=True)
            with stat_col2:
                st.markdown('<div class="metric-card">🔍<br>Smart Analysis</div>', unsafe_allow_html=True)
            with stat_col3:
                mode_icon = "🎯" if st.session_state.use_rag else "🤖"
                st.markdown(f'<div class="metric-card">{mode_icon}<br>{"RAG" if st.session_state.use_rag else "AI"} Mode</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        uploaded_file, index_name = UIComponents.render_sidebar(
            st.session_state.uploaded_file,
            st.session_state.processed,
            st.session_state.use_rag,
            Config.DEFAULT_INDEX_NAME,
            process_document_callback
        )
        
        # Update session state with uploaded file
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
    
    # Main chat area
    if not st.session_state.processed:
        UIComponents.render_welcome_screen()
        return
    
    # Chat interface
    st.markdown("### 💬 Document Analysis Console")
    
    # Display chat messages with modern styling
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-user"><strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-assistant"><strong>Analyst:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
            if "mode" in message:
                with st.expander("🔍 Analysis Details"):
                    st.write(f"**Mode:** {message['mode']}")
                    if st.session_state.use_rag:
                        st.write("**Source:** Document Content")
                    else:
                        st.write("**Source:** General Knowledge")
    
    # Chat input
    st.markdown("---")
    if prompt := st.chat_input(f"Ask about your document... ({'Context Mode' if st.session_state.use_rag else 'AI Mode'})"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Analyzing content..." if st.session_state.use_rag else "🤖 Thinking..."):
                try:
                    if st.session_state.use_rag:
                        # Use RAG mode
                        answer, sources = chat_engine.answer_with_rag(
                            st.session_state.vectorstore,
                            st.session_state.llm,
                            prompt
                        )
                        response = f"{answer}\n\n---\n*🔍 Answer generated using document context*"
                    else:
                        # Use direct LLM mode
                        answer = chat_engine.answer_with_llm(st.session_state.llm, prompt)
                        response = f"{answer}\n\n---\n*🤖 Answer generated using general knowledge*"
                    
                    st.markdown(response)
                    
                    mode = "RAG" if st.session_state.use_rag else "LLM"
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "mode": mode
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

if __name__ == "__main__":
    main()