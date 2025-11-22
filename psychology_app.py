import json
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import Counter
import random

import pandas as pd
import streamlit as st

# ---------------------- Page Configuration ---------------------- #

st.set_page_config(
    page_title="MindfulMe - Your Wellness Companion",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------- Constants ---------------------- #

DATA_FILE = Path("mindfulme_data.json")

DEFAULT_AFFIRMATIONS = [
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
    "I choose peace over worry",
]

GRATITUDE_CATEGORIES = [
    "✨ General",
    "❤️ Relationships",
    "🎯 Achievement",
    "🌅 Nature",
    "🎨 Creativity",
    "💪 Health",
    "🎉 Joy",
]

JOURNAL_TAGS = [
    "Work / Study",
    "Health & Fitness",
    "Relationships",
    "Personal Growth",
    "Rest & Recovery",
    "Fun & Hobbies",
]

MOOD_OPTIONS = ["😢", "😕", "😐", "🙂", "😊"]
MOOD_SCORES = {"😢": 1, "😕": 2, "😐": 3, "🙂": 4, "😊": 5}

DAILY_TIPS = [
    "Write down three small things that went well today.",
    "Send a kind message to someone you appreciate.",
    "Take a 5-minute walk without your phone.",
    "Notice one thing you can see, hear and feel right now.",
    "Drink a full glass of water mindfully.",
]

DAILY_CHALLENGES = [
    "Pause for 1 minute and take 5 slow breaths.",
    "Write one kind sentence about yourself.",
    "Declutter one small area: a drawer, your desk, or your desktop.",
    "Go outside and notice the sky for 30 seconds.",
    "Smile at yourself in the mirror once today.",
]

JOURNAL_PROMPTS = [
    "Something small that made today a little better:",
    "A person who made your life easier this week (and how):",
    "One thing your body allowed you to do today:",
    "A challenge you handled better than you would have a year ago:",
    "A comfort you often take for granted (home, food, internet, etc.):",
    "Something in nature you noticed or appreciated recently:",
    "A skill or quality in yourself that you're grateful for:",
    "One thing that went ‘okay’ today, even if it wasn't perfect:",
    "A mistake that taught you something useful:",
    "One thing you’re looking forward to in the next few days:",
]

# CBT / psychology content
THINKING_TRAPS = {
    "All-or-nothing thinking": {
        "description": "Seeing things in black-and-white categories; if it’s not perfect, it’s a failure.",
        "example": "“If I don’t exercise every day this week, I’m completely off track.”",
    },
    "Catastrophising": {
        "description": "Jumping straight to the worst possible outcome.",
        "example": "“If I make one mistake, I’ll lose my job and never recover.”",
    },
    "Mind reading": {
        "description": "Assuming you know what others are thinking without evidence.",
        "example": "“She didn’t reply quickly… she must be annoyed with me.”",
    },
    "Fortune telling": {
        "description": "Predicting the future as if it’s already decided.",
        "example": "“The interview will definitely go badly; there’s no point trying.”",
    },
    "Shoulds & musts": {
        "description": "Rigid rules about how you or others ‘must’ behave.",
        "example": "“I should always be productive; if I rest, I’m lazy.”",
    },
    "Discounting the positives": {
        "description": "Downplaying or dismissing good things that happen.",
        "example": "“They liked my work, but they were just being polite.”",
    },
    "Overgeneralisation": {
        "description": "Taking one event and seeing it as a never-ending pattern.",
        "example": "“This project failed; everything I do goes wrong.”",
    },
    "Emotional reasoning": {
        "description": "Assuming that because you feel something, it must be true.",
        "example": "“I feel guilty, so I must have done something wrong.”",
    },
    "Personalisation & blame": {
        "description": "Taking too much responsibility for things or blaming yourself for events outside your control.",
        "example": "“My friend is upset; it’s my fault for not being perfect.”",
    },
}

# ---------------------- Custom CSS ---------------------- #

st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)

# ---------------------- Session State Init ---------------------- #

if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

if "gratitude_jar" not in st.session_state:
    st.session_state.gratitude_jar = []

if "affirmations" not in st.session_state:
    st.session_state.affirmations = DEFAULT_AFFIRMATIONS.copy()

if "current_affirmation" not in st.session_state:
    st.session_state.current_affirmation = None

if "thought_records" not in st.session_state:
    st.session_state.thought_records = []

if "custom_jar_categories" not in st.session_state:
    st.session_state.custom_jar_categories = []

# ---------------------- Persistence Helpers ---------------------- #


def save_data() -> None:
    """Save all app data to a JSON file."""
    data = {
        "journal_entries": st.session_state.journal_entries,
        "gratitude_jar": st.session_state.gratitude_jar,
        "affirmations": st.session_state.affirmations,
        "thought_records": st.session_state.thought_records,
        "custom_jar_categories": st.session_state.custom_jar_categories,
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving data: {e}")


def load_data() -> None:
    """Load app data from JSON file into session_state."""
    if not DATA_FILE.exists():
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        st.session_state.journal_entries = data.get("journal_entries", [])
        st.session_state.gratitude_jar = data.get("gratitude_jar", [])
        stored_affirmations = data.get("affirmations")
        if stored_affirmations:
            st.session_state.affirmations = stored_affirmations
        st.session_state.thought_records = data.get("thought_records", [])
        st.session_state.custom_jar_categories = data.get("custom_jar_categories", [])
    except Exception as e:
        st.warning(f"Could not load saved data (it might be corrupted): {e}")


# Load existing data once at start
load_data()

# ---------------------- Helper Functions ---------------------- #


def get_unique_practice_days() -> int:
    """Number of unique days with journal entries."""
    return len({entry["date"] for entry in st.session_state.journal_entries})


def get_daily_entry_counts():
    """Return dates and counts for journal entries per day."""
    if not st.session_state.journal_entries:
        return [], []
    counts = Counter(entry["date"] for entry in st.session_state.journal_entries)
    dates_sorted = sorted(counts.keys())
    values = [counts[d] for d in dates_sorted]
    return dates_sorted, values


def get_average_mood():
    """Compute average mood score (1-5) and best representative emoji."""
    scores = []
    for entry in st.session_state.journal_entries:
        mood = entry.get("mood")
        if mood in MOOD_SCORES:
            scores.append(MOOD_SCORES[mood])
    if not scores:
        return None, "😐"
    avg = sum(scores) / len(scores)
    closest_mood = min(MOOD_SCORES.keys(), key=lambda m: abs(MOOD_SCORES[m] - avg))
    return avg, closest_mood


def get_longest_streak():
    """Compute longest streak (in days) of journaling."""
    if not st.session_state.journal_entries:
        return 0
    dates = sorted({entry["date"] for entry in st.session_state.journal_entries})
    date_objs = [datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    longest = 1
    current = 1
    for i in range(1, len(date_objs)):
        if (date_objs[i] - date_objs[i - 1]).days == 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


def get_today_string():
    return datetime.now().strftime("%Y-%m-%d")


def get_tip_of_the_day():
    today = date.today()
    idx = today.toordinal() % len(DAILY_TIPS)
    cidx = today.toordinal() % len(DAILY_CHALLENGES)
    return DAILY_TIPS[idx], DAILY_CHALLENGES[cidx]


def get_all_jar_categories():
    """Built-in + custom jar categories."""
    return GRATITUDE_CATEGORIES + st.session_state.custom_jar_categories


def get_weekly_summary():
    """Simple rule-based weekly summary (last 7 days)."""
    if not st.session_state.journal_entries:
        return None
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    filtered = []
    for e in st.session_state.journal_entries:
        try:
            d = datetime.strptime(e["date"], "%Y-%m-%d").date()
        except Exception:
            continue
        if week_ago <= d <= today:
            filtered.append(e)
    if not filtered:
        return None
    # stats
    count = len(filtered)
    moods = [e.get("mood") for e in filtered if e.get("mood") in MOOD_SCORES]
    if moods:
        avg_score = sum(MOOD_SCORES[m] for m in moods) / len(moods)
        avg_face = min(MOOD_SCORES.keys(), key=lambda m: abs(MOOD_SCORES[m] - avg_score))
    else:
        avg_score, avg_face = None, "😐"
    all_tags = []
    for e in filtered:
        all_tags.extend(e.get("tags", []))
    top_tag = None
    if all_tags:
        counts = Counter(all_tags)
        top_tag = counts.most_common(1)[0][0]
    return {
        "count": count,
        "avg_score": avg_score,
        "avg_face": avg_face,
        "top_tag": top_tag,
    }


def get_prompts_for_date(d: date, n: int = 3):
    """Return n stable prompts for the given date (so they don't change on every rerun)."""
    if not JOURNAL_PROMPTS:
        return []
    seed = d.toordinal()
    rnd = random.Random(seed)
    prompts = JOURNAL_PROMPTS.copy()
    rnd.shuffle(prompts)
    return prompts[:n]


# ---------------------- Sidebar ---------------------- #

st.sidebar.title("🌸 MindfulMe")
st.sidebar.markdown("*Your Wellness Companion*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    [
        "🏠 Home",
        "📔 Gratitude Journal",
        "🏺 Gratitude Jar",
        "✨ Self Affirmations",
        "📊 My Progress",
        "🧠 Psychology Tools",
        "🧘 Calm Corner",
    ],
)

st.sidebar.markdown("---")

tip, challenge = get_tip_of_the_day()
st.sidebar.markdown("### 💡 Today’s Tip")
st.sidebar.info(tip)

st.sidebar.markdown("### 🎯 Mini Challenge")
st.sidebar.caption(challenge)

# Today check-in
today_str = get_today_string()
has_today_entry = any(e["date"] == today_str for e in st.session_state.journal_entries)
if has_today_entry:
    st.sidebar.success("You’ve logged gratitude today ✅")
else:
    st.sidebar.warning("No journal entry yet today 🌱")

# ---------------------- Pages ---------------------- #

# HOME PAGE
if page == "🏠 Home":
    st.title("🌸 Welcome to MindfulMe")
    st.markdown("### Your Personal Wellness Companion")

    st.markdown(
        """
    This app combines gratitude, gentle behavioural tools, and psychology-inspired exercises
    to support your day-to-day mental wellbeing. It is **not** a replacement for professional care.
    """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div class="stat-box">
            <h3>📔</h3>
            <h4>Gratitude Journal</h4>
            <p>Reflect on daily blessings and cultivate positivity</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="stat-box">
            <h3>🏺</h3>
            <h4>Gratitude Jar</h4>
            <p>Collect moments of joy to revisit anytime</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="stat-box">
            <h3>✨</h3>
            <h4>Self Affirmations</h4>
            <p>Build confidence with positive self-talk</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown("### 🌟 Quick Stats")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Journal Entries", len(st.session_state.journal_entries))

    with c2:
        st.metric("Gratitude Notes", len(st.session_state.gratitude_jar))

    with c3:
        total_days = get_unique_practice_days()
        st.metric("Days Practiced", total_days)

    # Affirmation of the day
    if st.session_state.affirmations:
        today_ord = date.today().toordinal()
        aff = st.session_state.affirmations[today_ord % len(st.session_state.affirmations)]
        st.markdown("### ✨ Affirmation of the Day")
        st.markdown(
            f"""
        <div class="affirmation-card">
            "{aff}"
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Snapshot
    if st.session_state.journal_entries:
        avg_mood, mood_face = get_average_mood()
        longest_streak = get_longest_streak()
        weekly = get_weekly_summary()

        st.markdown("---")
        st.markdown("### 🧾 Snapshot of Your Journey")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.metric("Average Mood", f"{avg_mood:.1f}/5" if avg_mood else "–", delta=mood_face)
        with s2:
            st.metric("Longest Streak", f"{longest_streak} days")
        with s3:
            st.metric("Thought Records Done", len(st.session_state.thought_records))

        if weekly:
            st.markdown("### 📅 Last 7 Days (Summary)")
            desc = f"- Entries: **{weekly['count']}**"
            if weekly["avg_score"] is not None:
                desc += f"<br>- Average mood: **{weekly['avg_score']:.1f}/5** {weekly['avg_face']}"
            if weekly["top_tag"]:
                desc += f"<br>- Most frequent theme: **{weekly['top_tag']}**"
            st.markdown(desc, unsafe_allow_html=True)

    st.markdown("---")

    # Quick one-line gratitude
    with st.expander("✍️ Quick One-Line Gratitude"):
        quick_text = st.text_input(
            "One thing you're grateful for right now:",
            key="quick_gratitude",
            placeholder="I'm grateful for...",
        )
        if st.button("➕ Save Quick Gratitude", key="save_quick_gratitude"):
            if quick_text.strip():
                new_entry = {
                    "date": today_str,
                    "mood": "🙂",
                    "gratitudes": [quick_text.strip()],
                    "reflection": "",
                    "intention": "",
                    "tags": [],
                    "favorite": False,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.session_state.journal_entries.append(new_entry)
                save_data()
                st.success("✅ Saved! Nice tiny moment of gratitude.")
            else:
                st.warning("Write at least a few words before saving.")

    st.markdown("### 🧠 Why These Practices Matter")

    with st.expander("📖 The Science Behind Gratitude"):
        st.markdown(
            """
        Research suggests that regular gratitude practice can:
        - Increase happiness and life satisfaction  
        - Reduce symptoms of depression and anxiety  
        - Improve sleep quality  
        - Strengthen relationships  
        - Support physical health and immunity  
        """
        )

    with st.expander("🔬 The Power of Affirmations & Thought Work"):
        st.markdown(
            """
        Self-affirmations and CBT-style thought records can:
        - Help you notice unhelpful thinking patterns  
        - Reduce the intensity of difficult emotions  
        - Support more balanced, flexible thinking  
        - Strengthen a kinder inner voice toward yourself  

        These are **self-help tools**, not a substitute for therapy or medical care.
        """
        )

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
                options=MOOD_OPTIONS,
                value="😊",
                help="From left (low) to right (great) 😊",
            )

        # Gentle journal prompts based on date
        prompts = get_prompts_for_date(entry_date)
        with st.expander("💡 Need ideas? Try one of these prompts"):
            for p in prompts:
                st.markdown(f"- {p}")

        st.markdown("#### What are you grateful for today?")
        gratitude_1 = st.text_area(
            "First thing I'm grateful for:",
            placeholder="Example: I'm grateful for my supportive friend who listened to me today...",
            height=80,
        )

        gratitude_2 = st.text_area(
            "Second thing I'm grateful for:",
            placeholder="Example: I'm grateful for the beautiful sunrise I witnessed this morning...",
            height=80,
        )

        gratitude_3 = st.text_area(
            "Third thing I'm grateful for:",
            placeholder="Example: I'm grateful for my health and the energy I had today...",
            height=80,
        )

        st.markdown("#### 🧭 Daily Intention (optional)")
        intention = st.text_input(
            "Today, I want to...",
            placeholder="Example: be kinder to myself, focus on one thing at a time, etc.",
        )

        tags = st.multiselect(
            "Tag this entry (optional)",
            JOURNAL_TAGS,
            help="Helps you see patterns later (e.g., work vs health).",
        )

        reflection = st.text_area(
            "Additional reflections (optional)",
            placeholder="How did focusing on gratitude make you feel?",
            height=80,
        )

        if st.button("💾 Save Journal Entry"):
            if gratitude_1 or gratitude_2 or gratitude_3:
                new_entry = {
                    "date": entry_date.strftime("%Y-%m-%d"),
                    "mood": mood,
                    "gratitudes": [g for g in [gratitude_1, gratitude_2, gratitude_3] if g],
                    "reflection": reflection,
                    "intention": intention,
                    "tags": tags,
                    "favorite": False,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
            all_dates = sorted({e["date"] for e in st.session_state.journal_entries})
            min_date = datetime.strptime(all_dates[0], "%Y-%m-%d").date()
            max_date = datetime.strptime(all_dates[-1], "%Y-%m-%d").date()

            col_f1, col_f2 = st.columns(2)
            with col_f1:
                date_range = st.date_input(
                    "Filter by date range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                )
            with col_f2:
                mood_filter = st.multiselect(
                    "Filter by mood",
                    options=MOOD_OPTIONS,
                    default=MOOD_OPTIONS,
                )

            search_query = st.text_input(
                "Search text (gratitudes, reflections, intentions):",
                placeholder="Type a word or phrase to search...",
            )
            show_favorites_only = st.checkbox("Show only favourites ⭐")

            start_d, end_d = date_range
            start_str = start_d.strftime("%Y-%m-%d")
            end_str = end_d.strftime("%Y-%m-%d")

            filtered = [
                e
                for e in st.session_state.journal_entries
                if start_str <= e["date"] <= end_str
                and e.get("mood", "😐") in mood_filter
            ]

            if search_query.strip():
                q = search_query.strip().lower()
                new_filtered = []
                for e in filtered:
                    text_blob = " ".join(e.get("gratitudes", []))
                    text_blob += " " + e.get("reflection", "")
                    text_blob += " " + e.get("intention", "")
                    if q in text_blob.lower():
                        new_filtered.append(e)
                filtered = new_filtered

            if show_favorites_only:
                filtered = [e for e in filtered if e.get("favorite", False)]

            sorted_entries = sorted(
                filtered,
                key=lambda x: (x["date"], x.get("timestamp", "")),
                reverse=True,
            )

            if not sorted_entries:
                st.info(
                    "No entries match your filters yet. Try widening the range or clearing search."
                )
            else:
                for i, entry in enumerate(sorted_entries):
                    is_fav = entry.get("favorite", False)
                    entry_key = entry.get("timestamp", f"{entry['date']}_{i}")

                    st.markdown(
                        f"""
                        <div class="gratitude-card">
                            <h4>{entry.get('mood', '🙂')} {entry['date']}</h4>
                        """,
                        unsafe_allow_html=True,
                    )

                    if entry.get("intention"):
                        st.markdown(f"**Intention:** {entry['intention']}")

                    if entry.get("tags"):
                        tags_str = ", ".join(entry["tags"])
                        st.markdown(f"**Tags:** {tags_str}")

                    for j, gratitude in enumerate(entry["gratitudes"], 1):
                        st.markdown(f"**{j}.** {gratitude}")

                    if entry.get("reflection"):
                        st.markdown(f"*Reflection: {entry['reflection']}*")

                    col_b1, col_b2, col_b3 = st.columns(3)
                    with col_b1:
                        fav_label = "★ Unfavourite" if is_fav else "⭐ Mark as favourite"
                        if st.button(fav_label, key=f"fav_{entry_key}"):
                            entry["favorite"] = not is_fav
                            save_data()
                            st.experimental_rerun()

                    with col_b2:
                        if st.button("✏️ Edit", key=f"edit_{entry_key}"):
                            st.session_state[f"edit_mode_{entry_key}"] = not st.session_state.get(
                                f"edit_mode_{entry_key}", False
                            )

                    with col_b3:
                        if st.button("🗑️ Delete", key=f"delete_{entry_key}"):
                            st.session_state.journal_entries.remove(entry)
                            save_data()
                            st.warning("Entry deleted.")
                            st.experimental_rerun()

                    # Inline editor for this entry
                    if st.session_state.get(f"edit_mode_{entry_key}", False):
                        with st.expander("Edit this entry", expanded=True):
                            edit_date = st.date_input(
                                "Date",
                                datetime.strptime(entry["date"], "%Y-%m-%d").date(),
                                key=f"edit_date_{entry_key}",
                            )
                            edit_mood = st.select_slider(
                                "Mood",
                                options=MOOD_OPTIONS,
                                value=entry.get("mood", "🙂"),
                                key=f"edit_mood_{entry_key}",
                            )

                            existing_grats = entry.get("gratitudes", [])
                            edit_g1 = st.text_area(
                                "First thing I'm grateful for:",
                                value=existing_grats[0] if len(existing_grats) > 0 else "",
                                height=80,
                                key=f"edit_g1_{entry_key}",
                            )
                            edit_g2 = st.text_area(
                                "Second thing I'm grateful for:",
                                value=existing_grats[1] if len(existing_grats) > 1 else "",
                                height=80,
                                key=f"edit_g2_{entry_key}",
                            )
                            edit_g3 = st.text_area(
                                "Third thing I'm grateful for:",
                                value=existing_grats[2] if len(existing_grats) > 2 else "",
                                height=80,
                                key=f"edit_g3_{entry_key}",
                            )

                            edit_intention = st.text_input(
                                "Daily intention (optional)",
                                value=entry.get("intention", ""),
                                key=f"edit_intention_{entry_key}",
                            )
                            edit_tags = st.multiselect(
                                "Tags",
                                JOURNAL_TAGS,
                                default=entry.get("tags", []),
                                key=f"edit_tags_{entry_key}",
                            )
                            edit_reflection = st.text_area(
                                "Reflection (optional)",
                                value=entry.get("reflection", ""),
                                height=80,
                                key=f"edit_reflection_{entry_key}",
                            )

                            if st.button("💾 Save changes", key=f"save_edit_{entry_key}"):
                                entry["date"] = edit_date.strftime("%Y-%m-%d")
                                entry["mood"] = edit_mood
                                entry["gratitudes"] = [
                                    g.strip() for g in [edit_g1, edit_g2, edit_g3] if g.strip()
                                ]
                                entry["intention"] = edit_intention
                                entry["tags"] = edit_tags
                                entry["reflection"] = edit_reflection
                                save_data()
                                st.session_state[f"edit_mode_{entry_key}"] = False
                                st.success("Entry updated.")
                                st.experimental_rerun()

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
            height=150,
        )

        with st.expander("➕ Add a custom category"):
            new_cat = st.text_input(
                "New category name:",
                key="new_jar_category",
                placeholder="e.g. Career wins, Pets, Travel",
            )
            if st.button("Add Category", key="add_jar_category"):
                if new_cat.strip():
                    if (
                        new_cat not in st.session_state.custom_jar_categories
                        and new_cat not in GRATITUDE_CATEGORIES
                    ):
                        st.session_state.custom_jar_categories.append(new_cat.strip())
                        save_data()
                        st.success("✅ Category added!")
                    else:
                        st.info("That category already exists.")

        category = st.selectbox(
            "Category (optional)",
            get_all_jar_categories(),
        )

        if st.button("🎊 Add to Jar"):
            if jar_note.strip():
                new_note = {
                    "note": jar_note.strip(),
                    "category": category,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
            random_note = random.choice(st.session_state.gratitude_jar)
            st.markdown(
                f"""
                <div class="affirmation-card">
                    {random_note['category']}<br><br>
                    "{random_note['note']}"<br><br>
                    <small>- {random_note['date']}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif not st.session_state.gratitude_jar:
            st.info("Your jar is empty. Add some notes first!")

    st.markdown("---")
    st.markdown("### 🏺 Your Gratitude Collection")

    if st.session_state.gratitude_jar:
        categories = ["All"] + sorted(
            {note["category"] for note in st.session_state.gratitude_jar}
        )
        selected_category = st.selectbox("Filter by category:", categories)

        filtered_notes = (
            st.session_state.gratitude_jar
            if selected_category == "All"
            else [
                note
                for note in st.session_state.gratitude_jar
                if note["category"] == selected_category
            ]
        )

        sorted_notes = sorted(filtered_notes, key=lambda x: x["timestamp"], reverse=True)

        for i, note in enumerate(sorted_notes):
            note_key = note.get("timestamp", f"{note['date']}_{i}")
            st.markdown(
                f"""
                <div class="jar-item">
                    <strong>{note['category']}</strong> - {note['date']}<br>
                    {note['note']}
                </div>
                """,
                unsafe_allow_html=True,
            )
            cols_note = st.columns([0.8, 0.2])
            with cols_note[1]:
                if st.button("🗑️ Delete", key=f"delete_jar_{note_key}"):
                    st.session_state.gratitude_jar.remove(note)
                    save_data()
                    st.warning("Note removed from jar.")
                    st.experimental_rerun()
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
            if (
                st.button("🔄 Get New Affirmation", use_container_width=True)
                or st.session_state.current_affirmation is None
            ):
                st.session_state.current_affirmation = random.choice(
                    st.session_state.affirmations
                )

            st.markdown(
                f"""
                <div class="affirmation-card">
                    "{st.session_state.current_affirmation}"
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown("### 💡 How to Use")
            st.markdown(
                """
            1. Read the affirmation slowly  
            2. Take a deep breath  
            3. Repeat it 3 times  
            4. Notice how it feels in your body  
            5. Let it gently shape your next action  
            """
            )

        st.markdown("---")
        st.markdown("### ✍️ Create Your Own Affirmation")

        custom_affirmation = st.text_input(
            "Write a personal affirmation:",
            placeholder="I am...",
        )

        if st.button("➕ Add My Affirmation"):
            if custom_affirmation and custom_affirmation not in st.session_state.affirmations:
                st.session_state.affirmations.append(custom_affirmation)
                save_data()
                st.success("✅ Your personal affirmation has been added!")
            elif custom_affirmation in st.session_state.affirmations:
                st.info("This affirmation already exists!")
            else:
                st.warning("Please write an affirmation first!")

    with tab2:
        st.markdown("### 📚 Complete Affirmation Library")

        mode = st.radio(
            "Show:",
            ["All affirmations", "Only my custom ones"],
            horizontal=True,
        )

        base_list = st.session_state.affirmations
        if mode == "Only my custom ones":
            base_list = [
                a for a in st.session_state.affirmations if a not in DEFAULT_AFFIRMATIONS
            ]

        if not base_list:
            st.info("No custom affirmations yet. Add one in the previous tab!")
        else:
            col_count = 2
            cols = st.columns(col_count)

            for idx, affirmation in enumerate(base_list):
                with cols[idx % col_count]:
                    st.markdown(
                        f"""
                        <div class="gratitude-card">
                            💫 {affirmation}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

# MY PROGRESS PAGE
elif page == "📊 My Progress":
    st.title("📊 My Progress")
    st.markdown("*Track your wellness journey*")

    if (
        st.session_state.journal_entries
        or st.session_state.gratitude_jar
        or st.session_state.thought_records
    ):
        unique_days = get_unique_practice_days()
        avg_mood, mood_face = get_average_mood()
        longest_streak = get_longest_streak()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Journal Entries",
                len(st.session_state.journal_entries),
                delta="Keep it up!"
                if len(st.session_state.journal_entries) > 0
                else None,
            )

        with col2:
            st.metric("Gratitude Notes", len(st.session_state.gratitude_jar))

        with col3:
            st.metric("Days Practiced", unique_days)

        with col4:
            st.metric(
                "Average Mood",
                f"{avg_mood:.1f}/5" if avg_mood else "–",
                delta=mood_face,
            )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Longest Streak", f"{longest_streak} days")
        with c2:
            streak_msg = (
                "🔥 Amazing consistency!"
                if longest_streak >= 14
                else "⭐ Great habit forming!"
                if longest_streak >= 7
                else "🌱 Every day counts"
                if longest_streak >= 1
                else "Start today 🌸"
            )
            st.info(streak_msg)
        with c3:
            st.metric("Thought Records Done", len(st.session_state.thought_records))

        # Mood tracking
        if st.session_state.journal_entries:
            st.markdown("### 😊 Mood Tracking")

            mood_counts = {}
            for entry in st.session_state.journal_entries:
                m = entry.get("mood", "😐")
                mood_counts[m] = mood_counts.get(m, 0) + 1

            colm1, colm2 = st.columns(2)

            with colm1:
                st.markdown("#### Mood Distribution")
                for mood, count in sorted(mood_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(st.session_state.journal_entries)) * 100
                    st.markdown(f"{mood}: {count} times ({percentage:.1f}%)")

                mood_df = pd.DataFrame(
                    {"Mood": list(mood_counts.keys()), "Count": list(mood_counts.values())}
                ).set_index("Mood")
                st.bar_chart(mood_df)

            with colm2:
                st.markdown("#### Entries Over Time")
                dates, counts = get_daily_entry_counts()
                if dates:
                    timeline_df = pd.DataFrame(
                        {"date": dates, "entries": counts}
                    ).set_index("date")
                    st.line_chart(timeline_df)
                else:
                    st.info("Add some journal entries to see your journey over time.")

            st.markdown("#### Recent Entries")
            recent = sorted(
                st.session_state.journal_entries,
                key=lambda x: (x["date"], x.get("timestamp", "")),
                reverse=True,
            )[:5]
            for entry in recent:
                mood = entry.get("mood", "🙂")
                tags_str = ", ".join(entry.get("tags", []))
                tags_display = f" — {tags_str}" if tags_str else ""
                st.markdown(f"- {mood} {entry['date']}{tags_display}")

        # Tag analytics
        all_tags = []
        for e in st.session_state.journal_entries:
            all_tags.extend(e.get("tags", []))
        if all_tags:
            st.markdown("---")
            st.markdown("### 🏷️ Themes You Write About Most")
            tag_counts = Counter(all_tags)
            tag_df = (
                pd.DataFrame(
                    {"Tag": list(tag_counts.keys()), "Entries": list(tag_counts.values())}
                )
                .sort_values("Entries", ascending=False)
                .set_index("Tag")
            )
            st.bar_chart(tag_df)

        # Gratitude jar analytics
        if st.session_state.gratitude_jar:
            st.markdown("---")
            st.markdown("### 🏺 Gratitude Jar Insights")
            cat_counts = Counter(note["category"] for note in st.session_state.gratitude_jar)
            cat_df = pd.DataFrame(
                {"Category": list(cat_counts.keys()), "Notes": list(cat_counts.values())}
            ).set_index("Category")
            st.bar_chart(cat_df)

        # Thought record insights
        if st.session_state.thought_records:
            st.markdown("---")
            st.markdown("### 🧠 Thought Work Insights")

            before_vals = [
                tr.get("intensity_before")
                for tr in st.session_state.thought_records
                if isinstance(tr.get("intensity_before"), (int, float))
            ]
            after_vals = [
                tr.get("intensity_after")
                for tr in st.session_state.thought_records
                if isinstance(tr.get("intensity_after"), (int, float))
            ]
            if before_vals and after_vals:
                avg_before = sum(before_vals) / len(before_vals)
                avg_after = sum(after_vals) / len(after_vals)
                st.markdown(
                    f"- Average emotion intensity **before** thought work: **{avg_before:.1f}/100**"
                )
                st.markdown(
                    f"- Average emotion intensity **after** thought work: **{avg_after:.1f}/100**"
                )
                diff = avg_before - avg_after
                st.markdown(
                    f"- Average change: **{diff:+.1f} points** "
                    "(positive means the emotion got a bit less intense on average)."
                )
                ta_df = pd.DataFrame(
                    {"Stage": ["Before", "After"], "Intensity": [avg_before, avg_after]}
                ).set_index("Stage")
                st.bar_chart(ta_df)

            trap_counts = Counter()
            for tr in st.session_state.thought_records:
                for trap in tr.get("thinking_traps", []):
                    trap_counts[trap] += 1
            if trap_counts:
                st.markdown("#### Thinking Patterns You’ve Logged")
                trap_df = (
                    pd.DataFrame(
                        {
                            "Thinking pattern": list(trap_counts.keys()),
                            "Count": list(trap_counts.values()),
                        }
                    )
                    .sort_values("Count", ascending=False)
                    .set_index("Thinking pattern")
                )
                st.bar_chart(trap_df)

        st.markdown("---")
        st.markdown("### 🎯 Your Achievements")

        achievements = []
        if len(st.session_state.journal_entries) >= 1:
            achievements.append("🌟 First Journal Entry")
        if longest_streak >= 3:
            achievements.append("🔥 3-Day Streak")
        if longest_streak >= 7:
            achievements.append("🏅 1-Week Streak")
        if len(st.session_state.journal_entries) >= 7:
            achievements.append("📚 Week of Gratitude")
        if len(st.session_state.journal_entries) >= 30:
            achievements.append("🏆 Month of Mindfulness")
        if len(st.session_state.gratitude_jar) >= 10:
            achievements.append("🏺 Jar Collector")
        if len(st.session_state.gratitude_jar) >= 50:
            achievements.append("💎 Gratitude Master")
        if len(st.session_state.thought_records) >= 5:
            achievements.append("🧠 Thought Explorer")
        if len(st.session_state.thought_records) >= 20:
            achievements.append("🔍 Cognitive Detective")

        if achievements:
            cols = st.columns(min(len(achievements), 4))
            for idx, achievement in enumerate(achievements):
                with cols[idx % 4]:
                    st.success(achievement)
        else:
            st.info("Keep practicing to unlock achievements!")

        st.markdown("---")
        with st.expander("⚙️ Export / Reset Data"):
            data = {
                "journal_entries": st.session_state.journal_entries,
                "gratitude_jar": st.session_state.gratitude_jar,
                "affirmations": st.session_state.affirmations,
                "thought_records": st.session_state.thought_records,
                "custom_jar_categories": st.session_state.custom_jar_categories,
            }
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            st.download_button(
                "⬇️ Download All Data (JSON)",
                data=json_str,
                file_name="mindfulme_backup.json",
                mime="application/json",
            )

            if st.session_state.journal_entries:
                journal_df = pd.json_normalize(st.session_state.journal_entries)
                st.download_button(
                    "⬇️ Download Journal as CSV",
                    data=journal_df.to_csv(index=False),
                    file_name="mindfulme_journal.csv",
                    mime="text/csv",
                )
            if st.session_state.gratitude_jar:
                jar_df = pd.json_normalize(st.session_state.gratitude_jar)
                st.download_button(
                    "⬇️ Download Gratitude Jar as CSV",
                    data=jar_df.to_csv(index=False),
                    file_name="mindfulme_gratitude_jar.csv",
                    mime="text/csv",
                )
            if st.session_state.thought_records:
                tr_df = pd.json_normalize(st.session_state.thought_records)
                st.download_button(
                    "⬇️ Download Thought Records as CSV",
                    data=tr_df.to_csv(index=False),
                    file_name="mindfulme_thought_records.csv",
                    mime="text/csv",
                )

            if st.button("🗑️ Clear All Data", type="secondary"):
                st.session_state.journal_entries = []
                st.session_state.gratitude_jar = []
                st.session_state.affirmations = DEFAULT_AFFIRMATIONS.copy()
                st.session_state.current_affirmation = None
                st.session_state.thought_records = []
                st.session_state.custom_jar_categories = []
                if DATA_FILE.exists():
                    try:
                        DATA_FILE.unlink()
                    except Exception:
                        pass
                st.success("All data cleared. Fresh start! 🌱")
    else:
        st.info("Start your wellness journey to see your progress here!")
        st.markdown(
            """
        ### 🚀 Getting Started
        - Write your first gratitude journal entry  
        - Add notes to your gratitude jar  
        - Try a psychology-based thought record  
        - Watch your progress grow!  
        """
        )

# PSYCHOLOGY TOOLS PAGE (CBT-INSPIRED)
elif page == "🧠 Psychology Tools":
    st.title("🧠 Psychology Tools (CBT-Inspired)")
    st.markdown(
        """
    These tools are inspired by **Cognitive Behavioural Therapy (CBT)** ideas like  
    *noticing thoughts, checking the evidence, and finding more balanced perspectives*.
    
    > ⚠️ This is **self-help only** and **not a substitute for therapy or crisis support**.  
    > If you feel at risk of harming yourself or others, or feel unable to cope,  
    > please contact local emergency services or a trusted crisis helpline.
    """
    )

    tab1, tab2 = st.tabs(["📝 Thought Record", "📚 Thinking Patterns"])

    with tab1:
        st.markdown("### 📝 Guided Thought Record")

        col1, col2 = st.columns([2, 1])
        with col1:
            tr_date = st.date_input("Date", datetime.now())
        with col2:
            emotion = st.text_input(
                "Main emotion (e.g., anxiety, guilt, sadness)",
                placeholder="e.g. Anxiety",
            )

        intensity_before = st.slider(
            "How strong is this emotion *right now*?",
            min_value=0,
            max_value=100,
            value=60,
            help="0 = none, 100 = as intense as you can imagine.",
        )

        situation = st.text_area(
            "1️⃣ Situation (what happened?)",
            placeholder="Where were you? Who was there? What triggered the feeling?",
            height=80,
        )

        automatic_thoughts = st.text_area(
            "2️⃣ Automatic thoughts (what went through your mind?)",
            placeholder="Write the exact sentences that popped into your mind.",
            height=100,
        )

        thinking_traps_selected = st.multiselect(
            "3️⃣ Do any of these thinking patterns fit?",
            options=list(THINKING_TRAPS.keys()),
            help="Many uncomfortable thoughts follow repeated patterns.",
        )

        if thinking_traps_selected:
            st.markdown("#### 🔍 Gentle questions for these patterns")
            for trap in thinking_traps_selected:
                info = THINKING_TRAPS.get(trap)
                if info:
                    st.markdown(f"**{trap}** – {info['description']}")
                    st.markdown(
                        "- What is one fact that doesn't fully match this thought?\n"
                        "- If a friend had this thought, what would I want them to remember?"
                    )

        col3, col4 = st.columns(2)
        with col3:
            evidence_for = st.text_area(
                "4️⃣ Evidence that supports the thought",
                placeholder="Facts (not feelings) that seem to support the thought.",
                height=100,
            )
        with col4:
            evidence_against = st.text_area(
                "5️⃣ Evidence against or missing from the thought",
                placeholder="Facts you’re ignoring that don’t fully fit the thought.",
                height=100,
            )

        balanced_response = st.text_area(
            "6️⃣ More balanced response",
            placeholder="If a kind, fair friend looked at all the evidence, what might they say?",
            height=100,
        )

        intensity_after = st.slider(
            "Now re-rate the emotion *after writing this* (optional)",
            min_value=0,
            max_value=100,
            value=40,
            help="It’s okay if it didn’t change much – practice is what matters.",
        )

        if st.button("💾 Save Thought Record"):
            if situation.strip() and automatic_thoughts.strip():
                new_record = {
                    "date": tr_date.strftime("%Y-%m-%d"),
                    "emotion": emotion,
                    "intensity_before": intensity_before,
                    "intensity_after": intensity_after,
                    "situation": situation,
                    "automatic_thoughts": automatic_thoughts,
                    "thinking_traps": thinking_traps_selected,
                    "evidence_for": evidence_for,
                    "evidence_against": evidence_against,
                    "balanced_response": balanced_response,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.session_state.thought_records.append(new_record)
                save_data()
                st.success("✅ Thought record saved. Nice work showing up for your mind.")
            else:
                st.warning("Please fill at least the situation and your automatic thoughts.")

        st.markdown("---")
        st.markdown("### 🕊️ Recent Thought Records")

        if st.session_state.thought_records:
            emotion_filter = st.multiselect(
                "Filter by emotion (optional)",
                options=sorted(
                    {
                        r.get("emotion")
                        for r in st.session_state.thought_records
                        if r.get("emotion")
                    }
                ),
                default=None,
            )

            recs = st.session_state.thought_records
            if emotion_filter:
                recs = [r for r in recs if r.get("emotion") in emotion_filter]

            recent_tr = sorted(
                recs,
                key=lambda r: (r["date"], r.get("timestamp", "")),
                reverse=True,
            )[:5]

            if not recent_tr:
                st.info("No thought records match that filter yet.")
            else:
                for rec in recent_tr:
                    traps_str = ", ".join(rec.get("thinking_traps", [])) or "–"
                    st.markdown(
                        f"""
                        <div class="gratitude-card">
                            <h4>{rec.get('emotion', 'Emotion') or 'Emotion'} — {rec['date']}</h4>
                            <p><strong>Situation:</strong> {rec['situation']}</p>
                            <p><strong>Automatic thoughts:</strong> {rec['automatic_thoughts']}</p>
                            <p><strong>Thinking patterns:</strong> {traps_str}</p>
                            <p><strong>Balanced response:</strong> {rec.get('balanced_response', '')}</p>
                            <p><em>Intensity:</em> {rec.get('intensity_before', 0)} → {rec.get('intensity_after', 0)}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.info("No thought records yet. You can start with even a very small situation.")

    with tab2:
        st.markdown("### 📚 Common Unhelpful Thinking Patterns")

        st.markdown(
            """
        These are **common patterns**, not “bad” thoughts.  
        The goal isn’t to *never* have them – just to notice them and gently question them.
        """
        )

        for name, info in THINKING_TRAPS.items():
            with st.expander(name):
                st.markdown(f"**What it is:** {info['description']}")
                st.markdown(f"**Example:** _{info['example']}_")
                st.markdown(
                    """
                **Helpful questions you might ask:**
                - What is the actual evidence *for* and *against* this thought?  
                - If a friend said this about themselves, what would I say to them?  
                - Is there a more flexible or balanced way of seeing this?  
                """
                )

# CALM CORNER PAGE
elif page == "🧘 Calm Corner":
    st.title("🧘 Calm Corner")
    st.markdown("*Quick tools to relax your body and calm your mind*")

    breath_tab, ground_tab, break_tab, compassion_tab = st.tabs(
        ["🌬️ Breathing Exercises", "🌍 Grounding Exercise", "⏲️ Micro Break", "💗 Self-Compassion"]
    )

    with breath_tab:
        st.markdown("### 🌬️ Box Breathing (4-4-4-4)")
        st.markdown(
            """
        Simple breathing can gently shift your nervous system from “fight/flight”  
        towards “rest and digest”. One simple pattern is **box breathing**:
        - Inhale for 4 seconds  
        - Hold for 4 seconds  
        - Exhale for 4 seconds  
        - Hold for 4 seconds  
        """
        )

        if st.button("▶️ Start 1-Minute Box Breathing"):
            import time

            placeholder = st.empty()
            cycles = 4
            for _ in range(cycles):
                for phase, seconds in [("Inhale", 4), ("Hold", 4), ("Exhale", 4), ("Hold", 4)]:
                    for s in range(seconds, 0, -1):
                        placeholder.markdown(
                            f"### **{phase}**\n\nRemaining: **{s}** seconds"
                        )
                        time.sleep(1)
            placeholder.markdown("### ✅ Done! Notice how your body feels now.")

        st.markdown("---")
        st.markdown("### 🌙 4-7-8 Breathing")
        st.markdown(
            """
        Another pattern some people find calming, especially at night:
        - Inhale quietly through the nose for 4 seconds  
        - Hold your breath for 7 seconds  
        - Exhale completely through the mouth for 8 seconds  
        Try 3–4 cycles. If it feels uncomfortable, shorten the counts.
        """
        )

    with ground_tab:
        st.markdown("### 5-4-3-2-1 Grounding")
        st.markdown(
            """
        Use this when you feel overwhelmed. Gently name:
        """
        )

        steps = [
            "5 things you can see",
            "4 things you can feel (touch)",
            "3 things you can hear",
            "2 things you can smell",
            "1 thing you can taste",
        ]

        for idx, prompt in enumerate(steps, start=1):
            st.markdown(f"**{prompt}:**")
            st.text_input("", key=f"grounding_{idx}", placeholder="Write it here (optional)")

        st.info(
            "You don't have to write anything — even just mentally naming them can help bring you back to the present."
        )

    with break_tab:
        st.markdown("### ⏲️ Micro Break Timer")
        st.markdown(
            """
        A tiny reset can help when your mind feels overloaded.  
        Choose a short break duration and let the timer run while you rest your eyes or stretch.
        """
        )
        minutes = st.slider(
            "Break length (minutes)",
            min_value=1,
            max_value=5,
            value=2,
        )

        if st.button("▶️ Start Break"):
            import time

            total_seconds = minutes * 60
            placeholder = st.empty()
            for remaining in range(total_seconds, -1, -1):
                mins = remaining // 60
                secs = remaining % 60
                placeholder.markdown(f"### ⏳ Time left: **{mins:02d}:{secs:02d}**")
                time.sleep(1)
            placeholder.markdown(
                "### ✅ Break complete. Check in: how do you feel right now?"
            )

    with compassion_tab:
        st.markdown("### 💗 Self-Compassion Break")
        st.markdown(
            """
        This exercise is about talking to yourself the way you might talk to a close friend.

        1. **Notice** – Name what feels difficult right now.  
        2. **Normalise** – Remember that many humans feel this way sometimes.  
        3. **Be kind** – Offer yourself one short, kind sentence.
        """
        )

        sc_situation = st.text_area(
            "What is difficult right now?",
            placeholder="Write a sentence or two about what feels hard (or leave blank and just read).",
            height=80,
        )
        sc_feeling = st.text_input(
            "Main feeling (e.g. shame, fear, sadness):",
            placeholder="e.g. Sadness",
        )
        sc_sentence = st.text_input(
            "One kind sentence to yourself:",
            placeholder="e.g. It's understandable I feel this way; I'm doing the best I can right now.",
        )

        if st.button("💾 Save this self-compassion note"):
            if sc_situation.strip() or sc_sentence.strip():
                # Store as a gentle variant of a thought record
                st.session_state.thought_records.append(
                    {
                        "date": get_today_string(),
                        "emotion": sc_feeling or "Self-compassion",
                        "intensity_before": None,
                        "intensity_after": None,
                        "situation": sc_situation,
                        "automatic_thoughts": "",
                        "thinking_traps": [],
                        "evidence_for": "",
                        "evidence_against": "",
                        "balanced_response": sc_sentence,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
                save_data()
                st.success(
                    "Saved. You can revisit this in your Thought Records or Progress."
                )
            else:
                st.info("You can also just read the prompts without saving anything.")

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #6b7280; padding: 2rem;'>
    <p>🌸 MindfulMe - Your Wellness Companion</p>
    <p><small>This app is for reflection and self-help only, not a substitute for professional diagnosis or treatment.</small></p>
</div>
""",
    unsafe_allow_html=True,
)
