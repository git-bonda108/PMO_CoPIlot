# pmo_copilot_app.py
"""
PMO Agentic Copilot - AI-First Project Management Assistant
Enhanced Streamlit UI with Multi-Agent Support
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our PMO tools
from mock_jira_data import get_all_projects, get_project_summary, get_project, get_all_blockers, get_all_risks
from pmo_tools import (
    get_portfolio_overview,
    get_project_details,
    get_project_blockers,
    get_project_risks,
    calculate_project_evm,
    get_sprint_status,
    get_issue_breakdown,
    generate_escalation_report,
)
from demo_runner import PMOCoPilotDemo
from evm_calculator import calculate_evm, format_evm_report, get_evm_insights

# OpenAI Agents SDK integration
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flag to control AI mode
USE_OPENAI_AGENTS = os.getenv("OPENAI_API_KEY", "").startswith("sk-")

# Import agents if API key available
if USE_OPENAI_AGENTS:
    try:
        from pmo_copilot_agents import run_pmo_copilot
        AGENTS_SDK_AVAILABLE = True
    except ImportError as e:
        AGENTS_SDK_AVAILABLE = False
        print(f"OpenAI Agents SDK not available: {e}")
else:
    AGENTS_SDK_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="PMO Agentic Copilot - AI-First Project Management",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');
    
    /* Global Styles - Rich Deep Teal/Slate Theme */
    .stApp {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(145deg, #0f2027 0%, #203a43 40%, #2c5364 100%);
    }
    
    /* Hide default header */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Main Header with Animated Gradient */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00c9ff 0%, #92fe9d 25%, #00c9ff 50%, #f0f 75%, #00c9ff 100%);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 8s ease infinite;
        margin-bottom: 0;
        padding: 0.5rem 0;
        letter-spacing: -1px;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .sub-header {
        color: #a7c4bc;
        font-size: 1.2rem;
        margin-top: 0;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    /* Status Badges */
    .status-critical {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
        color: white;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.4);
    }
    .status-at-risk {
        background: linear-gradient(135deg, #feca57 0%, #ff9f43 100%);
        color: #1a1a2e;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        box-shadow: 0 0 20px rgba(254, 202, 87, 0.4);
    }
    .status-on-track {
        background: linear-gradient(135deg, #1dd1a1 0%, #10ac84 100%);
        color: white;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        box-shadow: 0 0 20px rgba(29, 209, 161, 0.4);
    }
    
    /* Report Container */
    .report-container {
        background: linear-gradient(180deg, rgba(32, 58, 67, 0.95) 0%, rgba(15, 32, 39, 0.98) 100%);
        border: 1px solid rgba(0, 201, 255, 0.25);
        border-radius: 1.25rem;
        padding: 1.75rem;
        margin: 1rem 0;
        color: #e8f4f8;
        font-family: 'Fira Code', monospace;
        font-size: 0.9rem;
        line-height: 1.7;
        max-height: 600px;
        overflow-y: auto;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
    }
    
    .report-container h1, .report-container h2, .report-container h3 {
        color: #5ee7df;
        border-bottom: 1px solid rgba(0, 201, 255, 0.25);
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    
    .report-container table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    
    .report-container th, .report-container td {
        border: 1px solid rgba(0, 201, 255, 0.2);
        padding: 0.6rem;
        text-align: left;
    }
    
    .report-container th {
        background: rgba(44, 83, 100, 0.8);
        color: #b8fff9;
    }
    
    /* Chat Messages */
    .chat-user {
        background: linear-gradient(135deg, rgba(44, 83, 100, 0.9) 0%, rgba(32, 58, 67, 0.85) 100%);
        border-left: 4px solid #00c9ff;
        padding: 1.25rem 1.5rem;
        border-radius: 0 1rem 1rem 0;
        margin: 0.85rem 0;
        color: #e8f4f8;
        box-shadow: 0 4px 20px rgba(0, 201, 255, 0.12);
    }
    
    .chat-ai {
        background: linear-gradient(135deg, rgba(29, 78, 95, 0.9) 0%, rgba(16, 69, 78, 0.85) 100%);
        border-left: 4px solid #1dd1a1;
        padding: 1.25rem 1.5rem;
        border-radius: 0 1rem 1rem 0;
        margin: 0.85rem 0;
        color: #e8f4f8;
        box-shadow: 0 4px 20px rgba(29, 209, 161, 0.12);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(44, 83, 100, 0.85) 0%, rgba(32, 58, 67, 0.75) 100%);
        border: 1px solid rgba(0, 201, 255, 0.3);
        border-radius: 1.25rem;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 60px rgba(0, 201, 255, 0.25);
        border-color: #00c9ff;
    }
    
    .metric-value {
        font-size: 2.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #5ee7df 0%, #b8fff9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #a7c4bc;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.5rem;
    }
    
    /* Project Cards */
    .project-card {
        background: linear-gradient(135deg, rgba(15, 32, 39, 0.9) 0%, rgba(32, 58, 67, 0.85) 100%);
        border: 1px solid rgba(94, 231, 223, 0.25);
        border-radius: 1.25rem;
        padding: 1.75rem;
        margin: 1rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
    }
    
    .project-card:hover {
        border-color: #5ee7df;
        box-shadow: 0 20px 60px rgba(94, 231, 223, 0.2);
        transform: translateY(-2px);
    }
    
    .project-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #e8f4f8;
        margin-bottom: 0.75rem;
    }
    
    /* Quick Action Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.6rem 1.25rem;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.35);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(6, 182, 212, 0.5);
    }
    
    /* Agent Button Styles */
    .agent-btn {
        background: linear-gradient(135deg, rgba(44, 83, 100, 0.85) 0%, rgba(32, 58, 67, 0.75) 100%);
        border: 1px solid rgba(0, 201, 255, 0.3);
        border-radius: 1rem;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .agent-btn:hover {
        border-color: #00c9ff;
        box-shadow: 0 0 30px rgba(0, 201, 255, 0.25);
        transform: translateX(5px);
    }
    
    .agent-btn.active {
        border-color: #5ee7df;
        background: linear-gradient(135deg, rgba(0, 201, 255, 0.2) 0%, rgba(94, 231, 223, 0.15) 100%);
        box-shadow: 0 0 30px rgba(94, 231, 223, 0.3);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(15, 32, 39, 0.85);
        padding: 0.75rem;
        border-radius: 1rem;
        border: 1px solid rgba(94, 231, 223, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 0.95rem;
        font-weight: 600;
        color: #a7c4bc;
        background: transparent;
        border-radius: 0.75rem;
        padding: 0.85rem 1.5rem;
        font-family: 'Outfit', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(44, 83, 100, 0.7);
        color: #e8f4f8;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%) !important;
        color: white !important;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.4);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #1a3a3a 100%);
        border-right: 1px solid rgba(94, 231, 223, 0.15);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e8f4f8;
    }
    
    /* Sidebar Agent Cards */
    .sidebar-agent {
        background: linear-gradient(135deg, rgba(44, 83, 100, 0.5) 0%, rgba(32, 58, 67, 0.4) 100%);
        border: 1px solid rgba(0, 201, 255, 0.2);
        border-radius: 0.85rem;
        padding: 0.85rem 1rem;
        margin: 0.6rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .sidebar-agent:hover {
        border-color: rgba(94, 231, 223, 0.5);
        background: linear-gradient(135deg, rgba(0, 201, 255, 0.15) 0%, rgba(94, 231, 223, 0.1) 100%);
        box-shadow: 0 4px 20px rgba(0, 201, 255, 0.15);
        transform: translateX(3px);
    }
    
    .sidebar-agent.active {
        border-color: #5ee7df;
        background: linear-gradient(135deg, rgba(0, 201, 255, 0.25) 0%, rgba(94, 231, 223, 0.15) 100%);
        box-shadow: 0 0 25px rgba(94, 231, 223, 0.25);
    }
    
    .agent-icon {
        font-size: 1.4rem;
        margin-right: 0.5rem;
    }
    
    .agent-name {
        font-weight: 600;
        font-size: 0.95rem;
        color: #e8f4f8;
    }
    
    .agent-desc {
        font-size: 0.75rem;
        color: #a7c4bc;
        margin-top: 0.25rem;
        line-height: 1.3;
    }
    
    /* Agent Badge */
    .agent-badge {
        display: inline-block;
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
        color: white;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.35);
    }
    
    /* Live Pulse Animation */
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #1dd1a1;
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(29, 209, 161, 0.7); }
        50% { opacity: 0.8; box-shadow: 0 0 0 10px rgba(29, 209, 161, 0); }
    }
    
    /* RAG Indicators */
    .rag-red { color: #ff6b6b; font-weight: bold; text-shadow: 0 0 10px rgba(255, 107, 107, 0.5); }
    .rag-amber { color: #feca57; font-weight: bold; text-shadow: 0 0 10px rgba(254, 202, 87, 0.5); }
    .rag-green { color: #1dd1a1; font-weight: bold; text-shadow: 0 0 10px rgba(29, 209, 161, 0.5); }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(32, 58, 67, 0.5);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #0891b2 0%, #06b6d4 100%);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #06b6d4 0%, #22d3ee 100%);
    }
    
    /* Data Tables */
    .stDataFrame {
        border-radius: 1rem;
        overflow: hidden;
        border: 1px solid rgba(0, 201, 255, 0.2);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(44, 83, 100, 0.7) 0%, rgba(32, 58, 67, 0.6) 100%);
        border-radius: 0.85rem;
        color: #e8f4f8;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(32, 58, 67, 0.85);
        border-color: rgba(0, 201, 255, 0.25);
        border-radius: 0.75rem;
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 1.25rem;
        padding: 1.5rem;
    }
    
    /* Glow Effect */
    .glow-teal {
        box-shadow: 0 0 40px rgba(94, 231, 223, 0.25);
    }
    
    .glow-cyan {
        box-shadow: 0 0 40px rgba(0, 201, 255, 0.25);
    }
    
    /* Text Input - DARK TEXT on white background */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 2px solid rgba(0, 201, 255, 0.4) !important;
        border-radius: 0.75rem;
        color: #1a1a2e !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00c9ff !important;
        box-shadow: 0 0 20px rgba(0, 201, 255, 0.25);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #666666 !important;
    }
    
    /* FORCE ALL MAIN CONTENT TEXT TO BE LIGHT */
    .stApp, .stApp * {
        color: #e8f4f8;
    }
    
    /* Main content area - all text light */
    [data-testid="stAppViewContainer"] {
        color: #e8f4f8 !important;
    }
    
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] div,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] td,
    [data-testid="stAppViewContainer"] th {
        color: #e8f4f8 !important;
    }
    
    /* Headings in main area */
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] h5,
    [data-testid="stAppViewContainer"] h6 {
        color: #5ee7df !important;
    }
    
    /* Markdown content */
    .stMarkdown, .stMarkdown * {
        color: #e8f4f8 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #5ee7df !important;
    }
    
    .stMarkdown strong {
        color: #b8fff9 !important;
    }
    
    .stMarkdown em {
        color: #a7c4bc !important;
    }
    
    .stMarkdown code {
        background: rgba(15, 32, 39, 0.95) !important;
        color: #5ee7df !important;
        padding: 0.25rem 0.5rem;
        border-radius: 0.35rem;
        border: 1px solid rgba(0, 201, 255, 0.3) !important;
        font-weight: 600;
    }
    
    .stMarkdown pre {
        background: rgba(15, 32, 39, 0.95) !important;
        border: 1px solid rgba(0, 201, 255, 0.3) !important;
        border-radius: 0.5rem;
    }
    
    .stMarkdown pre code {
        color: #e8f4f8 !important;
        background: transparent !important;
        border: none !important;
    }
    
    /* Table styling for markdown */
    .stMarkdown table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        background: rgba(15, 32, 39, 0.8) !important;
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    .stMarkdown th {
        background: rgba(6, 182, 212, 0.3) !important;
        color: #5ee7df !important;
        padding: 0.75rem 1rem;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid rgba(0, 201, 255, 0.3);
    }
    
    .stMarkdown td {
        background: rgba(15, 32, 39, 0.6) !important;
        color: #e8f4f8 !important;
        padding: 0.65rem 1rem;
        border-bottom: 1px solid rgba(0, 201, 255, 0.15);
    }
    
    .stMarkdown tr:hover td {
        background: rgba(6, 182, 212, 0.15) !important;
    }
    
    /* Code inside tables - ensure visibility */
    .stMarkdown td code {
        background: rgba(6, 182, 212, 0.25) !important;
        color: #b8fff9 !important;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
        border: 1px solid rgba(0, 201, 255, 0.4) !important;
        font-size: 0.9em;
    }
    
    /* Links */
    .stMarkdown a {
        color: #00c9ff !important;
    }
    
    /* Lists */
    .stMarkdown ul, .stMarkdown ol {
        color: #e8f4f8 !important;
    }
    
    .stMarkdown li {
        color: #e8f4f8 !important;
    }
    
    /* File uploader fix - DARK text on light background */
    [data-testid="stFileUploader"] button {
        color: #1a1a2e !important;
        background: #ffffff !important;
        border: 1px solid rgba(0, 201, 255, 0.4) !important;
    }
    
    [data-testid="stFileUploader"] button span {
        color: #1a1a2e !important;
    }
    
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] div,
    [data-testid="stFileUploader"] label {
        color: #1a1a2e !important;
    }
    
    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] {
        color: #1a1a2e !important;
    }
    
    /* Keep button text white */
    .stButton > button {
        color: white !important;
    }
    
    /* Selectbox dropdown */
    .stSelectbox label {
        color: #e8f4f8 !important;
    }
    
    /* Metric labels */
    [data-testid="stMetricLabel"] {
        color: #a7c4bc !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #5ee7df !important;
    }
    
    /* Tab content */
    [data-testid="stTabContent"] {
        color: #e8f4f8 !important;
    }
    
    [data-testid="stTabContent"] * {
        color: #e8f4f8 !important;
    }
    
    [data-testid="stTabContent"] h1,
    [data-testid="stTabContent"] h2,
    [data-testid="stTabContent"] h3,
    [data-testid="stTabContent"] h4 {
        color: #5ee7df !important;
    }
    
    /* Expander text */
    .streamlit-expanderHeader p {
        color: #e8f4f8 !important;
    }
    
    .streamlit-expanderContent {
        color: #e8f4f8 !important;
    }
    
    .streamlit-expanderContent * {
        color: #e8f4f8 !important;
    }
    
    /* DataFrame/Table */
    .stDataFrame {
        color: #e8f4f8 !important;
    }
    
    /* Chat input placeholder */
    .stTextInput input::placeholder {
        color: #7a9e9f !important;
    }
    
    /* Chat input styling - DARK TEXT on light background */
    [data-testid="stChatInput"] {
        background: #ffffff !important;
        border: 2px solid rgba(0, 201, 255, 0.5) !important;
        border-radius: 0.75rem !important;
    }
    
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] input,
    [data-testid="stChatInputTextArea"] {
        color: #1a1a2e !important;
        background: #ffffff !important;
        caret-color: #1a1a2e !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInput"] input::placeholder {
        color: #666666 !important;
    }
    
    /* Also fix regular text inputs */
    .stTextInput > div > div > input {
        color: #1a1a2e !important;
        background: #ffffff !important;
    }
    
    .stChatInput > div {
        background: #ffffff !important;
    }
    
    .stChatInput textarea {
        color: #1a1a2e !important;
        background: #ffffff !important;
    }
    
    /* Selectbox and dropdown styling */
    [data-testid="stSelectbox"] > div > div {
        background: rgba(15, 32, 39, 0.9) !important;
        color: #e8f4f8 !important;
        border-color: rgba(0, 201, 255, 0.3) !important;
    }
    
    [data-testid="stSelectbox"] span {
        color: #e8f4f8 !important;
    }
    
    /* Fix for combobox/dropdown text */
    .stSelectbox > div > div > div {
        color: #e8f4f8 !important;
    }
    
    /* Dropdown menu items */
    [data-baseweb="popover"] {
        background: rgba(15, 32, 39, 0.98) !important;
        border: 1px solid rgba(0, 201, 255, 0.3) !important;
    }
    
    [data-baseweb="popover"] li {
        color: #e8f4f8 !important;
    }
    
    [data-baseweb="popover"] li:hover {
        background: rgba(6, 182, 212, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'project_data' not in st.session_state:
    st.session_state.project_data = {}
if 'portfolio_loaded' not in st.session_state:
    st.session_state.portfolio_loaded = False
if 'demo' not in st.session_state:
    st.session_state.demo = PMOCoPilotDemo()
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = "auto"
if 'last_report' not in st.session_state:
    st.session_state.last_report = None
if 'agent_triggered' not in st.session_state:
    st.session_state.agent_triggered = False
if 'use_live_ai' not in st.session_state:
    st.session_state.use_live_ai = False  # Default to demo mode

# Get API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Agent definitions with descriptions
AGENTS = {
    "auto": {
        "icon": "🎯",
        "name": "Auto Orchestrator",
        "desc": "Intelligently routes your query to the best agent",
        "query": "help"
    },
    "status": {
        "icon": "📊",
        "name": "Status Report Agent",
        "desc": "Generates weekly/monthly status reports from project data",
        "query": "status"
    },
    "risk": {
        "icon": "⚠️",
        "name": "Risk Prediction Agent",
        "desc": "Analyzes risks, predicts delays & budget overruns",
        "query": "risks"
    },
    "escalation": {
        "icon": "🚨",
        "name": "Escalation Agent",
        "desc": "Identifies blockers & auto-escalates to stakeholders",
        "query": "escalate DPLAT"
    },
    "rag": {
        "icon": "🚦",
        "name": "RAG Reporter Agent",
        "desc": "Real-time Red/Amber/Green dashboard with AI insights",
        "query": "rag"
    },
    "steerco": {
        "icon": "📋",
        "name": "SteerCo Prep Agent",
        "desc": "Auto-generates executive summaries & talking points",
        "query": "steerco"
    },
    "evm": {
        "icon": "📈",
        "name": "EVM Analyst Agent",
        "desc": "Earned Value Management with variance analysis",
        "query": "evm"
    },
    "schedule": {
        "icon": "📅",
        "name": "Schedule Optimizer",
        "desc": "Optimizes timeline, dependencies & critical path",
        "query": "schedule"
    },
    "resource": {
        "icon": "👥",
        "name": "Resource Allocation",
        "desc": "Analyzes team capacity & workload distribution",
        "query": "resource"
    },
    "milestone": {
        "icon": "🎯",
        "name": "Milestone Guardian",
        "desc": "Tracks milestones & predicts delivery dates",
        "query": "milestone"
    },
    "predictive": {
        "icon": "🔮",
        "name": "Predictive Analytics",
        "desc": "ML-based forecasting & probability analysis",
        "query": "predict"
    },
    "ml_predict": {
        "icon": "🤖",
        "name": "ML Predictions",
        "desc": "XGBoost & Linear Regression cost/schedule forecasts",
        "query": "ml predictions"
    },
    "workflow": {
        "icon": "⚙️",
        "name": "Workflow Automation",
        "desc": "Analyzes bottlenecks & automation opportunities",
        "query": "workflow"
    }
}

def load_excel_to_json(uploaded_file):
    """Convert Excel file to JSON structure for AI processing"""
    excel_data = pd.ExcelFile(uploaded_file)
    project_data = {}
    for sheet in excel_data.sheet_names:
        df = pd.read_excel(excel_data, sheet_name=sheet)
        project_data[sheet] = df.to_dict(orient='records')
    return project_data

def get_health_emoji(health):
    """Get emoji for health status"""
    health_map = {
        "GREEN": "🟢",
        "AMBER": "🟡", 
        "RED": "🔴",
        "ON_TRACK": "🟢",
        "AT_RISK": "🟡",
        "CRITICAL": "🔴"
    }
    return health_map.get(health.upper(), "⚪")

def format_currency(amount):
    """Format number as currency"""
    return f"${amount:,.0f}"

def render_markdown_report(report_text):
    """Render a report in a styled container"""
    st.markdown(f'<div class="report-container">{report_text}</div>', unsafe_allow_html=True)

def get_ai_response(query, use_openai=True):
    """Get AI response using either OpenAI Agents SDK or demo mode"""
    
    # Check if we should use OpenAI Agents SDK
    if use_openai and AGENTS_SDK_AVAILABLE and st.session_state.get('use_live_ai', False):
        try:
            # Run async agent in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(run_pmo_copilot(query))
                return response
            finally:
                loop.close()
        except Exception as e:
            st.warning(f"OpenAI API error, falling back to demo mode: {str(e)[:100]}")
            # Fall back to demo mode
            demo = st.session_state.demo
            return demo.process_query(query)
    else:
        # Use demo mode (works without API)
        demo = st.session_state.demo
        return demo.process_query(query)

def trigger_agent(agent_key):
    """Trigger the selected agent and generate its report"""
    agent = AGENTS[agent_key]
    st.session_state.selected_agent = agent_key
    response = get_ai_response(agent["query"])
    st.session_state.chat_history.append({"role": "user", "content": f"[{agent['name']}] {agent['query']}"})
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.session_state.last_report = response
    st.session_state.agent_triggered = True

# Sidebar
with st.sidebar:
    # Logo and Title
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🚀</div>
        <div style='font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, #00c9ff 0%, #5ee7df 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>PMO Agentic Copilot</div>
        <div style='font-size: 0.85rem; color: #a7c4bc;'>AI-First Project Management</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Live Status
    # AI Mode indicator and toggle
    if AGENTS_SDK_AVAILABLE:
        ai_mode = st.toggle("🔥 Live AI Mode", value=st.session_state.use_live_ai, key="ai_mode_toggle")
        st.session_state.use_live_ai = ai_mode
        
        if ai_mode:
            st.markdown("""
            <div style='display: flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.5rem; background: rgba(255, 107, 107, 0.2); border-radius: 9999px; margin: 0.5rem 0;'>
                <div class='pulse-dot' style='background: #ff6b6b;'></div>
                <span style='color: #ff6b6b; font-size: 0.8rem; font-weight: 500;'>🔥 Live AI (GPT-4o)</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='display: flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.5rem; background: rgba(29, 209, 161, 0.15); border-radius: 9999px; margin: 0.5rem 0;'>
                <div class='pulse-dot'></div>
                <span style='color: #1dd1a1; font-size: 0.8rem; font-weight: 500;'>Demo Mode</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='display: flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.5rem; background: rgba(29, 209, 161, 0.15); border-radius: 9999px; margin: 0.5rem 0;'>
            <div class='pulse-dot'></div>
            <span style='color: #1dd1a1; font-size: 0.8rem; font-weight: 500;'>Demo Mode</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Agent Selection Section
    st.markdown("### 🤖 AI Agents")
    st.markdown("<p style='font-size: 0.8rem; color: #a7c4bc; margin-bottom: 1rem;'>Click an agent to run its analysis</p>", unsafe_allow_html=True)
    
    # Agent Cards as Buttons
    for agent_key, agent in AGENTS.items():
        is_active = st.session_state.selected_agent == agent_key
        active_class = "active" if is_active else ""
        
        # Create clickable agent card
        if st.button(
            f"{agent['icon']} {agent['name']}",
            key=f"agent_btn_{agent_key}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            trigger_agent(agent_key)
            st.rerun()
        
        # Show description below button
        st.markdown(f"<p style='font-size: 0.7rem; color: #7a9e9f; margin: -0.5rem 0 0.5rem 0.5rem;'>{agent['desc']}</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Project Quick Select
    st.markdown("### 📁 Project Portfolio")
    projects = get_project_summary()
    
    # Portfolio health summary
    red_count = sum(1 for p in projects if p['health'] == 'RED')
    amber_count = sum(1 for p in projects if p['health'] == 'AMBER')
    green_count = sum(1 for p in projects if p['health'] == 'GREEN')
    
    st.markdown(f"""
    <div style='display: flex; justify-content: space-around; padding: 0.75rem; background: rgba(44, 83, 100, 0.4); border-radius: 0.75rem; margin-bottom: 1rem;'>
        <div style='text-align: center;'>
            <div style='font-size: 1.5rem; font-weight: 700; color: #ff6b6b;'>{red_count}</div>
            <div style='font-size: 0.7rem; color: #a7c4bc;'>Critical</div>
        </div>
        <div style='text-align: center;'>
            <div style='font-size: 1.5rem; font-weight: 700; color: #feca57;'>{amber_count}</div>
            <div style='font-size: 0.7rem; color: #a7c4bc;'>At Risk</div>
        </div>
        <div style='text-align: center;'>
            <div style='font-size: 1.5rem; font-weight: 700; color: #1dd1a1;'>{green_count}</div>
            <div style='font-size: 0.7rem; color: #a7c4bc;'>On Track</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Project list
    for p in projects:
        health_emoji = get_health_emoji(p['health'])
        budget_pct = int(p['spent'] / p['budget'] * 100)
        st.markdown(f"""
        <div style='background: rgba(44, 83, 100, 0.35); border-radius: 0.6rem; padding: 0.6rem 0.75rem; margin: 0.4rem 0; border-left: 3px solid {"#ff6b6b" if p['health'] == "RED" else "#feca57" if p['health'] == "AMBER" else "#1dd1a1"};'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-weight: 600; color: #e8f4f8;'>{health_emoji} {p['project_key']}</span>
                <span style='font-size: 0.75rem; color: #a7c4bc;'>{budget_pct}% budget</span>
            </div>
            <div style='font-size: 0.75rem; color: #7a9e9f; margin-top: 0.2rem;'>{p['project_name'][:25]}...</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Upload Section
    st.markdown("### 📤 Data Import")
    uploaded_files = st.file_uploader(
        "Upload JIRA Exports",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        if st.button("🔄 Process Files", type="primary", use_container_width=True):
            with st.spinner("Processing..."):
                for file in uploaded_files:
                    project_name = file.name.replace('_Export.xlsx', '').replace('_', ' ')
                    st.session_state.project_data[project_name] = load_excel_to_json(file)
                st.session_state.portfolio_loaded = True
            st.success(f"✅ Loaded {len(uploaded_files)} projects!")

# Main content
st.markdown('<h1 class="main-header">🚀 PMO Agentic Copilot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">An AI-first PMO platform with 12 specialized agents that automate reporting, predict risks, and deliver executive insights in seconds.</p>', unsafe_allow_html=True)

# Show active agent indicator
if st.session_state.selected_agent != "auto":
    agent = AGENTS[st.session_state.selected_agent]
    st.markdown(f"""
    <div style='display: inline-flex; align-items: center; gap: 0.5rem; background: linear-gradient(135deg, rgba(0, 201, 255, 0.15) 0%, rgba(94, 231, 223, 0.1) 100%); padding: 0.5rem 1rem; border-radius: 9999px; border: 1px solid rgba(94, 231, 223, 0.4); margin-bottom: 1rem;'>
        <span style='font-size: 1.2rem;'>{agent['icon']}</span>
        <span style='color: #5ee7df; font-weight: 600;'>{agent['name']} Active</span>
    </div>
    """, unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "💬 AI Assistant", 
    "📊 Portfolio", 
    "🔍 Deep Dive", 
    "⚠️ Risks & Blockers", 
    "📈 EVM Analytics",
    "📊 Visualizations",
    "🤖 ML Predictions",
    "📋 Reports"
])

# TAB 1: AI Assistant
with tab1:
    st.markdown("### 💬 Chat with PMO Agentic Copilot")
    
    # Quick action buttons - 7 columns for handoff demo
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    quick_actions = [
        ("📊", "Portfolio", "portfolio overview"),
        ("🚨", "Blockers", "blockers"),
        ("⚠️", "Risks", "risks"),
        ("📋", "SteerCo", "steerco"),
        ("📈", "EVM", "evm"),
        ("🚦", "RAG", "rag dashboard"),
        ("🔄", "Handoff", "comprehensive multi-agent handoff analysis")
    ]
    
    for col, (icon, label, query) in zip([col1, col2, col3, col4, col5, col6, col7], quick_actions):
        with col:
            if st.button(f"{icon} {label}", use_container_width=True, key=f"btn_{label.lower()}"):
                response = get_ai_response(query)
                st.session_state.chat_history.append({"role": "user", "content": f"Generate {label} report"})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.session_state.last_report = response
                st.rerun()
    
    st.divider()
    
    # Two columns: Chat and Report
    chat_col, report_col = st.columns([1, 1])
    
    with chat_col:
        st.markdown("#### 💬 Conversation")
        
        # Chat container with scrolling
        chat_container = st.container(height=400)
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div style='text-align: center; padding: 2rem; color: #7a9e9f;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
                    <p style='font-size: 1.1rem; color: #a7c4bc;'>Welcome to PMO Agentic Copilot!</p>
                    <p style='font-size: 0.9rem;'>Click an agent in the sidebar or ask a question below.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.chat_history[-10:]:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-user">👤 <strong>You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
                    else:
                        content = msg["content"][:500] + "..." if len(msg["content"]) > 500 else msg["content"]
                        st.markdown(f'<div class="chat-ai">🤖 <strong>CoPilot:</strong> {content}</div>', unsafe_allow_html=True)
        
        # Chat input
        user_input = st.chat_input("Ask about projects... (e.g., 'Escalate DPLAT' or 'RAG dashboard')")
        
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            response = get_ai_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.session_state.last_report = response
            st.rerun()
    
    with report_col:
        st.markdown("#### 📄 Generated Report")
        if st.session_state.last_report:
            report_container = st.container(height=450)
            with report_container:
                st.markdown(st.session_state.last_report)
        else:
            st.markdown("""
            <div style='text-align: center; padding: 3rem; background: rgba(44, 83, 100, 0.35); border-radius: 1rem; border: 1px dashed rgba(0, 201, 255, 0.3);'>
                <div style='font-size: 2.5rem; margin-bottom: 1rem;'>📄</div>
                <p style='color: #a7c4bc;'>Click a quick action button or select an agent from the sidebar to generate a report</p>
            </div>
            """, unsafe_allow_html=True)

# TAB 2: Portfolio Dashboard
with tab2:
    st.markdown("### 📊 Portfolio Overview")
    
    # Get portfolio data
    projects = get_project_summary()
    all_projects = get_all_projects()
    
    # Portfolio metrics
    total_budget = sum(p['budget'] for p in projects)
    total_spent = sum(p['spent'] for p in projects)
    red_count = sum(1 for p in projects if p['health'] == 'RED')
    amber_count = sum(1 for p in projects if p['health'] == 'AMBER')
    green_count = sum(1 for p in projects if p['health'] == 'GREEN')
    
    # Metric cards
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        st.metric("Total Projects", len(projects))
    with m2:
        st.metric("🔴 Critical", red_count)
    with m3:
        st.metric("🟡 At Risk", amber_count)
    with m4:
        st.metric("🟢 On Track", green_count)
    with m5:
        st.metric("Budget Used", f"{total_spent/total_budget*100:.0f}%")
    
    st.divider()
    
    # Portfolio health chart
    col1, col2 = st.columns(2)
    
    with col1:
        # Health bar chart
        df_health = pd.DataFrame(projects)
        df_health['Health Score'] = df_health['health'].map({'GREEN': 85, 'AMBER': 60, 'RED': 30})
        
        fig = px.bar(
            df_health, 
            x='project_key', 
            y='Health Score',
            color='health',
            color_discrete_map={'RED': '#ef4444', 'AMBER': '#f59e0b', 'GREEN': '#10b981'},
            title='📊 Project Health Scores',
            labels={'project_key': 'Project', 'Health Score': 'Health Score'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8f4f8',
            title_font_color='#5ee7df',
            showlegend=False,
            xaxis=dict(tickfont=dict(color='#e8f4f8'), title_font=dict(color='#a7c4bc')),
            yaxis=dict(tickfont=dict(color='#e8f4f8'), title_font=dict(color='#a7c4bc'))
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Budget utilization
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Spent',
            x=[p['project_key'] for p in projects],
            y=[p['spent'] for p in projects],
            marker_color='#6366f1'
        ))
        fig.add_trace(go.Bar(
            name='Remaining',
            x=[p['project_key'] for p in projects],
            y=[p['budget'] - p['spent'] for p in projects],
            marker_color='#1e1b4b'
        ))
        fig.update_layout(
            barmode='stack',
            title='💰 Budget Utilization',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e8f4f8',
            title_font_color='#5ee7df',
            legend=dict(font=dict(color='#e8f4f8')),
            xaxis=dict(tickfont=dict(color='#e8f4f8'), title_font=dict(color='#a7c4bc')),
            yaxis=dict(tickfont=dict(color='#e8f4f8'), title_font=dict(color='#a7c4bc'))
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Project cards
    st.markdown("### 📁 Project Summary")
    
    for key, project in all_projects.items():
        health_emoji = get_health_emoji(project['health'])
        
        with st.expander(f"{health_emoji} **{project['project_name']}** ({key}) - {project['status']}", expanded=False):
            c1, c2, c3, c4 = st.columns(4)
            
            evm = project.get('evm', {})
            if evm:
                metrics = calculate_evm(evm)
                c1.metric("CPI", f"{metrics.CPI:.2f}", "Under Budget" if metrics.CPI >= 1 else "Over Budget")
                c2.metric("SPI", f"{metrics.SPI:.2f}", "On Schedule" if metrics.SPI >= 1 else "Behind")
            
            c3.metric("Blockers", len(project.get('blockers', [])))
            c4.metric("Risks", len(project.get('risks', [])))
            
            # Milestones
            st.markdown("**Milestones:**")
            for m in project.get('milestones', []):
                status_emoji = {"COMPLETED": "✅", "ON_TRACK": "🟢", "AT_RISK": "🟡", "NOT_STARTED": "⬜"}.get(m["status"], "❓")
                st.markdown(f"- {status_emoji} {m['name']} - Due: {m['due_date']} ({m['completion']}%)")

# TAB 3: Project Deep Dive
with tab3:
    st.markdown("### 🔍 Project Deep Dive")
    
    all_projects = get_all_projects()
    project_options = {f"{k} - {v['project_name']}": k for k, v in all_projects.items()}
    
    selected = st.selectbox("Select Project", list(project_options.keys()))
    project_key = project_options[selected]
    project = get_project(project_key)
    
    if project:
        # Project header
        health_emoji = get_health_emoji(project['health'])
        st.markdown(f"## {health_emoji} {project['project_name']}")
        st.markdown(f"**PM:** {project['project_manager']} | **Status:** {project['status']} | **Timeline:** {project['start_date']} to {project['planned_end_date']}")
        
        st.divider()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        evm = project.get('evm', {})
        if evm:
            metrics = calculate_evm(evm)
            col1.metric("Budget", format_currency(project['budget']))
            col2.metric("Spent", format_currency(project['spent']), f"{project['spent']/project['budget']*100:.0f}%")
            col3.metric("CPI", f"{metrics.CPI:.3f}")
            col4.metric("SPI", f"{metrics.SPI:.3f}")
        
        st.divider()
        
        # Issues breakdown
        tab_issues, tab_sprints, tab_team = st.tabs(["📋 Issues", "🏃 Sprints", "👥 Team"])
        
        with tab_issues:
            issues = project.get('issues', [])
            if issues:
                issues_df = pd.DataFrame(issues)
                
                col1, col2 = st.columns(2)
                with col1:
                    status_counts = issues_df['status'].value_counts()
                    fig = px.pie(values=status_counts.values, names=status_counts.index, title='Issues by Status',
                                 color_discrete_sequence=px.colors.qualitative.Set3)
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', 
                        paper_bgcolor='rgba(0,0,0,0)', 
                        font_color='#e8f4f8',
                        title_font_color='#5ee7df',
                        legend=dict(font=dict(color='#e8f4f8'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    priority_counts = issues_df['priority'].value_counts()
                    fig = px.pie(values=priority_counts.values, names=priority_counts.index, title='Issues by Priority',
                                 color_discrete_map={'Critical': '#ef4444', 'High': '#3b82f6', 'Medium': '#f59e0b', 'Low': '#10b981'})
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', 
                        paper_bgcolor='rgba(0,0,0,0)', 
                        font_color='#e8f4f8',
                        title_font_color='#5ee7df',
                        legend=dict(font=dict(color='#e8f4f8'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(issues_df[['key', 'type', 'summary', 'status', 'priority', 'assignee', 'story_points']], use_container_width=True)
        
        with tab_sprints:
            sprints = project.get('sprints', [])
            if sprints:
                sprints_df = pd.DataFrame(sprints)
                
                # Velocity chart
                completed_sprints = [s for s in sprints if s['velocity'] is not None]
                if completed_sprints:
                    fig = px.line(
                        x=[s['name'] for s in completed_sprints],
                        y=[s['velocity'] for s in completed_sprints],
                        markers=True,
                        title='📈 Velocity Trend'
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', 
                        paper_bgcolor='rgba(0,0,0,0)', 
                        font_color='#e8f4f8',
                        title_font_color='#5ee7df',
                        xaxis=dict(tickfont=dict(color='#e8f4f8'), title_font=dict(color='#a7c4bc')),
                        yaxis=dict(tickfont=dict(color='#e8f4f8'), title_font=dict(color='#a7c4bc'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(sprints_df, use_container_width=True)
        
        with tab_team:
            team = project.get('team', [])
            if team:
                team_df = pd.DataFrame(team)
                st.dataframe(team_df, use_container_width=True)

# TAB 4: Risks & Blockers
with tab4:
    st.markdown("### ⚠️ Risk & Blocker Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚨 Active Blockers")
        blockers = get_all_blockers()
        
        if blockers:
            for b in blockers:
                impact_color = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(b['impact'], "⚪")
                
                with st.container():
                    st.markdown(f"""
                    <div class="project-card">
                        <div class="project-title">{impact_color} [{b['project_key']}] {b['issue_key']}</div>
                        <p style='color: #94a3b8;'>{b['description']}</p>
                        <small style='color: #64748b;'>Blocked since: {b['blocked_since']} | Impact: {b['impact']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("🎉 No active blockers!")
    
    with col2:
        st.markdown("#### ⚠️ Risk Register")
        risks = get_all_risks()
        
        if risks:
            # Risk matrix
            risk_df = pd.DataFrame(risks)
            
            # Sort by severity
            prob_order = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
            impact_order = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
            risk_df['prob_score'] = risk_df['probability'].map(prob_order)
            risk_df['impact_score'] = risk_df['impact'].map(impact_order)
            risk_df['risk_score'] = risk_df['prob_score'] * risk_df['impact_score']
            risk_df = risk_df.sort_values('risk_score', ascending=False)
            
            for _, r in risk_df.head(6).iterrows():
                prob_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(r['probability'], "⚪")
                
                with st.expander(f"{prob_emoji} [{r['project_key']}] {r['id']}: {r['description'][:50]}..."):
                    st.markdown(f"**Probability:** {r['probability']}")
                    st.markdown(f"**Impact:** {r['impact']}")
                    st.markdown(f"**Mitigation:** {r['mitigation']}")

# TAB 5: EVM Analytics
with tab5:
    st.markdown("### 📈 Earned Value Management Analytics")
    
    all_projects = get_all_projects()
    
    # EVM comparison data
    evm_data = []
    for key, project in all_projects.items():
        evm = project.get('evm', {})
        if evm:
            metrics = calculate_evm(evm)
            evm_data.append({
                'Project': key,
                'BAC': metrics.BAC,
                'EV': metrics.EV,
                'AC': metrics.AC,
                'CPI': metrics.CPI,
                'SPI': metrics.SPI,
                'EAC': metrics.EAC,
                'VAC': metrics.VAC,
                'Health': metrics.overall_health
            })
    
    evm_df = pd.DataFrame(evm_data)
    
    # CPI/SPI Quadrant Chart
    fig = go.Figure()
    
    colors = {'GREEN': '#10b981', 'AMBER': '#f59e0b', 'RED': '#ef4444'}
    
    fig.add_trace(go.Scatter(
        x=evm_df['SPI'],
        y=evm_df['CPI'],
        mode='markers+text',
        text=evm_df['Project'],
        textposition='top center',
        marker=dict(
            size=30,
            color=[colors[h] for h in evm_df['Health']],
            line=dict(width=2, color='white')
        ),
        textfont=dict(color='#e8f4f8', size=12)
    ))
    
    # Add quadrant lines
    fig.add_hline(y=1.0, line_dash="dash", line_color="#06b6d4", annotation_text="CPI Target", annotation=dict(font=dict(color='#a7c4bc')))
    fig.add_vline(x=1.0, line_dash="dash", line_color="#06b6d4", annotation_text="SPI Target", annotation=dict(font=dict(color='#a7c4bc')))
    
    # Add quadrant labels
    fig.add_annotation(x=1.15, y=1.15, text="✅ Optimal", showarrow=False, font=dict(color="#1dd1a1", size=14))
    fig.add_annotation(x=0.75, y=1.15, text="⏰ Behind Schedule", showarrow=False, font=dict(color="#feca57", size=12))
    fig.add_annotation(x=1.15, y=0.75, text="💰 Over Budget", showarrow=False, font=dict(color="#feca57", size=12))
    fig.add_annotation(x=0.75, y=0.75, text="🔴 Critical", showarrow=False, font=dict(color="#ff6b6b", size=14))
    
    fig.update_layout(
        title='📊 CPI vs SPI Quadrant Analysis',
        xaxis_title='Schedule Performance Index (SPI)',
        yaxis_title='Cost Performance Index (CPI)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#e8f4f8',
        title_font_color='#5ee7df',
        legend=dict(font=dict(color='#e8f4f8')),
        xaxis=dict(range=[0.5, 1.3], tickfont=dict(color='#e8f4f8'), title_font=dict(color='#a7c4bc')),
        yaxis=dict(range=[0.5, 1.3], tickfont=dict(color='#e8f4f8'), title_font=dict(color='#a7c4bc'))
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # EVM metrics table
    st.markdown("#### 📊 EVM Metrics Summary")
    
    # Format for display
    display_df = evm_df.copy()
    display_df['BAC'] = display_df['BAC'].apply(lambda x: f"${x:,.0f}")
    display_df['EV'] = display_df['EV'].apply(lambda x: f"${x:,.0f}")
    display_df['AC'] = display_df['AC'].apply(lambda x: f"${x:,.0f}")
    display_df['EAC'] = display_df['EAC'].apply(lambda x: f"${x:,.0f}")
    display_df['VAC'] = display_df['VAC'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(display_df, use_container_width=True)
    
    # Individual project EVM
    st.markdown("#### 📈 Project EVM Details")
    selected_evm_project = st.selectbox("Select project for detailed EVM:", list(all_projects.keys()))
    
    if selected_evm_project:
        evm_report = calculate_project_evm(selected_evm_project)
        st.markdown(evm_report)

# TAB 6: Advanced Visualizations
with tab6:
    st.markdown("### 📊 Advanced Project Visualizations")
    
    viz_subtab1, viz_subtab2, viz_subtab3 = st.tabs(["📅 Gantt Chart", "🌡️ Resource Heatmap", "📉 Burn-down Chart"])
    
    all_projects = get_all_projects()
    
    # GANTT CHART TAB
    with viz_subtab1:
        st.markdown("#### 📅 Project Timeline - Gantt Chart")
        
        # Build Gantt data from milestones
        gantt_data = []
        colors_map = {'GREEN': '#10b981', 'AMBER': '#f59e0b', 'RED': '#ef4444'}
        
        for key, project in all_projects.items():
            milestones = project.get('milestones', [])
            health = project.get('health', 'GREEN')
            
            for milestone in milestones:
                # Parse dates
                try:
                    start_date = pd.to_datetime(project.get('start_date', '2025-01-01'))
                    end_date = pd.to_datetime(milestone.get('due_date', '2025-12-31'))
                    
                    gantt_data.append({
                        'Task': f"[{key}] {milestone.get('name', 'Milestone')}",
                        'Start': start_date,
                        'Finish': end_date,
                        'Project': key,
                        'Status': milestone.get('status', 'IN_PROGRESS'),
                        'Progress': milestone.get('progress', 0),
                        'Health': health
                    })
                except:
                    pass
        
        if gantt_data:
            gantt_df = pd.DataFrame(gantt_data)
            
            # Create Gantt chart using Plotly
            fig_gantt = px.timeline(
                gantt_df, 
                x_start="Start", 
                x_end="Finish", 
                y="Task",
                color="Project",
                hover_data=['Status', 'Progress'],
                title="Portfolio Timeline - All Projects",
                color_discrete_map={
                    'ECOM': '#06b6d4',
                    'MAPP': '#10b981',
                    'DPLAT': '#ef4444',
                    'SECU': '#8b5cf6'
                }
            )
            
            fig_gantt.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#e8f4f8',
                title_font_color='#5ee7df',
                legend=dict(font=dict(color='#e8f4f8')),
                xaxis=dict(
                    tickfont=dict(color='#a7c4bc'),
                    title_font=dict(color='#5ee7df'),
                    gridcolor='rgba(94, 231, 223, 0.1)'
                ),
                yaxis=dict(
                    tickfont=dict(color='#a7c4bc'),
                    title_font=dict(color='#5ee7df'),
                    gridcolor='rgba(94, 231, 223, 0.1)'
                ),
                height=500
            )
            
            fig_gantt.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_gantt, use_container_width=True)
            
            # Gantt summary
            st.markdown("#### 📊 Timeline Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Milestones", len(gantt_data))
            completed = len([g for g in gantt_data if g['Status'] == 'COMPLETED'])
            col2.metric("Completed", completed)
            in_progress = len([g for g in gantt_data if g['Status'] == 'IN_PROGRESS'])
            col3.metric("In Progress", in_progress)
            at_risk = len([g for g in gantt_data if g['Status'] == 'AT_RISK'])
            col4.metric("At Risk", at_risk, delta="⚠️" if at_risk > 0 else None)
        else:
            st.info("No milestone data available for Gantt chart")
    
    # RESOURCE HEATMAP TAB
    with viz_subtab2:
        st.markdown("#### 🌡️ Resource Allocation Heatmap")
        
        # Build resource allocation matrix
        resource_data = []
        
        for key, project in all_projects.items():
            team = project.get('team', [])
            for member in team:
                resource_data.append({
                    'Resource': member.get('name', 'Unknown'),
                    'Project': key,
                    'Role': member.get('role', 'Unknown'),
                    'Allocation': member.get('allocation', 100)
                })
        
        if resource_data:
            resource_df = pd.DataFrame(resource_data)
            
            # Pivot for heatmap
            heatmap_df = resource_df.pivot_table(
                index='Resource', 
                columns='Project', 
                values='Allocation', 
                aggfunc='sum',
                fill_value=0
            )
            
            # Create heatmap
            fig_heatmap = px.imshow(
                heatmap_df.values,
                x=heatmap_df.columns.tolist(),
                y=heatmap_df.index.tolist(),
                color_continuous_scale=[
                    [0, '#1e3a4a'],      # Low allocation - dark
                    [0.5, '#06b6d4'],    # Medium - cyan
                    [0.75, '#f59e0b'],   # High - amber
                    [1, '#ef4444']       # Over-allocated - red
                ],
                aspect='auto',
                title="Resource Allocation by Project (%)"
            )
            
            fig_heatmap.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#e8f4f8',
                title_font_color='#5ee7df',
                xaxis=dict(tickfont=dict(color='#a7c4bc'), title='Project'),
                yaxis=dict(tickfont=dict(color='#a7c4bc'), title='Resource'),
                height=500
            )
            
            # Add text annotations
            fig_heatmap.update_traces(
                text=heatmap_df.values,
                texttemplate="%{text}%",
                textfont={"size": 12, "color": "#ffffff"}
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Resource utilization summary
            st.markdown("#### 📊 Resource Utilization Summary")
            
            total_by_resource = resource_df.groupby('Resource')['Allocation'].sum().reset_index()
            total_by_resource.columns = ['Resource', 'Total Allocation']
            
            # Categorize
            total_by_resource['Status'] = total_by_resource['Total Allocation'].apply(
                lambda x: '🔴 Over-allocated' if x > 100 else ('🟢 Optimal' if x >= 80 else '🟡 Under-utilized')
            )
            
            col1, col2, col3 = st.columns(3)
            over_alloc = len(total_by_resource[total_by_resource['Total Allocation'] > 100])
            optimal = len(total_by_resource[(total_by_resource['Total Allocation'] >= 80) & (total_by_resource['Total Allocation'] <= 100)])
            under_util = len(total_by_resource[total_by_resource['Total Allocation'] < 80])
            
            col1.metric("🔴 Over-allocated", over_alloc)
            col2.metric("🟢 Optimal (80-100%)", optimal)
            col3.metric("🟡 Under-utilized", under_util)
            
            # Show table
            st.dataframe(
                total_by_resource.style.map(
                    lambda x: 'color: #ef4444' if '🔴' in str(x) else ('color: #10b981' if '🟢' in str(x) else 'color: #f59e0b'),
                    subset=['Status']
                ),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No resource data available for heatmap")
    
    # BURN-DOWN CHART TAB
    with viz_subtab3:
        st.markdown("#### 📉 Sprint Burn-down Chart")
        
        # Select project for burn-down
        burndown_project = st.selectbox("Select Project:", list(all_projects.keys()), key="burndown_project")
        
        if burndown_project:
            project = all_projects[burndown_project]
            sprints = project.get('sprints', [])
            
            if sprints:
                # Get latest sprint
                current_sprint = sprints[-1] if sprints else None
                
                if current_sprint:
                    st.markdown(f"**Current Sprint:** {current_sprint.get('name', 'Sprint')}")
                    
                    # Generate burn-down data (simulated for demo)
                    sprint_days = 10
                    total_points = current_sprint.get('total_points', 40)
                    completed = current_sprint.get('completed_points', 25)
                    
                    # Ideal burn-down line
                    ideal_burndown = [total_points - (total_points / sprint_days) * day for day in range(sprint_days + 1)]
                    
                    # Actual burn-down (simulated with some variance)
                    import random
                    random.seed(42)  # Consistent results
                    actual_burndown = [total_points]
                    remaining = total_points
                    for day in range(1, sprint_days + 1):
                        if day <= 7:  # Assuming we're on day 7
                            daily_completion = random.uniform(2, 6)
                            remaining = max(0, remaining - daily_completion)
                            actual_burndown.append(remaining)
                        else:
                            actual_burndown.append(None)  # Future days
                    
                    # Create burn-down chart
                    days = list(range(sprint_days + 1))
                    
                    fig_burndown = go.Figure()
                    
                    # Ideal line
                    fig_burndown.add_trace(go.Scatter(
                        x=days,
                        y=ideal_burndown,
                        mode='lines',
                        name='Ideal',
                        line=dict(color='#5ee7df', dash='dash', width=2)
                    ))
                    
                    # Actual line
                    fig_burndown.add_trace(go.Scatter(
                        x=days[:len([a for a in actual_burndown if a is not None])],
                        y=[a for a in actual_burndown if a is not None],
                        mode='lines+markers',
                        name='Actual',
                        line=dict(color='#06b6d4', width=3),
                        marker=dict(size=8, color='#06b6d4')
                    ))
                    
                    # Add scope line
                    fig_burndown.add_trace(go.Scatter(
                        x=days,
                        y=[total_points] * len(days),
                        mode='lines',
                        name='Scope',
                        line=dict(color='#f59e0b', dash='dot', width=1)
                    ))
                    
                    fig_burndown.update_layout(
                        title=f"Sprint Burn-down: {current_sprint.get('name', 'Sprint')}",
                        xaxis_title="Sprint Day",
                        yaxis_title="Story Points Remaining",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='#e8f4f8',
                        title_font_color='#5ee7df',
                        legend=dict(font=dict(color='#e8f4f8')),
                        xaxis=dict(
                            tickfont=dict(color='#a7c4bc'),
                            title_font=dict(color='#5ee7df'),
                            gridcolor='rgba(94, 231, 223, 0.1)'
                        ),
                        yaxis=dict(
                            tickfont=dict(color='#a7c4bc'),
                            title_font=dict(color='#5ee7df'),
                            gridcolor='rgba(94, 231, 223, 0.1)'
                        ),
                        height=400
                    )
                    
                    st.plotly_chart(fig_burndown, use_container_width=True)
                    
                    # Sprint metrics
                    st.markdown("#### 📊 Sprint Metrics")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    col1.metric("Total Points", total_points)
                    col2.metric("Completed", completed)
                    col3.metric("Remaining", total_points - completed)
                    velocity = current_sprint.get('velocity')
                    if velocity is None:
                        velocity = completed / 0.7 if completed > 0 else 0  # Estimate based on progress
                    col4.metric("Velocity", f"{velocity:.1f} pts/sprint")
                    
                    # Velocity trend
                    st.markdown("#### 📈 Velocity Trend")
                    
                    velocity_data = []
                    for sprint in sprints:
                        velocity_data.append({
                            'Sprint': sprint.get('name', 'Sprint'),
                            'Velocity': sprint.get('velocity', sprint.get('completed_points', 0))
                        })
                    
                    if velocity_data:
                        vel_df = pd.DataFrame(velocity_data)
                        
                        fig_velocity = px.bar(
                            vel_df,
                            x='Sprint',
                            y='Velocity',
                            title='Team Velocity Trend',
                            color_discrete_sequence=['#06b6d4']
                        )
                        
                        # Add average line
                        avg_velocity = vel_df['Velocity'].mean()
                        fig_velocity.add_hline(
                            y=avg_velocity,
                            line_dash="dash",
                            line_color="#5ee7df",
                            annotation_text=f"Avg: {avg_velocity:.1f}",
                            annotation_font_color="#5ee7df"
                        )
                        
                        fig_velocity.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='#e8f4f8',
                            title_font_color='#5ee7df',
                            xaxis=dict(tickfont=dict(color='#a7c4bc')),
                            yaxis=dict(tickfont=dict(color='#a7c4bc')),
                            height=300
                        )
                        
                        st.plotly_chart(fig_velocity, use_container_width=True)
            else:
                st.info("No sprint data available for this project")

# TAB 7: ML Predictions
with tab7:
    st.markdown("### 🤖 ML-Powered Predictions")
    st.markdown("*Using Linear Regression & XGBoost for forecasting*")
    
    # Try to import ML models
    try:
        from ml_models import (
            get_full_ml_prediction,
            get_feature_importance,
            EVMFeatureExtractor,
            ML_AVAILABLE,
            XGBOOST_AVAILABLE
        )
        ml_available = True
    except ImportError:
        ml_available = False
        st.warning("ML models not available. Install scikit-learn and optionally xgboost for full functionality.")
    
    if ml_available:
        # Model info
        col1, col2, col3 = st.columns(3)
        col1.metric("ML Library", "✅ Available" if ML_AVAILABLE else "⚠️ Fallback")
        col2.metric("XGBoost", "✅ Available" if XGBOOST_AVAILABLE else "⚠️ Using GradientBoosting")
        col3.metric("Models Trained", "5 Active")
        
        # Project selector
        all_projects = get_all_projects()
        ml_project = st.selectbox("Select Project for ML Analysis:", list(all_projects.keys()), key="ml_project")
        
        if ml_project:
            project = all_projects[ml_project]
            
            with st.spinner("Running ML predictions..."):
                predictions = get_full_ml_prediction(project)
                features = predictions['features']
            
            # Display predictions in columns
            st.markdown("#### 📈 EVM Input Features")
            feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
            feat_col1.metric("CPI", f"{features['cpi']:.2f}", 
                           delta=f"{'Good' if features['cpi'] >= 1 else 'Under'}")
            feat_col2.metric("SPI", f"{features['spi']:.2f}",
                           delta=f"{'Good' if features['spi'] >= 1 else 'Behind'}")
            feat_col3.metric("% Complete", f"{features['percent_complete']:.1f}%")
            feat_col4.metric("Risk Score", f"{features['risk_score']:.1f}")
            
            # Prediction results in tabs
            pred_tab1, pred_tab2, pred_tab3, pred_tab4, pred_tab5 = st.tabs([
                "💰 Cost Forecast", 
                "📅 Schedule", 
                "⚠️ Risk Level",
                "👥 Resources",
                "🔥 Burn Rate"
            ])
            
            # Cost Forecast Tab
            with pred_tab1:
                cost = predictions['cost_forecast']
                st.markdown("##### 💰 Cost Forecast (XGBoost Model)")
                
                cost_col1, cost_col2 = st.columns(2)
                with cost_col1:
                    st.metric("Predicted Final Cost", f"${cost['predicted_cost']:,.0f}")
                    st.metric("Budget (BAC)", f"${features['bac']:,.0f}")
                    overrun_color = "🔴" if cost['cost_overrun_pct'] > 10 else ("🟡" if cost['cost_overrun_pct'] > 0 else "🟢")
                    st.metric("Cost Overrun", f"{overrun_color} {cost['cost_overrun_pct']:+.1f}%")
                
                with cost_col2:
                    st.metric("Confidence", f"{cost['confidence']:.0f}%")
                    st.metric("Lower Bound", f"${cost['lower_bound']:,.0f}")
                    st.metric("Upper Bound", f"${cost['upper_bound']:,.0f}")
                
                # Cost prediction gauge
                fig_cost = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=cost['predicted_cost'],
                    delta={'reference': features['bac'], 'relative': True, 'valueformat': '.1%'},
                    title={'text': "Predicted vs Budget", 'font': {'color': '#e8f4f8'}},
                    gauge={
                        'axis': {'range': [0, cost['upper_bound'] * 1.1], 'tickcolor': '#a7c4bc'},
                        'bar': {'color': '#06b6d4'},
                        'bgcolor': 'rgba(0,0,0,0)',
                        'bordercolor': 'rgba(0,201,255,0.3)',
                        'steps': [
                            {'range': [0, features['bac']], 'color': 'rgba(16, 185, 129, 0.3)'},
                            {'range': [features['bac'], cost['upper_bound'] * 1.1], 'color': 'rgba(239, 68, 68, 0.3)'}
                        ],
                        'threshold': {
                            'line': {'color': '#5ee7df', 'width': 4},
                            'thickness': 0.75,
                            'value': features['bac']
                        }
                    }
                ))
                fig_cost.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8f4f8',
                    height=300
                )
                st.plotly_chart(fig_cost, use_container_width=True)
            
            # Schedule Forecast Tab
            with pred_tab2:
                schedule = predictions['schedule_forecast']
                st.markdown("##### 📅 Schedule Forecast (Linear Regression)")
                
                sched_col1, sched_col2 = st.columns(2)
                with sched_col1:
                    status_color = "🟢" if schedule['status'] == 'ON_TRACK' else ("🟡" if schedule['status'] == 'AT_RISK' else "🔴")
                    st.metric("Status", f"{status_color} {schedule['status']}")
                    st.metric("Predicted Delay", f"{schedule['delay_days']:.0f} days")
                
                with sched_col2:
                    st.metric("On-Time Probability", f"{schedule['on_time_probability']:.0f}%")
                    st.metric("Confidence", f"{schedule['confidence']:.0f}%")
                
                # On-time probability bar
                fig_sched = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=schedule['on_time_probability'],
                    title={'text': "On-Time Probability", 'font': {'color': '#e8f4f8'}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickcolor': '#a7c4bc'},
                        'bar': {'color': '#06b6d4'},
                        'steps': [
                            {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                            {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.3)'},
                            {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
                        ]
                    }
                ))
                fig_sched.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#e8f4f8', height=300)
                st.plotly_chart(fig_sched, use_container_width=True)
            
            # Risk Classification Tab
            with pred_tab3:
                risk = predictions['risk_classification']
                st.markdown("##### ⚠️ Risk Classification (XGBoost)")
                
                risk_color = "🔴" if risk['risk_level'] == 'HIGH' else ("🟡" if risk['risk_level'] == 'MEDIUM' else "🟢")
                st.metric("Risk Level", f"{risk_color} {risk['risk_level']}")
                st.metric("Confidence", f"{risk['confidence']:.0f}%")
                
                # Probability pie chart
                prob_data = risk['probabilities']
                fig_risk = go.Figure(data=[go.Pie(
                    labels=['HIGH', 'MEDIUM', 'LOW'],
                    values=[prob_data.get('HIGH', 0), prob_data.get('MEDIUM', 0), prob_data.get('LOW', 0)],
                    marker_colors=['#ef4444', '#f59e0b', '#10b981'],
                    hole=0.4
                )])
                fig_risk.update_layout(
                    title={'text': 'Risk Probability Distribution', 'font': {'color': '#5ee7df'}},
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8f4f8',
                    legend=dict(font=dict(color='#e8f4f8')),
                    height=300
                )
                st.plotly_chart(fig_risk, use_container_width=True)
            
            # Resource Forecast Tab
            with pred_tab4:
                resource = predictions['resource_forecast']
                st.markdown("##### 👥 Resource Forecast (Linear Regression)")
                
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.metric("Current Team", f"{resource['current_team']} FTEs")
                    st.metric("Recommended", f"{resource['required_ftes']:.1f} FTEs")
                
                with res_col2:
                    delta_val = resource['delta']
                    delta_icon = "➕" if delta_val > 0 else ("➖" if delta_val < 0 else "✅")
                    st.metric("Delta", f"{delta_icon} {delta_val:+.1f}")
                    st.metric("Action", resource['recommendation'])
                
                # Resource comparison bar
                fig_res = go.Figure(data=[
                    go.Bar(name='Current', x=['Team Size'], y=[resource['current_team']], marker_color='#06b6d4'),
                    go.Bar(name='Recommended', x=['Team Size'], y=[resource['required_ftes']], marker_color='#5ee7df')
                ])
                fig_res.update_layout(
                    barmode='group',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8f4f8',
                    legend=dict(font=dict(color='#e8f4f8')),
                    height=250
                )
                st.plotly_chart(fig_res, use_container_width=True)
            
            # Burn Rate Tab
            with pred_tab5:
                burn = predictions['burn_rate_forecast']
                st.markdown("##### 🔥 Burn Rate Forecast (XGBoost)")
                
                burn_col1, burn_col2 = st.columns(2)
                with burn_col1:
                    st.metric("Predicted Monthly Burn", f"${burn['predicted_monthly_burn']:,.0f}")
                    st.metric("Budgeted Burn", f"${burn['budgeted_burn']:,.0f}")
                
                with burn_col2:
                    var_color = "🔴" if burn['variance_pct'] > 10 else ("🟡" if burn['variance_pct'] > 0 else "🟢")
                    st.metric("Variance", f"{var_color} {burn['variance_pct']:+.1f}%")
                    st.metric("Runway", f"{burn['runway_months']:.1f} months")
            
            # Feature Importance Section
            st.markdown("#### 🎯 Feature Importance (What Drives Predictions)")
            
            importance = get_feature_importance()
            
            imp_col1, imp_col2 = st.columns(2)
            
            with imp_col1:
                st.markdown("**Cost Model Drivers**")
                cost_imp = importance['cost_model']
                fig_imp_cost = go.Figure(go.Bar(
                    y=list(cost_imp.keys()),
                    x=list(cost_imp.values()),
                    orientation='h',
                    marker_color='#06b6d4'
                ))
                fig_imp_cost.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8f4f8',
                    xaxis=dict(tickformat='.0%', tickfont=dict(color='#a7c4bc')),
                    yaxis=dict(tickfont=dict(color='#a7c4bc')),
                    height=250,
                    margin=dict(l=100, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_imp_cost, use_container_width=True)
            
            with imp_col2:
                st.markdown("**Schedule Model Drivers**")
                sched_imp = importance['schedule_model']
                fig_imp_sched = go.Figure(go.Bar(
                    y=list(sched_imp.keys()),
                    x=list(sched_imp.values()),
                    orientation='h',
                    marker_color='#5ee7df'
                ))
                fig_imp_sched.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e8f4f8',
                    xaxis=dict(tickformat='.0%', tickfont=dict(color='#a7c4bc')),
                    yaxis=dict(tickfont=dict(color='#a7c4bc')),
                    height=250,
                    margin=dict(l=100, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_imp_sched, use_container_width=True)
    
    else:
        st.info("ML models require scikit-learn. The demo mode will show sample predictions.")
        # Show demo mode content
        demo = st.session_state.demo
        ml_report = demo._ml_predictions_agent(None)
        st.markdown(ml_report)

# TAB 8: Reports
with tab8:
    st.markdown("### 📋 Report Generator")
    
    report_type = st.selectbox(
        "Select Report Type:",
        [
            "📊 Portfolio Status Report",
            "⚠️ Risk Analysis Report",
            "🚨 Escalation Report",
            "🚦 RAG Dashboard",
            "📋 SteerCo Package",
            "📈 EVM Analysis Report"
        ]
    )
    
    project_filter = st.selectbox(
        "Project (optional):",
        ["All Projects"] + list(get_all_projects().keys())
    )
    
    if st.button("🚀 Generate Report", type="primary", use_container_width=True):
        with st.spinner("Generating report..."):
            demo = st.session_state.demo
            
            if "Portfolio" in report_type:
                report = demo.process_query("portfolio status")
            elif "Risk" in report_type:
                query = f"risks {project_filter}" if project_filter != "All Projects" else "risks"
                report = demo.process_query(query)
            elif "Escalation" in report_type:
                query = f"escalate {project_filter}" if project_filter != "All Projects" else "escalate DPLAT"
                report = demo.process_query(query)
            elif "RAG" in report_type:
                report = demo.process_query("rag dashboard")
            elif "SteerCo" in report_type:
                report = demo.process_query("steerco")
            elif "EVM" in report_type:
                query = f"evm {project_filter}" if project_filter != "All Projects" else "evm"
                report = demo.process_query(query)
            else:
                report = demo.process_query("portfolio")
            
            st.session_state.last_report = report
        
        # Display report
        st.markdown(report)
        
        # Download button
        st.download_button(
            "📥 Download Report",
            report,
            file_name=f"pmo_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown"
        )

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, rgba(44, 83, 100, 0.4) 0%, rgba(32, 58, 67, 0.3) 100%); border-radius: 1rem; margin-top: 2rem;'>
    <p style='font-size: 1.2rem; color: #5ee7df; margin-bottom: 0.5rem;'>🚀 <strong>PMO Agentic Copilot</strong></p>
    <p style='font-size: 0.95rem; color: #a7c4bc;'>AI-First Project Management • OpenAI Agents SDK • Multi-Agent Architecture</p>
    <div style='display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;'>
        <span class='agent-badge'>Status Reports</span>
        <span class='agent-badge'>Risk Prediction</span>
        <span class='agent-badge'>EVM Analytics</span>
        <span class='agent-badge'>SteerCo Prep</span>
    </div>
    <p style='font-size: 0.8rem; color: #7a9e9f; margin-top: 1rem;'>PMO CoPilot — Multi-Agent Project Intelligence</p>
</div>
""", unsafe_allow_html=True)
