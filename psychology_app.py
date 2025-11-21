import streamlit as st
from datetime import datetime
import json
import os
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="MindfulMe - Your Wellness Companion",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #6366f1;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #4f46e5;
    }
    .gratitude-card {
        background-color: #f0f9ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #6366f1;
    }
    .affirmation-card {
        background-color: #fef3c7;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 500;
        color: #92400e;
    }
    .jar-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-box {
        background-color: #f3f4f6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = []
if 'gratitude_jar' not in st.session_state:
    st.session_state.gratitude_jar = []
if 'affirmations' not in st.session_state:
    st.session_state.affirmations = [
        "I am worthy of love and respect",
        "I choose to be happy and positive today",
        "I am capable of achieving my goals",
        "I embrace my unique qualities and strengths",
        "I am growing and improving every day",
        "I deserve good things in my life",
        "I am confident in my abilities",
        "I choose to focus on what I can control",
        "I am grateful for all the good in my life",
        "I am enough, just as I am",
        "I trust myself to make good decisions",
        "I am resilient and can overcome challenges",
        "I radiate positivity and kindness",
        "I am proud of how far I've come",
        "I choose peace over worry"
    ]

# Data persistence functions
DATA_FILE = Path("mindfulme_data.json")

def save_data():
    """Save all data to a JSON file"""
    data = {
        'journal_entries': st.session_state.journal_entries,
        'gratitude_jar': st.session_state.gratitude_jar
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_data():
    """Load data from JSON file"""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                st.session_state.journal_entries = data.get('journal_entries', [])
                st.session_state.gratitude_jar = data.get('gratitude_jar', [])
        except:
            pass

# Load existing data
load_data()

# Sidebar navigation
st.sidebar.title("🌸 MindfulMe")
st.sidebar.markdown("*Your Wellness Companion*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Home", "📔 Gratitude Journal", "🏺 Gratitude Jar", "✨ Self Affirmations", "📊 My Progress"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Daily Tip")
st.sidebar.info("Taking just 5 minutes each day for gratitude practice can significantly improve your mental well-being!")

# HOME PAGE
if page == "🏠 Home":
    st.title("🌸 Welcome to MindfulMe")
    st.markdown("### Your Personal Wellness Companion")
    
    st.markdown("""
    Welcome! This app is designed to support your mental wellness journey through proven psychological practices:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-box">
            <h3>📔</h3>
            <h4>Gratitude Journal</h4>
            <p>Reflect on daily blessings and cultivate positivity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-box">
            <h3>🏺</h3>
            <h4>Gratitude Jar</h4>
            <p>Collect moments of joy to revisit anytime</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-box">
            <h3>✨</h3>
            <h4>Self Affirmations</h4>
            <p>Build confidence with positive self-talk</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🌟 Quick Stats")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Journal Entries", len(st.session_state.journal_entries))
    with col2:
        st.metric("Gratitude Notes", len(st.session_state.gratitude_jar))
    with col3:
        total_days = len(set([entry['date'] for entry in st.session_state.journal_entries]))
        st.metric("Days Practiced", total_days)
    
    st.markdown("---")
    st.markdown("### 🧠 Why These Practices Matter")
    
    with st.expander("📖 The Science Behind Gratitude"):
        st.markdown("""
        Research shows that regular gratitude practice can:
        - Increase happiness and life satisfaction
        - Reduce symptoms of depression and anxiety
        - Improve sleep quality
        - Strengthen relationships
        - Boost physical health and immunity
        """)
    
    with st.expander("🔬 The Power of Affirmations"):
        st.markdown("""
        Self-affirmations work by:
        - Activating reward centers in the brain
        - Reducing stress and defensive responses
        - Improving problem-solving abilities
        - Building self-confidence and resilience
        - Creating positive neural pathways
        """)

# GRATITUDE JOURNAL PAGE
elif page == "📔 Gratitude Journal":
    st.title("📔 Gratitude Journal")
    st.markdown("*Take a moment to reflect on what you're grateful for today*")
    
    tab1, tab2 = st.tabs(["✍️ New Entry", "📖 Past Entries"])
    
    with tab1:
        st.markdown("### Today's Gratitude")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            entry_date = st.date_input("Date", datetime.now())
        with col2:
            mood = st.select_slider(
                "How are you feeling?",
                options=["😢", "😕", "😐", "🙂", "😊"],
                value="😊"
            )
        
        st.markdown("#### What are you grateful for today?")
        gratitude_1 = st.text_area(
            "First thing I'm grateful for:",
            placeholder="Example: I'm grateful for my supportive friend who listened to me today...",
            height=100
        )
        
        gratitude_2 = st.text_area(
            "Second thing I'm grateful for:",
            placeholder="Example: I'm grateful for the beautiful sunrise I witnessed this morning...",
            height=100
        )
        
        gratitude_3 = st.text_area(
            "Third thing I'm grateful for:",
            placeholder="Example: I'm grateful for my health and the energy I had today...",
            height=100
        )
        
        reflection = st.text_area(
            "Optional: Any additional reflections?",
            placeholder="How did focusing on gratitude make you feel?",
            height=80
        )
        
        if st.button("💾 Save Journal Entry"):
            if gratitude_1 or gratitude_2 or gratitude_3:
                new_entry = {
                    'date': entry_date.strftime("%Y-%m-%d"),
                    'mood': mood,
                    'gratitudes': [g for g in [gratitude_1, gratitude_2, gratitude_3] if g],
                    'reflection': reflection,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.journal_entries.append(new_entry)
                save_data()
                st.success("✅ Journal entry saved successfully!")
                st.balloons()
            else:
                st.warning("Please write at least one thing you're grateful for!")
    
    with tab2:
        st.markdown("### Your Gratitude History")
        
        if st.session_state.journal_entries:
            # Sort entries by date (newest first)
            sorted_entries = sorted(
                st.session_state.journal_entries,
                key=lambda x: x['date'],
                reverse=True
            )
            
            for entry in sorted_entries:
                with st.container():
                    st.markdown(f"""
                    <div class="gratitude-card">
                        <h4>{entry['mood']} {entry['date']}</h4>
                    """, unsafe_allow_html=True)
                    
                    for i, gratitude in enumerate(entry['gratitudes'], 1):
                        st.markdown(f"**{i}.** {gratitude}")
                    
                    if entry.get('reflection'):
                        st.markdown(f"*Reflection: {entry['reflection']}*")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No journal entries yet. Start your gratitude practice today!")

# GRATITUDE JAR PAGE
elif page == "🏺 Gratitude Jar":
    st.title("🏺 Gratitude Jar")
    st.markdown("*Drop notes of gratitude into your virtual jar and revisit them anytime*")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Add to Your Jar")
        
        jar_note = st.text_area(
            "What moment of joy or gratitude do you want to remember?",
            placeholder="Example: Had a wonderful conversation with my mom today that made me smile...",
            height=150
        )
        
        category = st.selectbox(
            "Category (optional)",
            ["✨ General", "❤️ Relationships", "🎯 Achievement", "🌅 Nature", "🎨 Creativity", "💪 Health", "🎉 Joy"]
        )
        
        if st.button("🎊 Add to Jar"):
            if jar_note:
                new_note = {
                    'note': jar_note,
                    'category': category,
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.gratitude_jar.append(new_note)
                save_data()
                st.success("✅ Added to your gratitude jar!")
                st.balloons()
            else:
                st.warning("Please write something before adding to the jar!")
    
    with col2:
        st.markdown("### 🎲 Random Note from Jar")
        st.markdown("*Need a pick-me-up? Draw a random note!*")
        
        if st.button("🎁 Pick a Random Note") and st.session_state.gratitude_jar:
            import random
            random_note = random.choice(st.session_state.gratitude_jar)
            st.markdown(f"""
            <div class="affirmation-card">
                {random_note['category']}<br><br>
                "{random_note['note']}"<br><br>
                <small>- {random_note['date']}</small>
            </div>
            """, unsafe_allow_html=True)
        elif not st.session_state.gratitude_jar:
            st.info("Your jar is empty. Add some notes first!")
    
    st.markdown("---")
    st.markdown("### 🏺 Your Gratitude Collection")
    
    if st.session_state.gratitude_jar:
        # Filter by category
        categories = ["All"] + list(set([note['category'] for note in st.session_state.gratitude_jar]))
        selected_category = st.selectbox("Filter by category:", categories)
        
        # Display notes
        filtered_notes = st.session_state.gratitude_jar if selected_category == "All" else [
            note for note in st.session_state.gratitude_jar if note['category'] == selected_category
        ]
        
        sorted_notes = sorted(filtered_notes, key=lambda x: x['timestamp'], reverse=True)
        
        for note in sorted_notes:
            st.markdown(f"""
            <div class="jar-item">
                <strong>{note['category']}</strong> - {note['date']}<br>
                {note['note']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Your gratitude jar is empty. Start adding moments you want to remember!")

# SELF AFFIRMATIONS PAGE
elif page == "✨ Self Affirmations":
    st.title("✨ Self Affirmations")
    st.markdown("*Positive self-talk to build confidence and resilience*")
    
    tab1, tab2 = st.tabs(["🎯 Daily Affirmation", "📚 All Affirmations"])
    
    with tab1:
        st.markdown("### Your Daily Affirmation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🔄 Get New Affirmation", use_container_width=True):
                import random
                st.session_state.current_affirmation = random.choice(st.session_state.affirmations)
            
            if 'current_affirmation' not in st.session_state:
                import random
                st.session_state.current_affirmation = random.choice(st.session_state.affirmations)
            
            st.markdown(f"""
            <div class="affirmation-card">
                "{st.session_state.current_affirmation}"
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💡 How to Use")
            st.markdown("""
            1. Read the affirmation slowly
            2. Take a deep breath
            3. Repeat it 3 times
            4. Feel it in your heart
            5. Believe in yourself
            """)
        
        st.markdown("---")
        st.markdown("### ✍️ Create Your Own Affirmation")
        
        custom_affirmation = st.text_input(
            "Write a personal affirmation:",
            placeholder="I am..."
        )
        
        if st.button("➕ Add My Affirmation"):
            if custom_affirmation and custom_affirmation not in st.session_state.affirmations:
                st.session_state.affirmations.append(custom_affirmation)
                st.success("✅ Your personal affirmation has been added!")
            elif custom_affirmation in st.session_state.affirmations:
                st.info("This affirmation already exists!")
            else:
                st.warning("Please write an affirmation first!")
    
    with tab2:
        st.markdown("### 📚 Complete Affirmation Library")
        
        col_count = 2
        cols = st.columns(col_count)
        
        for idx, affirmation in enumerate(st.session_state.affirmations):
            with cols[idx % col_count]:
                st.markdown(f"""
                <div class="gratitude-card">
                    💫 {affirmation}
                </div>
                """, unsafe_allow_html=True)

# MY PROGRESS PAGE
elif page == "📊 My Progress":
    st.title("📊 My Progress")
    st.markdown("*Track your wellness journey*")
    
    if st.session_state.journal_entries or st.session_state.gratitude_jar:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Journal Entries",
                len(st.session_state.journal_entries),
                delta="Keep it up!" if len(st.session_state.journal_entries) > 0 else None
            )
        
        with col2:
            st.metric(
                "Gratitude Notes",
                len(st.session_state.gratitude_jar)
            )
        
        with col3:
            unique_days = len(set([entry['date'] for entry in st.session_state.journal_entries]))
            st.metric(
                "Days Practiced",
                unique_days
            )
        
        with col4:
            if unique_days >= 7:
                streak_msg = "🔥 Week Streak!"
            elif unique_days >= 3:
                streak_msg = "⭐ Great Start!"
            else:
                streak_msg = "🌱 Beginning"
            st.metric("Achievement", streak_msg)
        
        st.markdown("---")
        
        # Mood tracking
        if st.session_state.journal_entries:
            st.markdown("### 😊 Mood Tracking")
            
            mood_counts = {}
            for entry in st.session_state.journal_entries:
                mood = entry.get('mood', '😐')
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Mood Distribution")
                for mood, count in sorted(mood_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(st.session_state.journal_entries)) * 100
                    st.markdown(f"{mood} {mood}: {count} times ({percentage:.1f}%)")
            
            with col2:
                st.markdown("#### Recent Entries")
                recent = sorted(
                    st.session_state.journal_entries,
                    key=lambda x: x['date'],
                    reverse=True
                )[:5]
                for entry in recent:
                    st.markdown(f"- {entry['mood']} {entry['date']}")
        
        st.markdown("---")
        st.markdown("### 🎯 Your Achievements")
        
        achievements = []
        if len(st.session_state.journal_entries) >= 1:
            achievements.append("🌟 First Journal Entry")
        if len(st.session_state.journal_entries) >= 7:
            achievements.append("📚 Week of Gratitude")
        if len(st.session_state.journal_entries) >= 30:
            achievements.append("🏆 Month of Mindfulness")
        if len(st.session_state.gratitude_jar) >= 10:
            achievements.append("🏺 Jar Collector")
        if len(st.session_state.gratitude_jar) >= 50:
            achievements.append("💎 Gratitude Master")
        
        if achievements:
            cols = st.columns(min(len(achievements), 4))
            for idx, achievement in enumerate(achievements):
                with cols[idx % 4]:
                    st.success(achievement)
        else:
            st.info("Keep practicing to unlock achievements!")
        
    else:
        st.info("Start your wellness journey to see your progress here!")
        st.markdown("### 🚀 Getting Started")
        st.markdown("""
        - Write your first gratitude journal entry
        - Add notes to your gratitude jar
        - Practice daily affirmations
        - Watch your progress grow!
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 2rem;'>
    <p>🌸 MindfulMe - Your Wellness Companion</p>
    <p><small>Remember: Small daily practices lead to big changes over time</small></p>
</div>
""", unsafe_allow_html=True)
