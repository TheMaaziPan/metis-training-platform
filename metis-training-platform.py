import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO

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
    .css-1d391kg {
        background-color: var(--metis-purple);
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
</style>
""", unsafe_allow_html=True)

# Mock user data
class User:
    def __init__(self, name, role, progress=0):
        self.name = name
        self.role = role
        self.progress = progress
        self.completed_modules = []

# Mock course data
courses = [
    {
        "id": 1,
        "title": "Introduction to Metis",
        "description": "Learn the basics of the Metis platform and its key features.",
        "modules": [
            {"id": 1, "title": "What is Metis?", "duration": "10 min"},
            {"id": 2, "title": "Navigating the Dashboard", "duration": "15 min"},
            {"id": 3, "title": "Understanding Key Metrics", "duration": "20 min"}
        ]
    },
    {
        "id": 2,
        "title": "Category Monitoring",
        "description": "Master the Category Monitoring tools to improve organic visibility.",
        "modules": [
            {"id": 1, "title": "Category Overview", "duration": "15 min"},
            {"id": 2, "title": "Filtering and Analysis", "duration": "25 min"},
            {"id": 3, "title": "Optimization Techniques", "duration": "30 min"}
        ]
    },
    {
        "id": 3,
        "title": "Product Visibility",
        "description": "Learn how to boost onsite visibility of products using Metis tools.",
        "modules": [
            {"id": 1, "title": "Product Visibility Basics", "duration": "20 min"},
            {"id": 2, "title": "Position Analysis", "duration": "25 min"},
            {"id": 3, "title": "Visibility Optimization", "duration": "35 min"}
        ]
    },
    {
        "id": 4,
        "title": "Category Merchandising",
        "description": "Maximize revenue through effective onsite merchandising strategies.",
        "modules": [
            {"id": 1, "title": "Merchandising Fundamentals", "duration": "20 min"},
            {"id": 2, "title": "Opportunity Scoring", "duration": "30 min"},
            {"id": 3, "title": "Revenue Optimization", "duration": "40 min"}
        ]
    }
]

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = User("Nigel Thompson", "Website Content Editor", 35)
    st.session_state.current_course = None
    st.session_state.current_module = None
    st.session_state.logged_in = False

# Authentication page
def login_page():
    st.markdown('<h1 class="main-header">MediaVision Metis Training Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Login to access your training modules</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="metis-card">', unsafe_allow_html=True)
        st.markdown("### Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username and password:  # In a real app, check credentials
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Please enter username and password")
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

# Sidebar navigation
def sidebar():
    st.sidebar.markdown("""
    <div style="padding: 15px 0; text-align: center; color: white;">
        <h3 style="margin: 0;">(M) MediaVision Metis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # User profile
    st.sidebar.markdown(f"""
    <div class="user-profile" style="background-color: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 20px;">
        <img src="https://via.placeholder.com/40" alt="Profile">
        <div>
            <div style="color: white; font-weight: bold;">{st.session_state.user.name}</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.8em;">{st.session_state.user.role}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.sidebar.markdown("### Navigation")
    
    if st.sidebar.button("📚 Course Catalog"):
        st.session_state.current_course = None
        st.session_state.current_module = None
    
    if st.sidebar.button("📊 My Progress"):
        st.session_state.current_course = "progress"
    
    if st.sidebar.button("🏆 Certifications"):
        st.session_state.current_course = "certifications"
    
    if st.sidebar.button("⚙️ Settings"):
        st.session_state.current_course = "settings"
    
    # Logout button at the bottom
    st.sidebar.markdown("<div style='position: fixed; bottom: 20px; width: inherit;'>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Course catalog page
def course_catalog():
    st.markdown('<h1 class="main-header">Course Catalog</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Select a course to begin or continue your training</p>', unsafe_allow_html=True)
    
    # Progress overview
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown("### Your Learning Progress")
    st.progress(st.session_state.user.progress / 100)
    st.markdown(f"You've completed **{st.session_state.user.progress}%** of the available training material.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Course grid
    st.markdown("### Available Courses")
    
    # Create two columns for the courses
    col1, col2 = st.columns(2)
    
    # Display courses in a grid
    for i, course in enumerate(courses):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f'<div class="metis-card">', unsafe_allow_html=True)
            st.markdown(f"#### {course['title']}")
            st.markdown(f"{course['description']}")
            st.markdown("**Modules:**")
            for module in course['modules']:
                st.markdown(f"- {module['title']} ({module['duration']})")
            
            # Enter course button
            if st.button(f"Start Course", key=f"start_{course['id']}"):
                st.session_state.current_course = course['id']
                st.session_state.current_module = course['modules'][0]['id']
                st.experimental_rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# Course page
def course_page(course_id):
    course = next((c for c in courses if c['id'] == course_id), None)
    
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
                st.experimental_rerun()
        
        if st.button("Back to Catalog"):
            st.session_state.current_course = None
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Display the current module content
        module = next((m for m in course['modules'] if m['id'] == st.session_state.current_module), course['modules'][0])
        
        st.markdown('<div class="metis-card">', unsafe_allow_html=True)
        st.markdown(f"### {module['title']}")
        st.markdown(f"Duration: {module['duration']}")
        
        # Module content would go here
        if course['id'] == 1 and module['id'] == 1:
            # Introduction module content
            st.markdown("""
            ## What is Metis?
            
            Metis is MediaVision's proprietary e-commerce analytics and optimization platform. It provides:
            
            - **Category Monitoring**: Track and improve organic visibility of your PLPs (Product Listing Pages)
            - **Product Visibility**: Boost onsite visibility of individual products
            - **Category Merchandising**: Maximize revenue through effective positioning strategies
            
            The platform analyzes data from your e-commerce site to provide actionable insights and recommendations.
            """)
            
            # Example image placeholder
            st.image("https://via.placeholder.com/800x400?text=Metis+Platform+Overview", use_column_width=True)
            
            # Quiz at the end of the module
            st.markdown("### Quick Knowledge Check")
            quiz_q1 = st.radio("What is the primary purpose of Metis?", [
                "Social media management",
                "E-commerce analytics and optimization",
                "Content creation",
                "Email marketing"
            ])
            
            if st.button("Submit Answer"):
                if quiz_q1 == "E-commerce analytics and optimization":
                    st.success("Correct! Metis is focused on e-commerce analytics and optimization.")
                else:
                    st.error("That's not quite right. Metis is an e-commerce analytics and optimization platform.")
        
        elif course['id'] == 2 and module['id'] == 1:
            # Category Monitoring module content
            st.markdown("""
            ## Category Overview
            
            The Category Monitoring tool in Metis helps you track and improve the organic visibility of your Product Listing Pages (PLPs).
            
            Key features include:
            - Tracking inbound and outbound links
            - Monitoring SEO performance
            - Identifying optimization opportunities
            
            The main dashboard displays:
            - Product counts
            - Page titles
            - SEO metrics
            - Link performance
            """)
            
            # Example image placeholder
            st.image("https://via.placeholder.com/800x400?text=Category+Monitoring+Dashboard", use_column_width=True)
            
        elif course['id'] == 3 and module['id'] == 1:
            # Product Visibility module
            st.markdown("""
            ## Product Visibility Basics
            
            The Product Visibility tool helps you analyze and optimize how products appear on your website.
            
            Key features:
            - Track product positions within categories
            - Monitor clicks and conversion rates
            - Identify underperforming products
            - Optimize placement for better results
            
            This tool is essential for merchandisers looking to maximize product visibility and sales.
            """)
            
            # Example image placeholder
            st.image("https://via.placeholder.com/800x400?text=Product+Visibility+Tool", use_column_width=True)
        
        elif course['id'] == 4 and module['id'] == 1:
            # Category Merchandising module
            st.markdown("""
            ## Merchandising Fundamentals
            
            Category Merchandising in Metis allows you to analyze and optimize how products are displayed within categories to maximize revenue.
            
            Key features:
            - Opportunity scoring to identify high-potential products
            - Category analysis tools
            - Date tracking for performance over time
            - Product code and attribute analysis
            
            Effective merchandising strategies can significantly impact conversion rates and average order value.
            """)
            
            # Example image placeholder
            st.image("https://via.placeholder.com/800x400?text=Category+Merchandising+Tool", use_column_width=True)
        
        else:
            st.markdown("Content for this module is being developed. Check back soon!")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.session_state.current_module > 1:
                if st.button("← Previous Module"):
                    st.session_state.current_module -= 1
                    st.experimental_rerun()
        
        with col3:
            if st.session_state.current_module < len(course['modules']):
                if st.button("Next Module →"):
                    st.session_state.current_module += 1
                    st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Progress page
def progress_page():
    st.markdown('<h1 class="main-header">My Learning Progress</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Track your training completion and achievements</p>', unsafe_allow_html=True)
    
    # Overall progress
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown("### Overall Completion")
    st.progress(st.session_state.user.progress / 100)
    st.markdown(f"You've completed **{st.session_state.user.progress}%** of all available training material.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Progress by course
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown("### Progress by Course")
    
    # Mock data for demonstration
    course_progress = [
        {"course": "Introduction to Metis", "progress": 100},
        {"course": "Category Monitoring", "progress": 67},
        {"course": "Product Visibility", "progress": 33},
        {"course": "Category Merchandising", "progress": 0}
    ]
    
    for course in course_progress:
        st.markdown(f"**{course['course']}**")
        st.progress(course['progress'] / 100)
        st.markdown(f"{course['progress']}% complete")
        st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown("### Recent Activity")
    
    # Sample activity data
    activities = [
        {"date": "April 28, 2025", "activity": "Completed 'Navigating the Dashboard' module"},
        {"date": "April 26, 2025", "activity": "Started 'Category Monitoring' course"},
        {"date": "April 25, 2025", "activity": "Completed 'Introduction to Metis' course"},
        {"date": "April 23, 2025", "activity": "Completed 'What is Metis?' module"}
    ]
    
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Activity</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)
    
    for activity in activities:
        st.markdown(f"""
        <tr>
            <td>{activity['date']}</td>
            <td>{activity['activity']}</td>
        </tr>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Certifications page
def certifications_page():
    st.markdown('<h1 class="main-header">Certifications</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">View and download your earned certifications</p>', unsafe_allow_html=True)
    
    # Available certifications
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown("### Available Certifications")
    
    # Certificate data
    certificates = [
        {"name": "Metis Fundamentals", "status": "Completed", "date": "April 25, 2025"},
        {"name": "Category Monitoring Specialist", "status": "In Progress", "date": "-"},
        {"name": "Product Visibility Expert", "status": "Not Started", "date": "-"},
        {"name": "Category Merchandising Professional", "status": "Not Started", "date": "-"},
        {"name": "Metis Platform Master", "status": "Not Started", "date": "-"}
    ]
    
    st.markdown("""
    <table class="styled-table">
        <thead>
            <tr>
                <th>Certification</th>
                <th>Status</th>
                <th>Completion Date</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)
    
    for cert in certificates:
        button = ""
        if cert["status"] == "Completed":
            button = '<button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Download</button>'
        elif cert["status"] == "In Progress":
            button = '<button style="background-color: #6C757D; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Continue Training</button>'
        else:
            button = '<button style="background-color: #6C757D; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Start</button>'
        
        st.markdown(f"""
        <tr class='{"active-row" if cert["status"] == "Completed" else ""}'>
            <td>{cert["name"]}</td>
            <td>{cert["status"]}</td>
            <td>{cert["date"]}</td>
            <td>{button}</td>
        </tr>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display certificate
    if certificates[0]["status"] == "Completed":
        st.markdown('<div class="metis-card">', unsafe_allow_html=True)
        st.markdown("### Metis Fundamentals Certificate")
        
        # Sample certificate display
        st.markdown("""
        <div style="border: 2px solid #7B68EE; border-radius: 10px; padding: 20px; text-align: center; background-color: #f9f9ff;">
            <h2 style="color: #2B2D42;">Certificate of Completion</h2>
            <h3>Metis Fundamentals</h3>
            <p>This certifies that</p>
            <h3>Nigel Thompson</h3>
            <p>has successfully completed the Metis Fundamentals training</p>
            <p>Awarded on April 25, 2025</p>
            <div style="margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px;">
                <p>MediaVision Metis Training Academy</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Settings page
def settings_page():
    st.markdown('<h1 class="main-header">Settings</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Manage your account and preferences</p>', unsafe_allow_html=True)
    
    # Profile settings
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown("### Profile Settings")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <img src="https://via.placeholder.com/150" style="border-radius: 50%; margin-bottom: 10px;">
            <button style="background-color: #7B68EE; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Change Photo</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.text_input("Full Name", value=st.session_state.user.name)
        st.text_input("Job Title", value=st.session_state.user.role)
        st.text_input("Email", value="nigel.thompson@example.com")
        st.text_input("Department", value="Content")
    
    if st.button("Save Profile Changes"):
        st.success("Profile updated successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Notification settings
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown("### Notification Settings")
    
    st.checkbox("Email notifications for new courses", value=True)
    st.checkbox("Email notifications for course completions", value=True)
    st.checkbox("Weekly progress summary", value=False)
    st.checkbox("Certificate alerts", value=True)
    
    if st.button("Save Notification Preferences"):
        st.success("Notification preferences updated!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Password change
    st.markdown('<div class="metis-card">', unsafe_allow_html=True)
    st.markdown("### Change Password")
    
    st.text_input("Current Password", type="password")
    st.text_input("New Password", type="password")
    st.text_input("Confirm New Password", type="password")
    
    if st.button("Update Password"):
        st.success("Password updated successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main app logic
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        sidebar()
        
        if st.session_state.current_course is None:
            course_catalog()
        elif st.session_state.current_course == "progress":
            progress_page()
        elif st.session_state.current_course == "certifications":
            certifications_page()
        elif st.session_state.current_course == "settings":
            settings_page()
        else:
            course_page(st.session_state.current_course)

if __name__ == "__main__":
    main()
