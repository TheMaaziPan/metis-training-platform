import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import datetime
import json
import os
import random

# Configure the page
st.set_page_config(
    page_title="MediaVision Metis Training",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match Metis design language
st.markdown("""
<style>
    /* Main colors */
    :root {
        --metis-purple: #7B68EE;
        --metis-light-purple: #9685F0;
        --metis-dark-purple: #1E1640;
        --metis-bg: #F8F9FA;
        --metis-text: #2B2D42;
        --metis-light-text: #6C757D;
        --metis-card-bg: #FFFFFF;
    }
    
    /* General styling */
    .stApp {
        background-color: var(--metis-bg);
    }
    
    /* Header styling */
    .main-header {
        color: var(--metis-text);
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 0;
    }
    
    .sub-header {
        color: var(--metis-light-text);
        font-size: 16px;
        margin-top: 0;
        margin-bottom: 20px;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1ram643 {
        background-color: var(--metis-dark-purple);
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--metis-purple);
        color: white;
        border-radius: 20px;
        padding: 8px 16px;
        border: none;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: var(--metis-light-purple);
    }
    
    .secondary-button>button {
        background-color: transparent;
        color: var(--metis-purple);
        border: 1px solid var(--metis-purple);
    }
    
    /* Card styling */
    .metis-card {
        background-color: var(--metis-card-bg);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: var(--metis-purple);
    }
    
    /* Custom table styling */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
    }
    
    .styled-table thead tr {
        background-color: var(--metis-purple);
        color: #ffffff;
        text-align: left;
    }
    
    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
    }
    
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f9f9f9;
    }

    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid var(--metis-purple);
    }
    
    .styled-table tbody tr.active-row {
        background-color: #f0ebff;
    }
    
    /* Input fields */
    div[data-baseweb="input"] {
        border-radius: 8px;
    }
    
    /* User profile */
    .user-profile {
        display: flex;
        align-items: center;
    }
    
    .user-profile img {
        border-radius: 50%;
        margin-right: 10px;
    }
    
    /* Badge styles */
    .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        margin-left: 8px;
    }
    
    .badge-employee {
        background-color: #0075FF;
    }
    
    .badge-partner {
        background-color: #FF7A00;
    }
    
    .badge-customer {
        background-color: #00C853;
    }
    
    /* Role icon card */
    .role-card {
        background-color: white;
        border-radius: 16px;
        padding: 30px;
        margin: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .role-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    .role-icon {
        font-size: 40px;
        margin-bottom: 15px;
    }
    
    /* Learning path */
    .path-step {
        display: flex;
        margin-bottom: 20px;
    }
    
    .path-number {
        background-color: var(--metis-purple);
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        flex-shrink: 0;
    }
    
    .path-content {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        flex-grow: 1;
    }
    
    /* Quiz styling */
    .quiz-question {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    /* Video container */
    .video-container {
        position: relative;
        padding-bottom: 56.25%; /* 16:9 ratio */
        height: 0;
        overflow: hidden;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    .video-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = {
        'name': "",
        'role': "",
        'company': "",
        'email': "",
        'progress': 0,
        'completed_modules': []
    }
    st.session_state.current_course = None
    st.session_state.current_module = None
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.quiz_active = False
    st.session_state.quiz_score = 0
    st.session_state.quiz_total = 0

# Mock user data
class User:
    def __init__(self, name, role, user_type, company="", email="", progress=0):
        self.name = name
        self.role = role
        self.user_type = user_type
        self.company = company
        self.email = email
        self.progress = progress
        self.completed_modules = []

# Mock course data - Base courses available to all users
base_courses = [
    {
        "id": 1,
        "title": "Introduction to Metis",
        "description": "Learn the basics of the Metis platform and its key features.",
        "for_user_types": ["employee", "partner", "customer"],
        "modules": [
            {"id": 1, "title": "What is Metis?", "duration": "10 min"},
            {"id": 2, "title": "Navigating the Dashboard", "duration": "15 min"},
            {"id": 3, "title": "Understanding Key Metrics", "duration": "20 min"}
        ]
    }
]

# Employee-specific courses
employee_courses = [
    {
        "id": 101,
        "title": "Metis Administration",
        "description": "Learn how to manage Metis settings, users, and advanced configurations.",
        "for_user_types": ["employee"],
        "modules": [
            {"id": 1, "title": "User Management", "duration": "30 min"},
            {"id": 2, "title": "System Configuration", "duration": "45 min"},
            {"id": 3, "title": "Data Pipeline Management", "duration": "50 min"}
        ]
    },
    {
        "id": 102,
        "title": "Client Onboarding",
        "description": "Learn the process for setting up new clients on the Metis platform.",
        "for_user_types": ["employee"],
        "modules": [
            {"id": 1, "title": "Initial Client Setup", "duration": "25 min"},
            {"id": 2, "title": "Data Integration", "duration": "40 min"},
            {"id": 3, "title": "Client Training Sessions", "duration": "35 min"}
        ]
    }
]

# Partner-specific courses
partner_courses = [
    {
        "id": 201,
        "title": "Metis API Integration",
        "description": "Learn how to integrate Metis with your own systems via our API.",
        "for_user_types": ["partner"],
        "modules": [
            {"id": 1, "title": "API Overview", "duration": "20 min"},
            {"id": 2, "title": "Authentication", "duration": "15 min"},
            {"id": 3, "title": "Data Endpoints", "duration": "35 min"},
            {"id": 4, "title": "Webhook Implementation", "duration": "40 min"}
        ]
    },
    {
        "id": 202,
        "title": "Partner Go-to-Market Strategy",
        "description": "Learn how to effectively market and sell Metis as a partner.",
        "for_user_types": ["partner"],
        "modules": [
            {"id": 1, "title": "Metis Value Proposition", "duration": "25 min"},
            {"id": 2, "title": "Target Customer Profiles", "duration": "30 min"},
            {"id": 3, "title": "Sales Process", "duration": "40 min"}
        ]
    }
]

# Customer-specific courses
customer_courses = [
    {
        "id": 301,
        "title": "Category Monitoring Masterclass",
        "description": "Master the Category Monitoring tools to improve organic visibility.",
        "for_user_types": ["customer"],
        "modules": [
            {"id": 1, "title": "Category Overview", "duration": "15 min"},
            {"id": 2, "title": "Filtering and Analysis", "duration": "25 min"},
            {"id": 3, "title": "Optimization Techniques", "duration": "30 min"}
        ]
    },
    {
        "id": 302,
        "title": "Product Visibility Optimization",
        "description": "Learn how to boost onsite visibility of products using Metis tools.",
        "for_user_types": ["customer"],
        "modules": [
            {"id": 1, "title": "Product Visibility Basics", "duration": "20 min"},
            {"id": 2, "title": "Position Analysis", "duration": "25 min"},
            {"id": 3, "title": "Visibility Optimization", "duration": "35 min"}
        ]
    },
    {
        "id": 303,
        "title": "Category Merchandising",
        "description": "Maximize revenue through effective onsite merchandising strategies.",
        "for_user_types": ["customer"],
        "modules": [
            {"id": 1, "title": "Merchandising Fundamentals", "duration": "20 min"},
            {"id": 2, "title": "Opportunity Scoring", "duration": "30 min"},
            {"id": 3, "title": "Revenue Optimization", "duration": "40 min"}
        ]
    }
]

# Combined courses for all user types (will be filtered based on user type)
all_courses = base_courses + employee_courses + partner_courses + customer_courses

# Module content - a simple dictionary to store content for each module
module_content = {
    # Intro course content
    "1-1": {
        "title": "What is Metis?",
        "content": """
        ## What is Metis?
        
        Metis is MediaVision's proprietary e-commerce analytics and optimization platform that unlocks the potential of market data to create a competitive edge for clients.
        
        ### Core Functionality
        
        Metis is an e-commerce optimization platform that helps you to understand what people want and when they want it. It makes tailored daily recommendations based on market data and your website to inform business decisions 4x faster than your competitors.
        
        The platform provides a central source of insight into weekly organic demand data. It pulls this data into tailored daily recommendations to improve business performance.
        
        ### Key Components
        
        Metis operates through three main processes:
        
        1. **Insight**: Understanding consumer confidence, brand health and growth opportunities based on your specific vertical.
        
        2. **Optimize**: Activating on those insights at scale across teams to maximize the potential of your search channel.
        
        3. **Convert**: Daily merchandising insights at category and product level to ensure the most relevant products are the most visible to the right customer at the right time.
        
        ### Who Uses Metis
        
        Metis adds value across the organization:
        
        - **Buyers**: Inform product buying, range building, new product development
        - **Merchandisers**: Inform sales planning decisions, delivery timetables, trading windows
        - **Trading Teams**: Support daily site trading, category creation, page creation
        - **Digital and Marketing Teams**: Deliver sitewide recommendations for quick wins
        - **C-Suite**: Access to unique data to support investment decisions
        """,
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",  # Placeholder
        "has_quiz": True,
        "quiz": [
            {
                "question": "What is the primary purpose of Metis?",
                "options": [
                    "Social media management",
                    "E-commerce analytics and optimization",
                    "Content creation",
                    "Email marketing"
                ],
                "correct": 1
            },
            {
                "question": "How much faster does Metis help inform business decisions compared to competitors?",
                "options": [
                    "2x faster",
                    "3x faster",
                    "4x faster",
                    "5x faster"
                ],
                "correct": 2
            },
            {
                "question": "Which of these is NOT one of the three main processes of Metis?",
                "options": [
                    "Insight",
                    "Optimize",
                    "Convert",
                    "Design"
                ],
                "correct": 3
            }
        ]
    },
    "1-2": {
        "title": "Navigating the Dashboard",
        "content": """
        ## Navigating the Dashboard
        
        The Metis dashboard provides a comprehensive overview of your e-commerce performance and opportunities. This module will help you understand the layout and key elements of the Metis interface.
        
        ### Dashboard Layout
        
        The Metis interface consists of:
        
        1. **Navigation Sidebar**: Access different modules and features
        2. **Main Content Area**: View data, charts, and recommendations
        3. **Filter Controls**: Refine the data displayed
        4. **Action Panel**: Take immediate actions based on insights
        
        ### Key Dashboard Elements
        
        When you log into Metis, you'll see several important elements:
        
        - **Performance Summary**: Top-level metrics showing your current performance
        - **Trend Charts**: Visualizations of key metrics over time
        - **Recommendations**: AI-generated suggestions for optimization
        - **Category & Product Insights**: Detailed data on your catalog performance
        
        ### Navigation Tips
        
        To get the most out of the Metis dashboard:
        
        - Use the date range filters to analyze specific time periods
        - Save custom views for frequently accessed reports
        - Set up alerts for significant changes in key metrics
        - Export data for further analysis or sharing with your team
        """,
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",  # Placeholder
        "has_quiz": True,
        "quiz": [
            {
                "question": "What is NOT a component of the Metis dashboard layout?",
                "options": [
                    "Navigation Sidebar",
                    "Main Content Area",
                    "Code Editor",
                    "Filter Controls"
                ],
                "correct": 2
            },
            {
                "question": "What can you use to analyze specific time periods in Metis?",
                "options": [
                    "Date range filters",
                    "Time machine",
                    "Calendar integration",
                    "Scheduling tool"
                ],
                "correct": 0
            }
        ]
    },
    # Add more module content as needed
    "301-1": {
        "title": "Category Overview",
        "content": """
        ## Category Monitoring Overview
        
        The Category Monitoring tool in Metis helps you track and improve the organic visibility of your Product Listing Pages (PLPs).
        
        ### Key Features
        
        Category Monitoring provides:
        
        - Tracking of inbound and outbound links
        - Monitoring of SEO performance
        - Identification of optimization opportunities
        - Product counts and page titles
        - SEO metrics and link performance
        
        ### Daily Recommendations
        
        The system provides daily view of every category on the website, with recommendations for optimization:
        
        - Improves traffic and revenue from SEO
        - Embeds best practice SEO in the ways of working
        - Reduces time spent uncovering opportunities manually
        - Analyzes category performance at scale
        - Highlights over 50 ecommerce optimization issues daily including low stock categories
        
        ### Practical Application
        
        Category Monitoring helps merchandisers:
        
        - Inform planning decisions
        - Set delivery timetables
        - Establish trading windows
        - Develop taxonomy and categorization
        """,
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",  # Placeholder
        "has_quiz": True,
        "quiz": [
            {
                "question": "What does the Category Monitoring tool help track?",
                "options": [
                    "Social media posts",
                    "Organic visibility of Product Listing Pages",
                    "Email open rates",
                    "Website uptime"
                ],
                "correct": 1
            },
            {
                "question": "How many e-commerce optimization issues can Metis highlight daily?",
                "options": [
                    "Up to 20",
                    "Up to 30",
                    "Over 50",
                    "Over 100"
                ],
                "correct": 2
            }
        ]
    },
    "102-1": {
        "title": "Initial Client Setup",
        "content": """
        ## Initial Client Setup Process
        
        This module covers the step-by-step process for setting up new clients on the Metis platform, a critical skill for all employees involved in client onboarding.
        
        ### Pre-onboarding Preparation
        
        Before beginning the client setup:
        
        1. Collect necessary client information (website URLs, Google Analytics access, etc.)
        2. Identify key stakeholders at the client organization
        3. Schedule initial kickoff call
        4. Prepare client workspace in the Metis admin panel
        
        ### Creating Client Account
        
        To create a new client in the Metis system:
        
        1. Navigate to Admin > Clients > Add New Client
        2. Complete the required fields (Company name, Industry, Main contact, etc.)
        3. Set up user access levels for client team members
        4. Configure data collection parameters
        5. Set billing and subscription details
        
        ### Initial Configuration
        
        After creating the account:
        
        1. Set up category mapping to align with client's website structure
        2. Configure custom KPIs and metrics important to the client
        3. Set up initial dashboards and reports
        4. Establish data refresh schedules
        
        ### Client Documentation
        
        Finally, prepare documentation for the client:
        
        1. Create client-specific quick start guide
        2. Document any custom configurations
        3. Prepare training schedule for client team
        """,
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",  # Placeholder
        "has_quiz": True,
        "quiz": [
            {
                "question": "What section of the admin panel do you use to add a new client?",
                "options": [
                    "Users > Add New",
                    "Clients > Add New Client",
                    "Accounts > Create",
                    "Setup > New Organization"
                ],
                "correct": 1
            },
            {
                "question": "What should be collected before beginning client setup?",
                "options": [
                    "Client credit card details",
                    "Social media accounts",
                    "Website URLs and Google Analytics access",
                    "Employee personal information"
                ],
                "correct": 2
            }
        ]
    },
    "201-1": {
        "title": "API Overview",
        "content": """
        ## Metis API Overview
        
        This module introduces partners to the Metis API, enabling integration with your own systems and applications.
        
        ### API Architecture
        
        The Metis API is built as a RESTful service with:
        
        - JSON-based data exchange
        - OAuth 2.0 authentication
        - Rate limiting of 1000 requests per hour
        - Versioned endpoints (current stable: v2)
        
        ### Available Resources
        
        The API provides access to key Metis data:
        
        1. **Analytics Data**
           - Brand performance metrics
           - Market demand insights
           - Competitive benchmarks
        
        2. **Category Data**
           - Category visibility scores
           - Optimization recommendations
           - Cross-linking opportunities
        
        3. **Product Data**
           - Product visibility metrics
           - Position analysis
           - Merchandising opportunities
        
        ### Integration Workflows
        
        Common integration patterns include:
        
        - Scheduled data synchronization
        - Real-time alerting on metrics
        - Automated reporting systems
        - Custom dashboard creation
        
        ### Getting Started
        
        To begin using the API:
        
        1. Register for API access in your partner portal
        2. Generate API credentials
        3. Review the API documentation
        4. Start with the sandbox environment
        """,
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",  # Placeholder
        "has_quiz": True,
        "quiz": [
            {
                "question": "What authentication method does the Metis API use?",
                "options": [
                    "Basic Auth",
                    "API Keys",
                    "OAuth 2.0",
                    "JWT Tokens"
                ],
                "correct": 2
            },
            {
                "question": "What is the rate limit for the Metis API?",
                "options": [
                    "100 requests per hour",
                    "500 requests per hour",
                    "1000 requests per hour",
                    "Unlimited requests"
                ],
                "correct": 2
            }
        ]
    },
    "302-1": {
        "title": "Product Visibility Basics",
        "content": """
        ## Product Visibility Basics
        
        The Product Visibility tool helps you analyze and optimize how products appear on your website.
        
        ### Key Features
        
        - Track product positions within categories
        - Monitor clicks and conversion rates
        - Identify underperforming products
        - Optimize placement for better results
        
        This tool is essential for merchandisers looking to maximize product visibility and sales.
        """,
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",  # Placeholder
        "has_quiz": True,
        "quiz": [
            {
                "question": "What does the Product Visibility tool help track?",
                "options": [
                    "Social media posts",
                    "Product positions within categories",
                    "Email open rates",
                    "Website uptime"
                ],
                "correct": 1
            },
            {
                "question": "Which team would benefit most from the Product Visibility tool?",
                "options": [
                    "HR team",
                    "IT support",
                    "Merchandisers",
                    "Accounting"
                ],
                "correct": 2
            }
        ]
    },
    "302-2": {
        "title": "Position Analysis",
        "content": """
        ## Position Analysis in Metis
        
        Position Analysis is a critical component of product visibility optimization that helps you understand how your products are performing based on their placement within category pages.
        
        ### Understanding Position Metrics
        
        In Metis, position analysis provides several key insights:
        
        1. **Position Distribution**: See where your products are positioned across all categories
        2. **Position vs. Performance**: Analyze how position impacts clicks and conversion
        3. **Historical Tracking**: Monitor position changes over time
        4. **Competitive Benchmarking**: Compare your product positioning with competitors
        
        ### Practical Application
        
        Using position analysis data, you can:
        
        - Identify products that need better placement
        - Quantify the impact of position changes on revenue
        - Create data-driven merchandising strategies
        - Prioritize which products to reposition first
        
        ### Case Study: Position Impact
        
        In a typical e-commerce store, products in positions 1-4 receive approximately 80% of all clicks. Products beyond position 20 receive almost no visibility. Metis helps you identify these opportunities and prioritize your merchandising efforts.
        """,
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",  # Placeholder
        "has_quiz": True,
        "quiz": [
            {
                "question": "What percentage of clicks do products in positions 1-4 typically receive?",
                "options": [
                    "About 50%",
                    "About 65%",
                    "About 80%",
                    "About 95%"
                ],
                "correct": 2
            },
            {
                "question": "Which of the following is NOT a component of Position Analysis in Metis?",
                "options": [
                    "Position Distribution",
                    "Position vs. Performance",
                    "Social Media Integration",
                    "Historical Tracking"
                ],
                "correct": 2
            }
        ]
    }
}

# Get courses available for the current user type
def get_available_courses(user_type):
    return [course for course in all_courses if user_type in course["for_user_types"]]

# Authentication page
def login_page():
    st.markdown('<h1 class="main-header">MediaVision Metis Training Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Login to access your training modules</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="metis-card">', unsafe_allow_html=True)
        st.markdown("### Login")
        username = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username and password:  # In a real app, check credentials
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Please enter email and password")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metis-card">', unsafe_allow_html=True)
        st.markdown("### Welcome to the Metis Training Platform")
        st.markdown("""
        This platform will help you master the Metis tools for e-commerce optimization:
        
        - Learn at your own pace
        - Interactive tutorials and quizzes
        - Track your progress
        - Earn certifications
        
        Get started by logging in with your MediaVision credentials.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Select user type page
def select_user_type():
    st.markdown('<h1 class="main-header">Select Your Role</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Choose your role to access relevant training content</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="role-card" onclick="document.getElementById('employee-button').click()">
            <div class="role-icon">👨‍💼</div>
            <h3>Employee</h3>
            <p>MediaVision staff training</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Employee", key="employee-button", help="For MediaVision employees"):
            st.session_state.user_type = "employee"
            # Set dummy user data for employee
            st.session_state.user = User(
                name="Alex Johnson",
                role="Implementation Specialist",
                user_type="employee",
                company="MediaVision",
                email="alex.johnson@mediavision.com",
                progress=35
            )
            st.experimental_rerun()
    
    with col2:
        st.markdown("""
        <div class="role-card" onclick="document.getElementById('partner-button').click()">
            <div class="role-icon">🤝</div>
            <h3>Partner</h3>
            <p>Integration and reseller training</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Partner", key="partner-button", help="For business partners and integrators"):
            st.session_state.user_type = "partner"
            # Set dummy user data for partner
            st.session_state.user = User(
                name="Sam Rodriguez",
                role="Integration Manager",
                user_type="partner",
                company="Digital Solutions Inc.",
                email="sam@digitalsolutions.com",
                progress=15
            )
            st.experimental_rerun()
    
    with col3:
        st.markdown("""
        <div class="role-card" onclick="document.getElementById('customer-button').click()">
            <div class="role-icon">🛒</div>
            <h3>Customer</h3>
            <p>E-commerce platform training</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Customer", key="customer-button", help="For Metis platform users"):
            st.session_state.user_type = "customer"
            # Set dummy user data for customer
            st.session_state.user = User(
                name="Nigel Thompson",
                role="Website Content Editor",
                user_type="customer",
                company="Fashion Retailer Ltd",
                email="nigel.thompson@fashionretailer.com",
                progress=22
            )
            st.experimental_rerun()

# Course catalog page
def course_catalog():
    st.markdown('<h1 class="main-header">Course Catalog</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Select a course to begin or continue your training</p>', unsafe_allow_html=True)
    
    # Get courses for the current user type
    available_courses = get_available_courses(st.session_state.user_type)
    
    # Progress overview
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown("### Your Learning Progress")
    st.progress(st.session_state.user.progress / 100)
    st.markdown(f"You've completed **{st.session_state.user.progress}%** of the available training material.")
    
    # Recommended courses
    if st.session_state.user.progress < 30:
        st.markdown("#### Recommended Next Steps")
        st.markdown("Complete the Introduction to Metis course to understand platform basics.")
    elif st.session_state.user.progress < 60:
        st.markdown("#### Recommended Next Steps")
        st.markdown("Explore role-specific courses to deepen your Metis expertise.")
    else:
        st.markdown("#### Recommended Next Steps")
        st.markdown("Complete advanced courses and earn your Metis certification.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Course grid - organized by course type/function
    st.markdown("### Getting Started")
    
    # Filter for introductory courses
    intro_courses = [c for c in available_courses if c["id"] < 100]
    create_course_grid(intro_courses)
    
    # Role-specific courses header
    if st.session_state.user_type == "employee":
        st.markdown("### Employee Courses")
        role_courses = [c for c in available_courses if 100 <= c["id"] < 200]
        create_course_grid(role_courses)
    elif st.session_state.user_type == "partner":
        st.markdown("### Partner Courses")
        role_courses = [c for c in available_courses if 200 <= c["id"] < 300]
        create_course_grid(role_courses)
    elif st.session_state.user_type == "customer":
        st.markdown("### Platform Mastery")
        role_courses = [c for c in available_courses if 300 <= c["id"] < 400]
        create_course_grid(role_courses)
        
    # Learning path section
    st.markdown("### Suggested Learning Path")
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    
    if st.session_state.user_type == "employee":
        st.markdown("#### Employee Certification Path")
        st.markdown("""
        Follow this recommended sequence to become a certified Metis Implementation Specialist:
        """)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">1</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Introduction to Metis</strong><br>Learn the basic concepts and navigation.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">2</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Metis Administration</strong><br>Master the admin tools and configurations.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">3</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Client Onboarding</strong><br>Learn the process for setting up new clients.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">4</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Advanced Configuration</strong><br>Deep dive into advanced settings and customizations.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif st.session_state.user_type == "partner":
        st.markdown("#### Partner Certification Path")
        st.markdown("""
        Follow this recommended sequence to become a certified Metis Integration Partner:
        """)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">1</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Introduction to Metis</strong><br>Learn the basic concepts and navigation.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">2</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Metis API Integration</strong><br>Master the API endpoints and authentication.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">3</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Partner Go-to-Market Strategy</strong><br>Learn how to position and sell Metis.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">4</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Integration Case Studies</strong><br>Real-world examples of successful integrations.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif st.session_state.user_type == "customer":
        st.markdown("#### Customer Certification Path")
        st.markdown("""
        Follow this recommended sequence to become a certified Metis Platform Expert:
        """)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">1</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Introduction to Metis</strong><br>Learn the basic concepts and navigation.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">2</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Category Monitoring Masterclass</strong><br>Master the Category Monitoring tools.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">3</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Product Visibility Optimization</strong><br>Learn to optimize product visibility.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="path-step">', unsafe_allow_html=True)
        st.markdown('<div class="path-number">4</div>', unsafe_allow_html=True)
        st.markdown('<div class="path-content"><strong>Category Merchandising</strong><br>Master effective merchandising strategies.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Create two columns for the courses
def create_course_grid(courses):
    if not courses:
        st.info("No courses available in this category yet.")
        return
    
    # Create two columns for the courses
    cols = st.columns(2)
    
    # Display courses in a grid
    for i, course in enumerate(courses):
        with cols[i % 2]:
            st.markdown(f'<div class="metis-card">', unsafe_allow_html=True)
            
            # Course title and completion badge
            completed = random.randint(0, 100) > 70  # Randomize for demo purposes
            if completed:
                st.markdown(f"#### {course['title']} <span class='badge' style='background-color: #00C853;'>Completed</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"#### {course['title']}")
            
            st.markdown(f"{course['description']}")
            
            # Module list
            st.markdown("**Modules:**")
            for module in course['modules']:
                st.markdown(f"- {module['title']} ({module['duration']})")
            
            # Enter course button
            if st.button(f"{'Continue' if completed else 'Start'} Course", key=f"start_{course['id']}"):
                st.session_state.current_course = course['id']
                st.session_state.current_module = course['modules'][0]['id']
                st.session_state.quiz_active = False
                st.experimental_rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# Course page
def course_page(course_id):
    course = next((c for c in all_courses if c['id'] == course_id), None)
    
    if not course:
        st.error("Course not found")
        return
    
    st.markdown(f'<h1 class="main-header">{course["title"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{course["description"]}</p>', unsafe_allow_html=True)
    
    # Module navigation
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown('<div class="metis-card">', unsafe_allow_html=True)
        st.markdown("### Modules")
        
        for module in course['modules']:
            if st.button(f"{module['title']}", key=f"module_{module['id']}"):
                st.session_state.current_module = module['id']
                st.session_state.quiz_active = False
                st.experimental_rerun()
        
        if st.button("Back to Catalog"):
            st.session_state.current_course = None
            st.session_state.current_module = None
            st.session_state.quiz_active = False
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Display the current module content or quiz
        if st.session_state.quiz_active:
            display_quiz(course_id, st.session_state.current_module)
        else:
            display_module_content(course_id, st.session_state.current_module)

# Display module content
def display_module_content(course_id, module_id):
    # Get the content for the current module
    content_key = f"{course_id}-{module_id}"
    
    if content_key not in module_content:
        st.error(f"Content for module {module_id} not found")
        return
    
    module_data = module_content[content_key]
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown(f"### {module_data['title']}")
    
    # Video (if available)
    if 'video_url' in module_data and module_data['video_url']:
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.markdown(f'<iframe width="100%" height="315" src="{module_data["video_url"]}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Module content
    st.markdown(module_data['content'], unsafe_allow_html=True)
    
    # Add user-specific content if applicable
    if st.session_state.user_type == "employee" and "employee_content" in module_data:
        st.markdown("### For MediaVision Employees")
        st.markdown(module_data["employee_content"], unsafe_allow_html=True)
    
    elif st.session_state.user_type == "partner" and "partner_content" in module_data:
        st.markdown("### For Partners")
        st.markdown(module_data["partner_content"], unsafe_allow_html=True)
    
    elif st.session_state.user_type == "customer" and "customer_content" in module_data:
        st.markdown("### For Customers")
        st.markdown(module_data["customer_content"], unsafe_allow_html=True)
    
    # Quiz button at the end
    if 'has_quiz' in module_data and module_data['has_quiz']:
        if st.button("Take Quiz", key=f"quiz_{content_key}"):
            st.session_state.quiz_active = True
            st.session_state.quiz_score = 0
            st.session_state.quiz_total = len(module_data['quiz'])
            st.experimental_rerun()
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    course = next((c for c in all_courses if c['id'] == course_id), None)
    module_ids = [m['id'] for m in course['modules']]
    current_index = module_ids.index(module_id)
    
    with col1:
        if current_index > 0:
            if st.button("← Previous Module"):
                st.session_state.current_module = module_ids[current_index - 1]
                st.session_state.quiz_active = False
                st.experimental_rerun()
    
    with col3:
        if current_index < len(module_ids) - 1:
            if st.button("Next Module →"):
                st.session_state.current_module = module_ids[current_index + 1]
                st.session_state.quiz_active = False
                st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Display quiz for the current module
def display_quiz(course_id, module_id):
    content_key = f"{course_id}-{module_id}"
    
    if content_key not in module_content or 'quiz' not in module_content[content_key]:
        st.error("Quiz not found")
        return
    
    module_data = module_content[content_key]
    quiz_data = module_data['quiz']
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown(f"### Quiz: {module_data['title']}")
    st.markdown("Test your knowledge by answering the following questions.")
    
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
        st.session_state.quiz_answers = [-1] * len(quiz_data)
    
    for i, question in enumerate(quiz_data):
        st.markdown(f'<div class="quiz-question">', unsafe_allow_html=True)
        st.markdown(f"**Question {i+1}:** {question['question']}")
        
        # Disable radio buttons if quiz is already submitted
        disabled = st.session_state.quiz_submitted
        
        selected = st.radio(
            f"Select an answer for question {i+1}:",
            options=question['options'],
            index=st.session_state.quiz_answers[i] if st.session_state.quiz_answers[i] >= 0 else 0,
            key=f"q_{content_key}_{i}",
            disabled=disabled
        )
        
        # Save the selected answer
        selected_index = question['options'].index(selected)
        st.session_state.quiz_answers[i] = selected_index
        
        # Show feedback if quiz is submitted
        if st.session_state.quiz_submitted:
            if selected_index == question['correct']:
                st.success("✓ Correct!")
            else:
                st.error(f"✗ Incorrect. The correct answer is: {question['options'][question['correct']]}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Back to Module", key=f"back_to_module_{content_key}"):
            st.session_state.quiz_active = False
            st.session_state.quiz_submitted = False
            st.session_state.quiz_answers = [-1] * len(quiz_data)
            st.experimental_rerun()
    
    with col2:
        if not st.session_state.quiz_submitted:
            if st.button("Submit Answers", key=f"submit_quiz_{content_key}"):
                # Calculate score
                score = 0
                for i, question in enumerate(quiz_data):
                    if st.session_state.quiz_answers[i] == question['correct']:
                        score += 1
                
                st.session_state.quiz_score = score
                st.session_state.quiz_submitted = True
                
                # Update user progress if not done before
                # In a real app, this would be stored in a database
                if content_key not in st.session_state.user.completed_modules:
                    st.session_state.user.completed_modules.append(content_key)
                    st.session_state.user.progress = min(100, st.session_state.user.progress + 5)
                
                st.experimental_rerun()
        else:
            # Show final score
            st.markdown(f"**Final Score:** {st.session_state.quiz_score}/{st.session_state.quiz_total}")
            
            # Show appropriate message based on score
            if st.session_state.quiz_score == st.session_state.quiz_total:
                st.success("Perfect score! You've mastered this module.")
            elif st.session_state.quiz_score >= st.session_state.quiz_total * 0.7:
                st.success("Good job! You've passed this module.")
            else:
                st.warning("You may want to review the module content and try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar navigation
def sidebar():
    user_type_badge = {
        "employee": "Employee",
        "partner": "Partner",
        "customer": "Customer"
    }
    
    user_type_colors = {
        "employee": "badge-employee",
        "partner": "badge-partner",
        "customer": "badge-customer"
    }
    
    st.sidebar.markdown(f"""
    <div style="padding: 15px 0; text-align: center; color: white;">
        <h3 style="margin: 0;">(M) MediaVision Metis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # User profile
    st.sidebar.markdown(f"""
    <div class="user-profile" style="background-color: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 20px;">
        <img src="https://via.placeholder.com/40" alt="Profile">
        <div>
            <div style="color: white; font-weight: bold;">{st.session_state.user.name} <span class="badge {user_type_colors[st.session_state.user_type]}">{user_type_badge[st.session_state.user_type]}</span></div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.8em;">{st.session_state.user.role}</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.8em;">{st.session_state.user.company}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.sidebar.markdown("### Navigation")
    
    if st.sidebar.button("📚 Course Catalog", help="View all available courses"):
        st.session_state.current_course = None
        st.session_state.current_module = None
        st.session_state.quiz_active = False
    
    if st.sidebar.button("📊 My Progress", help="Track your learning journey"):
        st.session_state.current_course = "progress"
        st.session_state.current_module = None
        st.session_state.quiz_active = False
    
    if st.sidebar.button("🏆 Certifications", help="View your earned certifications"):
        st.session_state.current_course = "certifications"
        st.session_state.current_module = None
        st.session_state.quiz_active = False
    
    # User type specific navigation options
    if st.session_state.user_type == "employee":
        st.sidebar.markdown("### Admin Tools")
        if st.sidebar.button("👥 Manage Users", help="Manage client and partner accounts"):
            st.session_state.current_course = "manage_users"
        if st.sidebar.button("📈 Usage Analytics", help="View platform usage statistics"):
            st.session_state.current_course = "usage_analytics"
    
    elif st.session_state.user_type == "partner":
        st.sidebar.markdown("### Partner Resources")
        if st.sidebar.button("🔌 API Documentation", help="Access API integration guides"):
            st.session_state.current_course = "api_docs"
        if st.sidebar.button("💼 Marketing Materials", help="Access co-branded marketing resources"):
            st.session_state.current_course = "marketing_materials"
    
    elif st.session_state.user_type == "customer":
        st.sidebar.markdown("### Support Resources")
        if st.sidebar.button("❓ FAQs & Troubleshooting", help="Find answers to common questions"):
            st.session_state.current_course = "faqs"
        if st.sidebar.button("🎯 ROI Calculator", help="Calculate your return on investment"):
            st.session_state.current_course = "roi_calculator"
    
    if st.sidebar.button("⚙️ Settings", help="Manage your account settings"):
        st.session_state.current_course = "settings"
        st.session_state.current_module = None
        st.session_state.quiz_active = False
    
    # Logout button at the bottom
    st.sidebar.markdown("<div style='position: fixed; bottom: 20px; width: inherit;'>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Logout", help="Sign out of your account"):
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.experimental_rerun()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Progress page
def progress_page():
    st.markdown('<h1 class="main-header">My Progress</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Track your learning journey</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    
    # Overall progress
    st.markdown("### Overall Completion")
    st.progress(st.session_state.user.progress / 100)
    st.markdown(f"You've completed **{st.session_state.user.progress}%** of your available training materials.")
    
    # Course breakdown
    st.markdown("### Course Progress")
    
    available_courses = get_available_courses(st.session_state.user_type)
    
    for course in available_courses:
        # Calculate course progress (in a real app, this would come from a database)
        completed_modules_in_course = [m for m in st.session_state.user.completed_modules if m.startswith(f"{course['id']}-")]
        total_modules = len(course['modules'])
        completed_modules = len(completed_modules_in_course)
        course_progress = (completed_modules / total_modules) * 100 if total_modules > 0 else 0
        
        st.markdown(f"**{course['title']}**")
        st.progress(course_progress / 100)
        st.markdown(f"{completed_modules}/{total_modules} modules completed ({int(course_progress)}%)")
    
    # Recent activity
    st.markdown("### Recent Activity")
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Activity</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>April 30, 2025</td>
                <td>Product Visibility Optimization - Module 1</td>
                <td>Completed</td>
            </tr>
            <tr>
                <td>April 29, 2025</td>
                <td>Introduction to Metis - Quiz</td>
                <td>Passed (90%)</td>
            </tr>
            <tr>
                <td>April 28, 2025</td>
                <td>Introduction to Metis - Module 3</td>
                <td>Completed</td>
            </tr>
            <tr>
                <td>April 26, 2025</td>
                <td>Introduction to Metis - Module 2</td>
                <td>Completed</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    # Achievement badges
    st.markdown("### Achievement Badges")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 12px;">
            <div style="font-size: 30px; margin-bottom: 10px;">🏆</div>
            <div style="font-weight: bold;">Platform Navigator</div>
            <div style="font-size: 12px; color: #6c757d;">Completed Introduction to Metis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 12px;">
            <div style="font-size: 30px; margin-bottom: 10px;">📊</div>
            <div style="font-weight: bold;">Analytics Explorer</div>
            <div style="font-size: 12px; color: #6c757d;">Completed 5 modules</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 12px; opacity: 0.5;">
            <div style="font-size: 30px; margin-bottom: 10px;">🔍</div>
            <div style="font-weight: bold;">Category Master</div>
            <div style="font-size: 12px; color: #6c757d;">Complete Category Monitoring Masterclass</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 12px; opacity: 0.5;">
            <div style="font-size: 30px; margin-bottom: 10px;">🚀</div>
            <div style="font-weight: bold;">Optimization Guru</div>
            <div style="font-size: 12px; color: #6c757d;">Complete all optimization courses</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Certifications page
def certifications_page():
    st.markdown('<h1 class="main-header">Certifications</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">View and track your Metis certifications</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    
    # Available certifications based on user type
    if st.session_state.user_type == "employee":
        st.markdown("### MediaVision Certifications")
        certifications = [
            {"title": "Metis Fundamentals", "status": "Completed", "date": "March 15, 2025", "badge": "🏆"},
            {"title": "Metis Implementation Specialist", "status": "In Progress (2/4)", "date": "-", "badge": "🛠️"},
            {"title": "Metis Master Trainer", "status": "Not Started", "date": "-", "badge": "👨‍🏫"}
        ]
    
    elif st.session_state.user_type == "partner":
        st.markdown("### Partner Certifications")
        certifications = [
            {"title": "Metis Fundamentals", "status": "Completed", "date": "April 10, 2025", "badge": "🏆"},
            {"title": "Metis Integration Partner", "status": "In Progress (1/4)", "date": "-", "badge": "🔌"},
            {"title": "Metis Solutions Architect", "status": "Not Started", "date": "-", "badge": "🏗️"}
        ]
    
    elif st.session_state.user_type == "customer":
        st.markdown("### Customer Certifications")
        certifications = [
            {"title": "Metis Fundamentals", "status": "In Progress (2/3)", "date": "-", "badge": "🏆"},
            {"title": "Metis Platform Expert", "status": "Not Started", "date": "-", "badge": "👑"},
            {"title": "Metis Optimization Specialist", "status": "Not Started", "date": "-", "badge": "📈"}
        ]
    
    # Display certifications
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th></th>
                <th>Certification</th>
                <th>Status</th>
                <th>Completion Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)
    
    for cert in certifications:
        button_text = "View" if cert["status"].startswith("Completed") else "Continue" if cert["status"].startswith("In Progress") else "Start"
        button_disabled = "disabled" if cert["status"] == "Not Started" else ""
        
        st.markdown(f"""
        <tr>
            <td style="font-size: 24px;">{cert["badge"]}</td>
            <td><strong>{cert["title"]}</strong></td>
            <td>{cert["status"]}</td>
            <td>{cert["date"]}</td>
            <td><button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;" {button_disabled}>{button_text}</button></td>
        </tr>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </tbody>
    </table>
    """, unsafe_allow_html=True)
# Settings page
def settings_page():
    st.markdown('<h1 class="main-header">Account Settings</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage your account preferences</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    
    # Profile settings
    st.markdown("### Profile Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Full Name", value=st.session_state.user.name)
    
    with col2:
        st.text_input("Job Title", value=st.session_state.user.role)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Email", value=st.session_state.user.email)
    
    with col2:
        st.text_input("Company", value=st.session_state.user.company)
    
    st.file_uploader("Profile Picture", type=["jpg", "jpeg", "png"])
    
    if st.button("Update Profile"):
        st.success("Profile updated successfully!")
    
    # Password settings
    st.markdown("### Change Password")
    
    st.text_input("Current Password", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("New Password", type="password")
    
    with col2:
        st.text_input("Confirm New Password", type="password")
    
    if st.button("Change Password"):
        st.success("Password changed successfully!")
    
    # Notification settings
    st.markdown("### Notification Preferences")
    
    st.checkbox("Course updates and new content", value=True)
    st.checkbox("Quiz and assessment reminders", value=True)
    st.checkbox("Certification opportunities", value=True)
    st.checkbox("Platform feature updates", value=False)
    st.checkbox("Marketing communications", value=False)
    
    if st.button("Save Notification Preferences"):
        st.success("Notification preferences saved!")
    
    # Learning preferences
    st.markdown("### Learning Preferences")
    
    st.selectbox("Preferred Learning Style", ["Self-paced", "Instructor-led", "Blended"])
    st.selectbox("Content Format Priority", ["Video", "Text", "Interactive", "No Preference"])
    st.slider("Content Difficulty Level", 1, 5, 3, help="1 = Beginner, 5 = Expert")
    
    if st.button("Save Learning Preferences"):
        st.success("Learning preferences saved!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Manage users page (for employees)
def manage_users_page():
    st.markdown('<h1 class="main-header">Manage Users</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Add, edit, and manage platform users</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    
    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.text_input("Search Users", placeholder="Search by name, email, or company")
    
    with col2:
        st.selectbox("User Type", ["All Types", "Employee", "Partner", "Customer"])
    
    with col3:
        st.selectbox("Status", ["All Statuses", "Active", "Inactive", "Pending"])
    
    # User table
    st.markdown("### User Directory")
    
    # Sample user data
    users = [
        {"name": "Emily Wilson", "email": "emily@mediavision.com", "type": "Employee", "company": "MediaVision", "status": "Active", "last_login": "May 1, 2025"},
        {"name": "David Chen", "email": "david@fashionretailer.com", "type": "Customer", "company": "Fashion Retailer Ltd", "status": "Active", "last_login": "April 29, 2025"},
        {"name": "Jessica Lee", "email": "jessica@digitalsolutions.com", "type": "Partner", "company": "Digital Solutions Inc.", "status": "Active", "last_login": "April 30, 2025"},
        {"name": "Michael Brown", "email": "michael@homegoods.com", "type": "Customer", "company": "Home Goods Direct", "status": "Inactive", "last_login": "March 15, 2025"},
        {"name": "Sarah Johnson", "email": "sarah@mediavision.com", "type": "Employee", "company": "MediaVision", "status": "Active", "last_login": "May 1, 2025"}
    ]
    
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>User Type</th>
                <th>Company</th>
                <th>Status</th>
                <th>Last Login</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)
    
    for user in users:
        status_color = "#00C853" if user["status"] == "Active" else "#FF5252" if user["status"] == "Inactive" else "#FFC107"
        
        st.markdown(f"""
        <tr>
            <td>{user["name"]}</td>
            <td>{user["email"]}</td>
            <td>{user["type"]}</td>
            <td>{user["company"]}</td>
            <td><span style="color: {status_color}; font-weight: bold;">{user["status"]}</span></td>
            <td>{user["last_login"]}</td>
            <td>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 3px 8px; border-radius: 5px; font-size: 12px; cursor: pointer; margin-right: 5px;">Edit</button>
                <button style="background-color: transparent; color: #7B68EE; border: 1px solid #7B68EE; padding: 3px 8px; border-radius: 5px; font-size: 12px; cursor: pointer;">Disable</button>
            </td>
        </tr>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    # Add new user form
    st.markdown("### Add New User")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Full Name", key="new_user_name")
        st.text_input("Email", key="new_user_email")
        st.selectbox("User Type", ["Employee", "Partner", "Customer"], key="new_user_type")
    
    with col2:
        st.text_input("Company", key="new_user_company")
        st.text_input("Job Title", key="new_user_title")
        st.selectbox("Initial Access Level", ["Standard", "Admin", "Limited"], key="new_user_access")
    
    if st.button("Add User"):
        st.success("User added successfully! An invitation email has been sent.")
    
    # Bulk actions
    st.markdown("### Bulk Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("Import Users (CSV)")
    
    with col2:
        st.button("Export User List")
    
    with col3:
        st.button("Send Bulk Invitations")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Usage analytics page (for employees)
def usage_analytics_page():
    st.markdown('<h1 class="main-header">Usage Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Monitor platform usage and engagement</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Start Date", value=datetime.datetime.now() - datetime.timedelta(days=30))
    with col2:
        st.date_input("End Date", value=datetime.datetime.now())
    
    # Filter options
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        st.selectbox("User Type", ["All Users", "Customers", "Partners", "Employees"])
    with filter_col2:
        st.selectbox("Activity Type", ["All Activities", "Course Completion", "Quiz Attempts", "Logins"])
    with filter_col3:
        st.selectbox("Group By", ["Day", "Week", "Month"])
    
    if st.button("Apply Filters"):
        # Dashboard would be populated here in a real app
        pass
    
    # Sample analytics charts and data
    st.markdown("### Platform Usage Overview")
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; text-align: center; margin-bottom: 20px;">
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; width: 23%;">
            <h4>Total Logins</h4>
            <p style="font-size: 24px; font-weight: bold;">1,287</p>
        </div>
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; width: 23%;">
            <h4>Active Users</h4>
            <p style="font-size: 24px; font-weight: bold;">342</p>
        </div>
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; width: 23%;">
            <h4>Courses Started</h4>
            <p style="font-size: 24px; font-weight: bold;">756</p>
        </div>
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; width: 23%;">
            <h4>Courses Completed</h4>
            <p style="font-size: 24px; font-weight: bold;">521</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Usage trend chart (placeholder)
    st.markdown("### Usage Trend")
    st.markdown("```python\n# This would be a line chart showing usage over time\n```")
    
    # Popular courses
    st.markdown("### Most Popular Courses")
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th>Course</th>
                <th>Users Started</th>
                <th>Completion Rate</th>
                <th>Avg. Rating</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Introduction to Metis</td>
                <td>245</td>
                <td>92%</td>
                <td>4.8/5</td>
            </tr>
            <tr>
                <td>Category Monitoring Masterclass</td>
                <td>187</td>
                <td>78%</td>
                <td>4.7/5</td>
            </tr>
            <tr>
                <td>Product Visibility Optimization</td>
                <td>156</td>
                <td>82%</td>
                <td>4.6/5</td>
            </tr>
            <tr>
                <td>Metis API Integration</td>
                <td>143</td>
                <td>75%</td>
                <td>4.5/5</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    # Export options
    st.markdown("### Export Data")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Export as CSV")
    with col2:
        st.button("Export as PDF")
    
    st.markdown('</div>', unsafe_allow_html=True)

# API documentation page (for partners)
def api_docs_page():
    st.markdown('<h1 class="main-header">API Documentation</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Learn how to integrate with the Metis platform</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    
    # API documentation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Authentication", "Endpoints", "Code Examples"])
    
    with tab1:
        st.markdown("### Metis API Overview")
        st.markdown("""
        The Metis API provides programmatic access to data and functionality of the Metis platform. You can use the API to:
        
        - Retrieve e-commerce analytics data
        - Access optimization recommendations
        - Create and manage categories
        - Monitor product visibility
        - Generate custom reports
        
        The API follows RESTful principles and uses JSON for data exchange. All API requests require authentication using OAuth 2.0.
        """)
        
        st.markdown("### Getting Started")
        st.markdown("""
        To get started with the Metis API:
        
        1. Register for API access in your partner portal
        2. Generate API credentials
        3. Implement OAuth 2.0 authentication
        4. Make your first API request
        
        See the Authentication and Endpoints tabs for detailed instructions.
        """)
    
    with tab2:
        st.markdown("### Authentication")
        st.markdown("""
        The Metis API uses OAuth 2.0 for authentication. Follow these steps to authenticate your requests:
        
        1. **Generate API credentials**:
           - Log in to your partner portal
           - Navigate to API Settings
           - Generate a client ID and client secret
        
        2. **Request an access token**:
        ```
        POST https://api.metisplatform.com/oauth/token
        Content-Type: application/x-www-form-urlencoded
        
        grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET
        ```
        
        3. **Use the access token in requests**:
        ```
        GET https://api.metisplatform.com/v2/analytics/categories
        Authorization: Bearer YOUR_ACCESS_TOKEN
        ```
        
        Access tokens are valid for 60 minutes. You'll need to request a new token when it expires.
        """)
    
    with tab3:
        st.markdown("### API Endpoints")
        
        # Categories endpoints
        st.markdown("#### Categories")
        st.markdown("""
        ```
        GET /v2/categories
        GET /v2/categories/{id}
        POST /v2/categories
        PUT /v2/categories/{id}
        DELETE /v2/categories/{id}
        ```
        """)
        
        # Products endpoints
        st.markdown("#### Products")
        st.markdown("""
        ```
        GET /v2/products
        GET /v2/products/{id}
        GET /v2/products/{id}/visibility
        GET /v2/products/{id}/recommendations
        ```
        """)
        
        # Analytics endpoints
        st.markdown("#### Analytics")
        st.markdown("""
        ```
        GET /v2/analytics/demand
        GET /v2/analytics/visibility
        GET /v2/analytics/performance
        GET /v2/analytics/competitors
        ```
        """)
        
        # Recommendations endpoints
        st.markdown("#### Recommendations")
        st.markdown("""
        ```
        GET /v2/recommendations/categories
        GET /v2/recommendations/products
        GET /v2/recommendations/merchandising
        ```
        """)
    
    with tab4:
        st.markdown("### Code Examples")
        
        # JavaScript example
        st.markdown("#### JavaScript")
        st.code("""
// Request an access token
async function getAccessToken() {
  const response = await fetch('https://api.metisplatform.com/oauth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET'
  });
  
  const data = await response.json();
  return data.access_token;
}

// Get category analytics
async function getCategoryAnalytics() {
  const token = await getAccessToken();
  
  const response = await fetch('https://api.metisplatform.com/v2/analytics/categories', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
}
        """, language="javascript")
        
        # Python example
        st.markdown("#### Python")
        st.code("""
import requests

# Request an access token
def get_access_token():
    url = 'https://api.metisplatform.com/oauth/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'YOUR_CLIENT_ID',
        'client_secret': 'YOUR_CLIENT_SECRET'
    }
    
    response = requests.post(url, data=data)
    return response.json()['access_token']

# Get product visibility data
def get_product_visibility(product_id):
    token = get_access_token()
    
    url = f'https://api.metisplatform.com/v2/products/{product_id}/visibility'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(url, headers=headers)
    return response.json()
        """, language="python")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Marketing materials page (for partners)
def marketing_materials_page():
    st.markdown('<h1 class="main-header">Marketing Materials</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Access co-branded marketing resources</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown("### Available Marketing Resources")
    
    # Categories for materials
    tabs = st.tabs(["Presentations", "Case Studies", "Logos & Brand Assets", "Product Sheets"])
    
    with tabs[0]:
        st.markdown("#### Presentation Templates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h4>Metis Overview Presentation</h4>
                <p>A comprehensive introduction to Metis for potential clients.</p>
                <p style="color: #666;">Last updated: March 15, 2025</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PowerPoint</button>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h4>Partner Success Stories</h4>
                <p>Showcase of successful partner implementations and results.</p>
                <p style="color: #666;">Last updated: April 10, 2025</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PowerPoint</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h4>Technical Integration Presentation</h4>
                <p>Detailed slides on API integration and technical requirements.</p>
                <p style="color: #666;">Last updated: April 22, 2025</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PowerPoint</button>
            </div>
            
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h4>ROI Case Builder</h4>
                <p>Presentation template for building custom ROI cases.</p>
                <p style="color: #666;">Last updated: March 28, 2025</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PowerPoint</button>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Custom Branding")
        st.markdown("Upload your logo to create co-branded presentations.")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.file_uploader("Upload your logo", type=["png", "jpg", "jpeg"])
        with col2:
            st.button("Generate Co-Branded Materials")
    
    with tabs[1]:
        st.markdown("#### Case Studies")
        
        st.markdown("""
        <div style="display: flex; flex-wrap: wrap; gap: 20px;">
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; width: 45%;">
                <h4>New Look Success Story</h4>
                <p>How New Look increased organic visibility by 400% with Metis</p>
                <p style="color: #666;">Industry: Fashion Retail | ROI: 342%</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PDF</button>
            </div>
            
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; width: 45%;">
                <h4>Farfetch Implementation Case Study</h4>
                <p>Farfetch's journey to optimized product visibility</p>
                <p style="color: #666;">Industry: Luxury Fashion | ROI: 287%</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PDF</button>
            </div>
            
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; width: 45%;">
                <h4>Abbott Lyon Revenue Growth</h4>
                <p>How Abbott Lyon achieved ambitious growth targets with Metis</p>
                <p style="color: #666;">Industry: Jewelry | ROI: 215%</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PDF</button>
            </div>
            
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; width: 45%;">
                <h4>Moss Bros SEO Transformation</h4>
                <p>Moss Bros Group's strategy for transforming organic performance</p>
                <p style="color: #666;">Industry: Men's Fashion | ROI: 198%</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PDF</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("#### Logos & Brand Assets")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Metis Logos")
            st.markdown("""
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; text-align: center;">
                    <img src="https://via.placeholder.com/150x80?text=Metis+Logo" alt="Metis Logo">
                    <p style="margin: 5px 0;">Primary Logo</p>
                    <button style="background-color: #7B68EE; color: white; border: none; padding: 3px 8px; border-radius: 5px; font-size: 12px; cursor: pointer;">PNG</button>
                    <button style="background-color: #7B68EE; color: white; border: none; padding: 3px 8px; border-radius: 5px; font-size: 12px; cursor: pointer;">SVG</button>
                </div>
                
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; text-align: center;">
                    <img src="https://via.placeholder.com/150x80?text=Metis+Icon" alt="Metis Icon">
                    <p style="margin: 5px 0;">Icon Only</p>
                    <button style="background-color: #7B68EE; color: white; border: none; padding: 3px 8px; border-radius: 5px; font-size: 12px; cursor: pointer;">PNG</button>
                    <button style="background-color: #7B68EE; color: white; border: none; padding: 3px 8px; border-radius: 5px; font-size: 12px; cursor: pointer;">SVG</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("##### Partner Badges")
            st.markdown("""
            <div style="display: flex; gap: 10px;">
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; text-align: center;">
                    <img src="https://via.placeholder.com/150x80?text=Certified+Partner" alt="Certified Partner Badge">
                    <p style="margin: 5px 0;">Certified Partner</p>
                    <button style="background-color: #7B68EE; color: white; border: none; padding: 3px 8px; border-radius: 5px; font-size: 12px; cursor: pointer;">PNG</button>
                    <button style="background-color: #7B68EE; color: white; border: none; padding: 3px 8px; border-radius: 5px; font-size: 12px; cursor: pointer;">SVG</button>
                </div>
                
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; text-align: center;">
                    <img src="https://via.placeholder.com/150x80?text=Gold+Partner" alt="Gold Partner Badge">
                    <p style="margin: 5px 0;">Gold Partner</p>
                    <button style="background-color: #7B68EE; color: white; border: none; padding: 3px 8px; border-radius: 5px; font-size: 12px; cursor: pointer;">PNG</button>
                    <button style="background-color: #7B68EE; color: white; border: none; padding: 3px 8px; border-radius: 5px; font-size: 12px; cursor: pointer;">SVG</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("##### Brand Guidelines")
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h5>Metis Brand Guidelines</h5>
                <p>Complete guide to using Metis brand assets correctly.</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PDF</button>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("##### Color Palette")
            st.markdown("""
            <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                <div style="background-color: #7B68EE; width: 50px; height: 50px; border-radius: 5px;"></div>
                <div style="background-color: #1E1640; width: 50px; height: 50px; border-radius: 5px;"></div>
                <div style="background-color: #F8F9FA; width: 50px; height: 50px; border-radius: 5px; border: 1px solid #ddd;"></div>
                <div style="background-color: #2B2D42; width: 50px; height: 50px; border-radius: 5px;"></div>
                <div style="background-color: #6C757D; width: 50px; height: 50px; border-radius: 5px;"></div>
            </div>
            <div style="margin-bottom: 15px;">
                <p style="margin: 0;">Primary: #7B68EE | Secondary: #1E1640 | Background: #F8F9FA</p>
                <p style="margin: 0;">Text: #2B2D42 | Light Text: #6C757D</p>
            </div>
            
            <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; margin-top: 10px;">Download Color Assets</button>
            """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("#### Product Sheets")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h4>Metis Platform Overview</h4>
                <p>Complete platform capabilities and features.</p>
                <p style="color: #666;">Last updated: April 15, 2025</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PDF</button>
            </div>
            
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h4>Category Monitoring Module</h4>
                <p>Detailed information on the Category Monitoring tools.</p>
                <p style="color: #666;">Last updated: March 22, 2025</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PDF</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h4>Product Visibility Module</h4>
                <p>Detailed information on Product Visibility capabilities.</p>
                <p style="color: #666;">Last updated: April 5, 2025</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PDF</button>
            </div>
            
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <h4>Metis API Integration Guide</h4>
                <p>Technical details for integrating with the Metis API.</p>
                <p style="color: #666;">Last updated: April 18, 2025</p>
                <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download PDF</button>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# FAQs & Troubleshooting page (for customers)
def faqs_page():
    st.markdown('<h1 class="main-header">FAQs & Troubleshooting</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Find answers to common questions and issues</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    
    # Search box
    st.text_input("Search FAQs", placeholder="Type your question here...")
    
    # FAQ categories
    tab1, tab2, tab3, tab4 = st.tabs(["General", "Technical", "Account & Billing", "Optimization"])
    
    with tab1:
        st.markdown("### General Questions")
        
        # FAQ accordion
        with st.expander("What is Metis and how does it work?"):
            st.markdown("""
            Metis is an e-commerce optimization platform that helps you understand what people want and when they want it. It makes tailored daily recommendations based on market data and your website to inform business decisions 4x faster than your competitors.
            
            The platform provides a central source of insight into weekly organic demand data and pulls this data into tailored daily recommendations to improve business performance.
            """)
        
        with st.expander("Who can benefit from using Metis?"):
            st.markdown("""
            Metis adds value across the organization:
            
            - **Buyers**: Inform product buying, range building, new product development
            - **Merchandisers**: Inform sales planning decisions, delivery timetables, trading windows
            - **Trading Teams**: Support daily site trading, category creation, page creation
            - **Digital and Marketing Teams**: Deliver sitewide recommendations for quick wins
            - **C-Suite**: Access to unique data to support investment decisions
            """)
        
        with st.expander("How long does it take to implement Metis?"):
            st.markdown("""
            The typical implementation timeline for Metis is 2-4 weeks, depending on the complexity of your e-commerce platform and the specific modules you're implementing. Our implementation team will work with you to create a tailored onboarding plan.
            """)
        
        with st.expander("What makes Metis different from other analytics tools?"):
            st.markdown("""
            Metis differs from standard analytics tools in several key ways:
            
            1. It focuses specifically on e-commerce optimization rather than general website analytics
            2. It provides actionable recommendations, not just data
            3. It combines market demand data with your website performance
            4. It updates daily with fresh insights rather than static reports
            5. It's designed for cross-functional use across your organization
            """)
    
    with tab2:
        st.markdown("### Technical Questions")
        
        with st.expander("What technical requirements are needed to use Metis?"):
            st.markdown("""
            Metis is a cloud-based platform that requires minimal technical setup. The basic requirements are:
            
            - Access to your Google Analytics account
            - Access to your e-commerce platform's admin area
            - Implementation of a small tracking script on your website
            
            No server-side installation is required, and our team handles most of the setup process.
            """)
        
        with st.expander("Can Metis integrate with my e-commerce platform?"):
            st.markdown("""
            Yes, Metis can integrate with all major e-commerce platforms including:
            
            - Shopify
            - Magento
            - WooCommerce
            - BigCommerce
            - Custom platforms
            
            We have pre-built integrations for major platforms and can develop custom integrations for proprietary systems.
            """)
        
        with st.expander("How secure is my data with Metis?"):
            st.markdown("""
            Data security is a top priority at Metis. We implement multiple layers of protection:
            
            - All data is encrypted in transit and at rest
            - We are GDPR compliant and SOC 2 certified
            - Regular security audits and penetration testing
            - No personally identifiable information (PII) is collected
            - Role-based access controls for your team members
            """)
        
        with st.expander("Can I access Metis data via API?"):
            st.markdown("""
            Yes, Metis offers a comprehensive API that allows you to:
            
            - Retrieve analytics data
            - Access recommendations
            - Integrate Metis insights into your dashboards
            - Automate reporting
            
            API documentation is available in the partner portal, and our support team can help you with integration.
            """)
    
    with tab3:
        st.markdown("### Account & Billing Questions")
        
        with st.expander("How is Metis priced?"):
            st.markdown("""
            Metis is available in several pricing tiers based on your e-commerce volume and the specific modules you need. Our pricing is subscription-based with monthly or annual billing options.
            
            For detailed pricing information, please contact your account manager or sales representative.
            """)
        
        with st.expander("Can I change my subscription plan?"):
            st.markdown("""
            Yes, you can upgrade or downgrade your subscription plan at any time. Upgrades take effect immediately, while downgrades will be applied at the end of your current billing cycle.
            
            To change your plan, contact your account manager or submit a request through the support portal.
            """)
        
        with st.expander("How do I add more users to my account?"):
            st.markdown("""
            You can add additional users to your Metis account from the Admin section:
            
            1. Navigate to Settings > User Management
            2. Click "Add User"
            3. Enter the user's information and select their role
            4. An invitation will be sent to the user's email
            
            Additional user licenses may affect your subscription cost, depending on your plan.
            """)
        
        with st.expander("What support options are available?"):
            st.markdown("""
            All Metis subscriptions include standard support:
            
            - Email support (24-hour response time)
            - Access to the knowledge base and documentation
            - Monthly check-in calls
            
            Premium and Enterprise plans include additional support options:
            
            - Dedicated account manager
            - Phone support
            - Priority response times
            - Custom training sessions
            """)
    
    with tab4:
        st.markdown("### Optimization Questions")
        
        with st.expander("How often is Metis data updated?"):
            st.markdown("""
            Metis updates data on different schedules depending on the module:
            
            - Market demand data: Weekly
            - Category and product performance: Daily
            - Recommendations: Daily
            - Competitor analysis: Weekly
            
            All recommendations and insights are refreshed daily to ensure you have the most current information.
            """)
        
        with st.expander("How do I implement Metis recommendations?"):
            st.markdown("""
            Implementing Metis recommendations depends on the specific recommendation type:
            
            - Category structure changes: Update your site navigation and category pages
            - Product visibility: Adjust product positions within category pages
            - Content optimization: Update meta titles, descriptions, and category content
            - Merchandising: Adjust product promotions and featured items
            
            Most recommendations include step-by-step implementation instructions, and our support team can provide guidance as needed.
            """)
        
        with st.expander("How do I measure the impact of Metis?"):
            st.markdown("""
            Metis provides several ways to measure the impact of your optimizations:
            
            - Before/after performance comparisons
            - ROI calculations for specific recommendations
            - Traffic and revenue attribution
            - Competitive benchmark tracking
            
            The Analytics section of the platform includes dedicated reports for measuring the impact of implemented recommendations.
            """)
        
        with st.expander("Can Metis help with international markets?"):
            st.markdown("""
            Yes, Metis supports international optimization across multiple markets and languages. The platform can:
            
            - Analyze market-specific demand trends
            - Provide localized recommendations
            - Support multiple currencies and languages
            - Compare performance across different regions
            
            International optimization is available on Premium and Enterprise plans.
            """)
    
    # Still need help section
    st.markdown("### Still Need Help?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; text-align: center; height: 150px;">
            <h4>Contact Support</h4>
            <p>Reach out to our support team for personalized assistance.</p>
            <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Submit Ticket</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; text-align: center; height: 150px;">
            <h4>Schedule a Call</h4>
            <p>Book a call with your account manager for guidance.</p>
            <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Book Appointment</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; text-align: center; height: 150px;">
            <h4>Knowledge Base</h4>
            <p>Explore detailed guides and tutorials in our knowledge base.</p>
            <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">View Resources</button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ROI Calculator page (for customers)
def roi_calculator_page():
    st.markdown('<h1 class="main-header">ROI Calculator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Calculate your potential return on investment with Metis</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    
    # Business information
    st.markdown("### Business Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("Industry", ["Fashion & Apparel", "Jewelry & Accessories", "Home & Garden", "Electronics", "Beauty & Cosmetics", "Sports & Outdoors", "Toys & Games", "Food & Beverage", "Other"])
    
    with col2:
        st.selectbox("E-commerce Platform", ["Shopify", "Magento", "WooCommerce", "BigCommerce", "Custom Platform", "Other"])
    
    # Current performance metrics
    st.markdown("### Current Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        monthly_traffic = st.number_input("Monthly Website Traffic", min_value=0, value=100000)
    
    with col2:
        conversion_rate = st.number_input("Conversion Rate (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1)
    
    with col3:
        average_order_value = st.number_input("Average Order Value ($)", min_value=0, value=75)
    
    # Advanced metrics (optional)
    with st.expander("Advanced Metrics (Optional)"):
        col1, col2 = st.columns(2)
        
        with col1:
            organic_traffic_percentage = st.slider("Organic Traffic Percentage", 0, 100, 40)
            current_seo_spend = st.number_input("Monthly SEO Spend ($)", min_value=0, value=5000)
        
        with col2:
            product_count = st.number_input("Total Product Count", min_value=0, value=5000)
            category_count = st.number_input("Total Category Count", min_value=0, value=50)
    
    # Business goals
    st.markdown("### Business Goals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        primary_goal = st.selectbox("Primary Goal", [
            "Increase organic traffic",
            "Improve conversion rates",
            "Optimize product visibility",
            "Enhance category structure",
            "Reduce PPC dependency",
            "Improve overall revenue"
        ])
    
    with col2:
        timeline = st.selectbox("Implementation Timeline", [
            "0-3 months",
            "3-6 months",
            "6-12 months",
            "12+ months"
        ])
    
    # Calculate button
    if st.button("Calculate ROI"):
        # Calculating current metrics
        monthly_orders = monthly_traffic * (conversion_rate / 100)
        monthly_revenue = monthly_orders * average_order_value
        annual_revenue = monthly_revenue * 12
        
        # Estimated improvements with Metis (example values)
        traffic_increase = 0.25  # 25% increase in traffic
        conversion_increase = 0.15  # 15% increase in conversion rate
        
        # Calculate new metrics
        new_monthly_traffic = monthly_traffic * (1 + traffic_increase)
        new_conversion_rate = conversion_rate * (1 + conversion_increase)
        new_monthly_orders = new_monthly_traffic * (new_conversion_rate / 100)
        new_monthly_revenue = new_monthly_orders * average_order_value
        new_annual_revenue = new_monthly_revenue * 12
        
        # Calculate ROI
        revenue_increase = new_annual_revenue - annual_revenue
        estimated_cost = 25000  # Example annual cost of Metis
        roi_percentage = (revenue_increase - estimated_cost) / estimated_cost * 100
        
        # Display results
        st.markdown("### Your Estimated Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; text-align: center;">
                <h4>Annual Revenue Increase</h4>
                <p style="font-size: 24px; font-weight: bold; color: #7B68EE;">${round(revenue_increase / 1000000, 2)}M</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; text-align: center;">
                <h4>ROI</h4>
                <p style="font-size: 24px; font-weight: bold; color: #7B68EE;">{round(roi_percentage)}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; text-align: center;">
                <h4>Payback Period</h4>
                <p style="font-size: 24px; font-weight: bold; color: #7B68EE;">{round(12 * estimated_cost / revenue_increase)} months</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed breakdown
        st.markdown("### Detailed Breakdown")
        
        st.markdown(f"""
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Current</th>
                    <th>Projected</th>
                    <th>Improvement</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Monthly Traffic</td>
                    <td>{int(monthly_traffic):,}</td>
                    <td>{int(new_monthly_traffic):,}</td>
                    <td>+{traffic_increase * 100:.1f}%</td>
                </tr>
                <tr>
                    <td>Conversion Rate</td>
                    <td>{conversion_rate:.2f}%</td>
                    <td>{new_conversion_rate:.2f}%</td>
                    <td>+{conversion_increase * 100:.1f}%</td>
                </tr>
                <tr>
                    <td>Monthly Orders</td>
                    <td>{int(monthly_orders):,}</td>
                    <td>{int(new_monthly_orders):,}</td>
                    <td>+{(new_monthly_orders / monthly_orders - 1) * 100:.1f}%</td>
                </tr>
                <tr>
                    <td>Monthly Revenue</td>
                    <td>${int(monthly_revenue):,}</td>
                    <td>${int(new_monthly_revenue):,}</td>
                    <td>+{(new_monthly_revenue / monthly_revenue - 1) * 100:.1f}%</td>
                </tr>
                <tr>
                    <td>Annual Revenue</td>
                    <td>${int(annual_revenue):,}</td>
                    <td>${int(new_annual_revenue):,}</td>
                    <td>+{(new_annual_revenue / annual_revenue - 1) * 100:.1f}%</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)
        
        # ROI chart placeholder (in a real implementation, this would be a chart)
        st.markdown("### ROI Timeline")
        st.markdown("```python\n# This would be a line chart showing ROI over time\n```")
        
        # Next steps
        st.markdown("### Recommended Next Steps")
        st.markdown("""
        Based on your input, we recommend:
        
        1. **Schedule a personalized demo** to see how Metis can address your specific needs
        2. **Request a custom ROI analysis** from our team with more detailed projections
        3. **Begin a pilot implementation** to validate these projections in your environment
        """)
        
        # Call-to-action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.button("Schedule Demo")
        
        with col2:
            st.button("Request Custom Analysis")
        
        with col3:
            st.button("Start Pilot Program")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main app logic
def main():
    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.user_type is None:
        select_user_type()
    else:
        sidebar()
        
        # Navigation to different pages based on session state
        if st.session_state.current_course is None:
            course_catalog()
        elif st.session_state.current_course == "progress":
            progress_page()
        elif st.session_state.current_course == "certifications":
            certifications_page()
        elif st.session_state.current_course == "settings":
            settings_page()
        # Employee-specific pages
        elif st.session_state.current_course == "manage_users" and st.session_state.user_type == "employee":
            manage_users_page()
        elif st.session_state.current_course == "usage_analytics" and st.session_state.user_type == "employee":
            usage_analytics_page()
        # Partner-specific pages
        elif st.session_state.current_course == "api_docs" and st.session_state.user_type == "partner":
            api_docs_page()
        elif st.session_state.current_course == "marketing_materials" and st.session_state.user_type == "partner":
            marketing_materials_page()
        # Customer-specific pages
        elif st.session_state.current_course == "faqs" and st.session_state.user_type == "customer":
            faqs_page()
        elif st.session_state.current_course == "roi_calculator" and st.session_state.user_type == "customer":
            roi_calculator_page()
        else:
            # Display a course and its modules
            course_page(st.session_state.current_course)

if __name__ == "__main__":
    main()
