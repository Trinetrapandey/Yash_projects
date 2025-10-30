import streamlit as st

class UIComponents:
    """UI components and styling for the application"""
    
    @staticmethod
    def setup_custom_css():
        """Setup custom CSS styling"""
        st.markdown("""
        <style>
            /* Main styling */
            .main-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 3rem 2rem;
                border-radius: 20px;
                margin-bottom: 2rem;
                color: white;
                text-align: center;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            }
            
            .analysis-card {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                margin-bottom: 1.5rem;
                border-left: 5px solid #667eea;
                transition: transform 0.2s ease;
            }
            
            .analysis-card:hover {
                transform: translateY(-2px);
            }
            
            .status-card {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 12px;
                margin: 0.8rem 0;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 15px;
                padding: 3rem 2rem;
                text-align: center;
                background: #f8faff;
                margin: 1.5rem 0;
                transition: all 0.3s ease;
            }
            
            .upload-area:hover {
                background: #f0f4ff;
                border-color: #5a6fd8;
            }
            
            .mode-toggle {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 15px;
                text-align: center;
                color: white;
                margin: 1.5rem 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .chat-user {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.2rem 1.5rem;
                border-radius: 20px 20px 5px 20px;
                margin: 1rem 0 1rem 4rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                border: none;
            }
            
            .chat-assistant {
                background: #ffffff;
                padding: 1.2rem 1.5rem;
                border-radius: 20px 20px 20px 5px;
                margin: 1rem 4rem 1rem 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                border-left: 4px solid #667eea;
            }
            
            .metric-card {
                background: white;
                padding: 1.2rem;
                border-radius: 12px;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
                text-align: center;
                margin: 0.8rem;
                border-top: 4px solid #667eea;
            }
            
            .stButton button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0.8rem 1.5rem;
                width: 100%;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .stButton button:hover {
                background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            }
            
            .sidebar-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 1.5rem;
            }
            
            /* Custom file uploader */
            .stFileUploader > div > div {
                border: 3px dashed #667eea !important;
                border-radius: 15px !important;
                background: #f8faff !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_main_header():
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1 style="margin:0; font-size: 3rem; font-weight: 700;">🚀 IntelliDoc Analyzer</h1>
            <p style="margin:0; font-size: 1.3rem; opacity: 0.95;">AI-Powered Document Intelligence with Smart RAG Technology</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_welcome_screen():
        """Render the welcome screen"""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem;">
                <h1 style="font-size: 4rem;">📄</h1>
                <h2>Welcome to IntelliDoc Analyzer</h2>
                <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
                    Upload a PDF document to unlock AI-powered analysis and intelligent conversations with your content.
                </p>
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           color: white; padding: 2rem; border-radius: 15px;">
                    <h3>🚀 Get Started</h3>
                    <ol style="text-align: left; color: white;">
                        <li>Upload a PDF using the sidebar</li>
                        <li>Click "Process Document"</li>
                        <li>Start asking questions about your content</li>
                    </ol>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_sidebar(uploaded_file, processed, use_rag, index_name, process_callback):
        """Render the sidebar components"""
        st.markdown('<div class="sidebar-header"><h2>⚙️ Control Center</h2></div>', unsafe_allow_html=True)
        
        # File upload section
        st.markdown("### 📁 Document Upload")
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drag & Drop PDF File",
            type="pdf",
            help="Upload your document for AI analysis",
            label_visibility="collapsed"
        )
        st.markdown("""
        <div style="text-align: center; color: #666; margin-top: 1rem;">
            <span style="font-size: 3rem;">📄</span><br>
            <strong>Drop PDF Here</strong><br>
            <small>or click to browse</small>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            st.success(f"**{uploaded_file.name}** ready for processing!")
        
        # Processing section
        st.markdown("### 🚀 Processing")
        index_name = st.text_input(
            "Knowledge Base Name",
            value=index_name,
            help="Name for your document knowledge base"
        )
        
        process_disabled = uploaded_file is None or processed
        
        if st.button("🚀 Process Document", 
                    disabled=process_disabled, 
                    use_container_width=True,
                    type="primary",
                    key="process_btn"):
            process_callback(uploaded_file, index_name)
        
        # Status section
        if processed:
            st.markdown("### ✅ Status")
            st.success("**Document Ready for Analysis!**")
            st.info(f"**Current Mode:** {'🔍 RAG' if use_rag else '🤖 LLM'}")
        
        st.markdown("---")
        
        # Management section
        st.markdown("### 🔧 Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("📤 New Doc", use_container_width=True):
                st.session_state.vectorstore = None
                st.session_state.llm = None
                st.session_state.messages = []
                st.session_state.processed = False
                st.session_state.uploaded_file = None
                st.rerun()
        
        return uploaded_file, index_name