import React, { useState, useEffect } from 'react';
import { Heart, Book, Smile, Wind, Sparkles, Calendar, TrendingUp, Plus, X, Check, Target, Coffee, Phone, AlertCircle, Clock, BarChart3, Lightbulb, Users, Sun } from 'lucide-react';

export default function MentalHealthApp() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [gratitudeEntries, setGratitudeEntries] = useState([]);
  const [moodEntries, setMoodEntries] = useState([]);
  const [journalEntries, setJournalEntries] = useState([]);
  const [goals, setGoals] = useState([]);
  const [habits, setHabits] = useState([
    { id: 1, name: 'Drink 8 glasses of water', completed: [], icon: '💧' },
    { id: 2, name: 'Exercise for 30 minutes', completed: [], icon: '🏃' },
    { id: 3, name: 'Meditate for 10 minutes', completed: [], icon: '🧘' },
    { id: 4, name: 'Get 8 hours of sleep', completed: [], icon: '😴' }
  ]);
  const [newGratitude, setNewGratitude] = useState('');
  const [selectedMood, setSelectedMood] = useState(null);
  const [moodNote, setMoodNote] = useState('');
  const [breathingActive, setBreathingActive] = useState(false);
  const [breathPhase, setBreathPhase] = useState('inhale');
  const [breathCount, setBreathCount] = useState(0);
  const [meditationTime, setMeditationTime] = useState(5);
  const [meditationActive, setMeditationActive] = useState(false);
  const [meditationSeconds, setMeditationSeconds] = useState(0);
  const [journalPromptIndex, setJournalPromptIndex] = useState(0);
  const [journalText, setJournalText] = useState('');
  const [newGoal, setNewGoal] = useState('');
  const [newHabit, setNewHabit] = useState('');

  const affirmations = [
    "I am worthy of love and respect",
    "I choose to focus on what I can control",
    "Every day is a fresh start",
    "I am stronger than my challenges",
    "I deserve peace and happiness",
    "My feelings are valid",
    "I am proud of how far I've come",
    "I am enough, just as I am",
    "I trust in my ability to overcome obstacles",
    "I am growing and learning every day",
    "My mental health is a priority",
    "I choose joy and positivity"
  ];

  const journalPrompts = [
    "What made me smile today?",
    "What challenge did I overcome recently?",
    "What am I looking forward to?",
    "Who am I grateful for and why?",
    "What's something I learned about myself today?",
    "What would I tell my younger self?",
    "What are three things I love about myself?",
    "What does self-care mean to me?",
    "What's a recent accomplishment I'm proud of?",
    "How can I be kinder to myself?",
    "What brings me peace?",
    "What boundaries do I need to set?"
  ];

  const selfCareActivities = [
    { activity: "Take a warm bath", icon: "🛁", category: "Physical" },
    { activity: "Call a friend", icon: "📞", category: "Social" },
    { activity: "Read a book", icon: "📚", category: "Mental" },
    { activity: "Go for a walk", icon: "🚶", category: "Physical" },
    { activity: "Listen to music", icon: "🎵", category: "Emotional" },
    { activity: "Practice yoga", icon: "🧘", category: "Physical" },
    { activity: "Cook a healthy meal", icon: "🥗", category: "Physical" },
    { activity: "Write in a journal", icon: "✍️", category: "Mental" },
    { activity: "Watch something funny", icon: "😂", category: "Emotional" },
    { activity: "Spend time in nature", icon: "🌳", category: "Physical" },
    { activity: "Do a creative activity", icon: "🎨", category: "Mental" },
    { activity: "Practice mindfulness", icon: "🌸", category: "Emotional" }
  ];

  const [currentAffirmation, setCurrentAffirmation] = useState(affirmations[0]);

  const moods = [
    { emoji: '😊', label: 'Great', color: 'bg-green-500' },
    { emoji: '🙂', label: 'Good', color: 'bg-blue-500' },
    { emoji: '😐', label: 'Okay', color: 'bg-yellow-500' },
    { emoji: '😔', label: 'Low', color: 'bg-orange-500' },
    { emoji: '😢', label: 'Difficult', color: 'bg-red-500' }
  ];

  useEffect(() => {
    if (breathingActive) {
      const phases = [
        { name: 'inhale', duration: 4000 },
        { name: 'hold', duration: 4000 },
        { name: 'exhale', duration: 4000 },
        { name: 'hold', duration: 4000 }
      ];
      
      let currentPhaseIndex = 0;
      
      const cycleBreath = () => {
        const phase = phases[currentPhaseIndex];
        setBreathPhase(phase.name);
        
        setTimeout(() => {
          currentPhaseIndex = (currentPhaseIndex + 1) % phases.length;
          if (currentPhaseIndex === 0) {
            setBreathCount(prev => prev + 1);
          }
          if (breathingActive) {
            cycleBreath();
          }
        }, phase.duration);
      };
      
      cycleBreath();
    }
  }, [breathingActive]);

  useEffect(() => {
    let interval;
    if (meditationActive && meditationSeconds < meditationTime * 60) {
      interval = setInterval(() => {
        setMeditationSeconds(prev => prev + 1);
      }, 1000);
    } else if (meditationSeconds >= meditationTime * 60) {
      setMeditationActive(false);
    }
    return () => clearInterval(interval);
  }, [meditationActive, meditationSeconds, meditationTime]);

  const addGratitude = () => {
    if (newGratitude.trim()) {
      setGratitudeEntries([
        { id: Date.now(), text: newGratitude, date: new Date().toLocaleDateString() },
        ...gratitudeEntries
      ]);
      setNewGratitude('');
    }
  };

  const addMood = () => {
    if (selectedMood !== null) {
      setMoodEntries([
        { 
          id: Date.now(), 
          mood: moods[selectedMood], 
          note: moodNote,
          date: new Date().toLocaleDateString(),
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
        ...moodEntries
      ]);
      setSelectedMood(null);
      setMoodNote('');
    }
  };

  const deleteGratitude = (id) => {
    setGratitudeEntries(gratitudeEntries.filter(entry => entry.id !== id));
  };

  const deleteMood = (id) => {
    setMoodEntries(moodEntries.filter(entry => entry.id !== id));
  };

  const randomAffirmation = () => {
    const randomIndex = Math.floor(Math.random() * affirmations.length);
    setCurrentAffirmation(affirmations[randomIndex]);
  };

  const startBreathing = () => {
    setBreathingActive(true);
    setBreathCount(0);
  };

  const stopBreathing = () => {
    setBreathingActive(false);
    setBreathPhase('inhale');
  };

  const addJournalEntry = () => {
    if (journalText.trim()) {
      setJournalEntries([
        {
          id: Date.now(),
          prompt: journalPrompts[journalPromptIndex],
          text: journalText,
          date: new Date().toLocaleDateString(),
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
        ...journalEntries
      ]);
      setJournalText('');
      nextPrompt();
    }
  };

  const deleteJournalEntry = (id) => {
    setJournalEntries(journalEntries.filter(entry => entry.id !== id));
  };

  const nextPrompt = () => {
    setJournalPromptIndex((journalPromptIndex + 1) % journalPrompts.length);
  };

  const addGoal = () => {
    if (newGoal.trim()) {
      setGoals([
        {
          id: Date.now(),
          text: newGoal,
          completed: false,
          date: new Date().toLocaleDateString()
        },
        ...goals
      ]);
      setNewGoal('');
    }
  };

  const toggleGoal = (id) => {
    setGoals(goals.map(goal => 
      goal.id === id ? { ...goal, completed: !goal.completed } : goal
    ));
  };

  const deleteGoal = (id) => {
    setGoals(goals.filter(goal => goal.id !== id));
  };

  const addCustomHabit = () => {
    if (newHabit.trim()) {
      setHabits([
        ...habits,
        {
          id: Date.now(),
          name: newHabit,
          completed: [],
          icon: '⭐'
        }
      ]);
      setNewHabit('');
    }
  };

  const toggleHabit = (habitId) => {
    const today = new Date().toLocaleDateString();
    setHabits(habits.map(habit => {
      if (habit.id === habitId) {
        const isCompleted = habit.completed.includes(today);
        return {
          ...habit,
          completed: isCompleted 
            ? habit.completed.filter(date => date !== today)
            : [...habit.completed, today]
        };
      }
      return habit;
    }));
  };

  const deleteHabit = (id) => {
    setHabits(habits.filter(habit => habit.id !== id));
  };

  const startMeditation = () => {
    setMeditationActive(true);
    setMeditationSeconds(0);
  };

  const stopMeditation = () => {
    setMeditationActive(false);
    setMeditationSeconds(0);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getMoodStats = () => {
    const last7Days = moodEntries.slice(0, 7);
    if (last7Days.length === 0) return null;
    
    const moodCounts = {};
    last7Days.forEach(entry => {
      const label = entry.mood.label;
      moodCounts[label] = (moodCounts[label] || 0) + 1;
    });
    
    const dominant = Object.entries(moodCounts).sort((a, b) => b[1] - a[1])[0];
    return { dominant: dominant[0], total: last7Days.length };
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-4 sm:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full mb-4">
            <Heart className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Mental Health Companion</h1>
          <p className="text-gray-600">Your daily wellness journey</p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex flex-wrap gap-2 mb-6 bg-white rounded-lg p-2 shadow-md">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'dashboard' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span className="text-sm font-medium">Dashboard</span>
          </button>
          <button
            onClick={() => setActiveTab('gratitude')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'gratitude' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Book className="w-4 h-4" />
            <span className="text-sm font-medium">Gratitude</span>
          </button>
          <button
            onClick={() => setActiveTab('mood')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'mood' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Smile className="w-4 h-4" />
            <span className="text-sm font-medium">Mood</span>
          </button>
          <button
            onClick={() => setActiveTab('journal')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'journal' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Lightbulb className="w-4 h-4" />
            <span className="text-sm font-medium">Journal</span>
          </button>
          <button
            onClick={() => setActiveTab('goals')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'goals' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Target className="w-4 h-4" />
            <span className="text-sm font-medium">Goals</span>
          </button>
          <button
            onClick={() => setActiveTab('habits')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'habits' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Check className="w-4 h-4" />
            <span className="text-sm font-medium">Habits</span>
          </button>
          <button
            onClick={() => setActiveTab('breathing')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'breathing' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Wind className="w-4 h-4" />
            <span className="text-sm font-medium">Breathing</span>
          </button>
          <button
            onClick={() => setActiveTab('meditation')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'meditation' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Clock className="w-4 h-4" />
            <span className="text-sm font-medium">Meditation</span>
          </button>
          <button
            onClick={() => setActiveTab('affirmations')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'affirmations' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span className="text-sm font-medium">Affirmations</span>
          </button>
          <button
            onClick={() => setActiveTab('selfcare')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'selfcare' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Sun className="w-4 h-4" />
            <span className="text-sm font-medium">Self-Care</span>
          </button>
          <button
            onClick={() => setActiveTab('resources')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${
              activeTab === 'resources' ? 'bg-purple-500 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Phone className="w-4 h-4" />
            <span className="text-sm font-medium">Resources</span>
          </button>
        </div>

        {/* Content Area */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          {/* Dashboard */}
          {activeTab === 'dashboard' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Your Wellness Dashboard</h2>
              <p className="text-gray-600 mb-6">Track your mental health journey</p>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                {/* Stats Cards */}
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg">
                  <div className="flex items-center gap-3 mb-2">
                    <Book className="w-6 h-6 text-purple-600" />
                    <h3 className="font-semibold text-gray-800">Gratitude Entries</h3>
                  </div>
                  <p className="text-3xl font-bold text-purple-600">{gratitudeEntries.length}</p>
                  <p className="text-sm text-gray-600 mt-1">Total entries logged</p>
                </div>

                <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg">
                  <div className="flex items-center gap-3 mb-2">
                    <Smile className="w-6 h-6 text-blue-600" />
                    <h3 className="font-semibold text-gray-800">Mood Logs</h3>
                  </div>
                  <p className="text-3xl font-bold text-blue-600">{moodEntries.length}</p>
                  <p className="text-sm text-gray-600 mt-1">
                    {getMoodStats() ? `Most common: ${getMoodStats().dominant}` : 'Start tracking!'}
                  </p>
                </div>

                <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg">
                  <div className="flex items-center gap-3 mb-2">
                    <Target className="w-6 h-6 text-green-600" />
                    <h3 className="font-semibold text-gray-800">Goals</h3>
                  </div>
                  <p className="text-3xl font-bold text-green-600">
                    {goals.filter(g => g.completed).length}/{goals.length}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">Completed goals</p>
                </div>

                <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-4 rounded-lg">
                  <div className="flex items-center gap-3 mb-2">
                    <Check className="w-6 h-6 text-yellow-600" />
                    <h3 className="font-semibold text-gray-800">Habits Today</h3>
                  </div>
                  <p className="text-3xl font-bold text-yellow-600">
                    {habits.filter(h => h.completed.includes(new Date().toLocaleDateString())).length}/{habits.length}
                  </p>
                  <p className="text-sm text-gray-600 mt-1">Completed today</p>
                </div>

                <div className="bg-gradient-to-br from-pink-50 to-pink-100 p-4 rounded-lg">
                  <div className="flex items-center gap-3 mb-2">
                    <Lightbulb className="w-6 h-6 text-pink-600" />
                    <h3 className="font-semibold text-gray-800">Journal Entries</h3>
                  </div>
                  <p className="text-3xl font-bold text-pink-600">{journalEntries.length}</p>
                  <p className="text-sm text-gray-600 mt-1">Reflections written</p>
                </div>

                <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 p-4 rounded-lg">
                  <div className="flex items-center gap-3 mb-2">
                    <Sparkles className="w-6 h-6 text-indigo-600" />
                    <h3 className="font-semibold text-gray-800">Daily Affirmation</h3>
                  </div>
                  <p className="text-sm text-gray-700 mt-2 italic">"{currentAffirmation}"</p>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="mt-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Quick Actions</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <button
                    onClick={() => setActiveTab('mood')}
                    className="flex flex-col items-center gap-2 p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
                  >
                    <Smile className="w-6 h-6 text-blue-600" />
                    <span className="text-sm font-medium text-gray-700">Log Mood</span>
                  </button>
                  <button
                    onClick={() => setActiveTab('breathing')}
                    className="flex flex-col items-center gap-2 p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors"
                  >
                    <Wind className="w-6 h-6 text-purple-600" />
                    <span className="text-sm font-medium text-gray-700">Breathe</span>
                  </button>
                  <button
                    onClick={() => setActiveTab('meditation')}
                    className="flex flex-col items-center gap-2 p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
                  >
                    <Clock className="w-6 h-6 text-green-600" />
                    <span className="text-sm font-medium text-gray-700">Meditate</span>
                  </button>
                  <button
                    onClick={() => setActiveTab('affirmations')}
                    className="flex flex-col items-center gap-2 p-4 bg-yellow-50 hover:bg-yellow-100 rounded-lg transition-colors"
                  >
                    <Sparkles className="w-6 h-6 text-yellow-600" />
                    <span className="text-sm font-medium text-gray-700">Affirm</span>
                  </button>
                </div>
              </div>

              {/* Recent Activity */}
              {(moodEntries.length > 0 || gratitudeEntries.length > 0) && (
                <div className="mt-6">
                  <h3 className="text-lg font-semibold text-gray-800 mb-3">Recent Activity</h3>
                  <div className="space-y-2">
                    {moodEntries.slice(0, 3).map(entry => (
                      <div key={entry.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <span className="text-2xl">{entry.mood.emoji}</span>
                        <div className="flex-1">
                          <p className="text-sm font-medium text-gray-800">Mood: {entry.mood.label}</p>
                          <p className="text-xs text-gray-500">{entry.date} at {entry.time}</p>
                        </div>
                      </div>
                    ))}
                    {gratitudeEntries.slice(0, 2).map(entry => (
                      <div key={entry.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <Heart className="w-5 h-5 text-purple-500" />
                        <div className="flex-1">
                          <p className="text-sm text-gray-800">{entry.text.substring(0, 50)}...</p>
                          <p className="text-xs text-gray-500">{entry.date}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Gratitude Journal */}
          {activeTab === 'gratitude' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Gratitude Journal</h2>
              <p className="text-gray-600 mb-6">What are you grateful for today?</p>
              
              <div className="mb-6">
                <textarea
                  value={newGratitude}
                  onChange={(e) => setNewGratitude(e.target.value)}
                  placeholder="I'm grateful for..."
                  className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none resize-none"
                  rows="3"
                />
                <button
                  onClick={addGratitude}
                  className="mt-3 flex items-center gap-2 bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  Add Entry
                </button>
              </div>

              <div className="space-y-3">
                {gratitudeEntries.length === 0 ? (
                  <p className="text-gray-400 text-center py-8">No entries yet. Start your gratitude journey!</p>
                ) : (
                  gratitudeEntries.map(entry => (
                    <div key={entry.id} className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg flex justify-between items-start">
                      <div className="flex-1">
                        <p className="text-gray-800">{entry.text}</p>
                        <p className="text-sm text-gray-500 mt-1">{entry.date}</p>
                      </div>
                      <button
                        onClick={() => deleteGratitude(entry.id)}
                        className="text-gray-400 hover:text-red-500 ml-4"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* Mood Tracker */}
          {activeTab === 'mood' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Mood Tracker</h2>
              <p className="text-gray-600 mb-6">How are you feeling right now?</p>
              
              <div className="mb-6">
                <div className="flex flex-wrap gap-3 mb-4">
                  {moods.map((mood, index) => (
                    <button
                      key={index}
                      onClick={() => setSelectedMood(index)}
                      className={`flex flex-col items-center p-4 rounded-lg border-2 transition-all ${
                        selectedMood === index 
                          ? 'border-purple-500 bg-purple-50' 
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <span className="text-4xl mb-2">{mood.emoji}</span>
                      <span className="text-sm font-medium text-gray-700">{mood.label}</span>
                    </button>
                  ))}
                </div>

                {selectedMood !== null && (
                  <div>
                    <textarea
                      value={moodNote}
                      onChange={(e) => setMoodNote(e.target.value)}
                      placeholder="Add a note about your mood (optional)..."
                      className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none resize-none mb-3"
                      rows="2"
                    />
                    <button
                      onClick={addMood}
                      className="flex items-center gap-2 bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition-colors"
                    >
                      <Check className="w-4 h-4" />
                      Log Mood
                    </button>
                  </div>
                )}
              </div>

              <div className="space-y-3">
                {moodEntries.length === 0 ? (
                  <p className="text-gray-400 text-center py-8">No mood entries yet. Track your first mood!</p>
                ) : (
                  moodEntries.map(entry => (
                    <div key={entry.id} className={`${entry.mood.color} bg-opacity-10 p-4 rounded-lg flex justify-between items-start`}>
                      <div className="flex items-start gap-3 flex-1">
                        <span className="text-3xl">{entry.mood.emoji}</span>
                        <div>
                          <p className="font-medium text-gray-800">{entry.mood.label}</p>
                          {entry.note && <p className="text-gray-700 mt-1">{entry.note}</p>}
                          <p className="text-sm text-gray-500 mt-1">{entry.date} at {entry.time}</p>
                        </div>
                      </div>
                      <button
                        onClick={() => deleteMood(entry.id)}
                        className="text-gray-400 hover:text-red-500 ml-4"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* Journal with Prompts */}
          {activeTab === 'journal' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Reflective Journal</h2>
              <p className="text-gray-600 mb-6">Explore your thoughts with guided prompts</p>
              
              <div className="mb-6">
                <div className="bg-gradient-to-r from-pink-50 to-purple-50 p-6 rounded-lg mb-4">
                  <div className="flex items-start gap-3 mb-4">
                    <Lightbulb className="w-6 h-6 text-purple-600 mt-1" />
                    <div>
                      <h3 className="font-semibold text-gray-800 mb-2">Today's Prompt</h3>
                      <p className="text-lg text-gray-700">{journalPrompts[journalPromptIndex]}</p>
                    </div>
                  </div>
                  <button
                    onClick={nextPrompt}
                    className="text-sm text-purple-600 hover:text-purple-700 font-medium"
                  >
                    Get different prompt →
                  </button>
                </div>
                
                <textarea
                  value={journalText}
                  onChange={(e) => setJournalText(e.target.value)}
                  placeholder="Write your thoughts here..."
                  className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none resize-none"
                  rows="6"
                />
                <button
                  onClick={addJournalEntry}
                  className="mt-3 flex items-center gap-2 bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  Save Entry
                </button>
              </div>

              <div className="space-y-3">
                {journalEntries.length === 0 ? (
                  <p className="text-gray-400 text-center py-8">No journal entries yet. Start reflecting!</p>
                ) : (
                  journalEntries.map(entry => (
                    <div key={entry.id} className="bg-gradient-to-r from-pink-50 to-purple-50 p-4 rounded-lg">
                      <div className="flex justify-between items-start mb-2">
                        <p className="font-semibold text-purple-700 text-sm">{entry.prompt}</p>
                        <button
                          onClick={() => deleteJournalEntry(entry.id)}
                          className="text-gray-400 hover:text-red-500"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                      <p className="text-gray-800 mb-2">{entry.text}</p>
                      <p className="text-sm text-gray-500">{entry.date} at {entry.time}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* Goals */}
          {activeTab === 'goals' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Personal Goals</h2>
              <p className="text-gray-600 mb-6">Set and track your mental health goals</p>
              
              <div className="mb-6">
                <input
                  type="text"
                  value={newGoal}
                  onChange={(e) => setNewGoal(e.target.value)}
                  placeholder="Enter a new goal..."
                  className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none mb-3"
                />
                <button
                  onClick={addGoal}
                  className="flex items-center gap-2 bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  Add Goal
                </button>
              </div>

              <div className="space-y-3">
                {goals.length === 0 ? (
                  <p className="text-gray-400 text-center py-8">No goals yet. Set your first goal!</p>
                ) : (
                  goals.map(goal => (
                    <div key={goal.id} className={`p-4 rounded-lg flex items-center gap-3 ${
                      goal.completed ? 'bg-green-50' : 'bg-gray-50'
                    }`}>
                      <button
                        onClick={() => toggleGoal(goal.id)}
                        className={`flex-shrink-0 w-6 h-6 rounded border-2 flex items-center justify-center transition-colors ${
                          goal.completed 
                            ? 'bg-green-500 border-green-500' 
                            : 'border-gray-300 hover:border-green-500'
                        }`}
                      >
                        {goal.completed && <Check className="w-4 h-4 text-white" />}
                      </button>
                      <div className="flex-1">
                        <p className={`${goal.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                          {goal.text}
                        </p>
                        <p className="text-sm text-gray-500">{goal.date}</p>
                      </div>
                      <button
                        onClick={() => deleteGoal(goal.id)}
                        className="text-gray-400 hover:text-red-500"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* Habits */}
          {activeTab === 'habits' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Daily Habits</h2>
              <p className="text-gray-600 mb-6">Build healthy habits one day at a time</p>
              
              <div className="mb-6">
                <input
                  type="text"
                  value={newHabit}
                  onChange={(e) => setNewHabit(e.target.value)}
                  placeholder="Add a new habit to track..."
                  className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none mb-3"
                />
                <button
                  onClick={addCustomHabit}
                  className="flex items-center gap-2 bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  Add Habit
                </button>
              </div>

              <div className="space-y-3">
                {habits.map(habit => {
                  const completedToday = habit.completed.includes(new Date().toLocaleDateString());
                  return (
                    <div key={habit.id} className={`p-4 rounded-lg flex items-center gap-3 ${
                      completedToday ? 'bg-green-50' : 'bg-gray-50'
                    }`}>
                      <button
                        onClick={() => toggleHabit(habit.id)}
                        className={`flex-shrink-0 w-10 h-10 rounded-full border-2 flex items-center justify-center transition-colors ${
                          completedToday 
                            ? 'bg-green-500 border-green-500' 
                            : 'border-gray-300 hover:border-green-500'
                        }`}
                      >
                        {completedToday ? <Check className="w-5 h-5 text-white" /> : <span className="text-xl">{habit.icon}</span>}
                      </button>
                      <div className="flex-1">
                        <p className="text-gray-800 font-medium">{habit.name}</p>
                        <p className="text-sm text-gray-500">
                          {habit.completed.length} {habit.completed.length === 1 ? 'day' : 'days'} completed
                        </p>
                      </div>
                      {habit.id > 4 && (
                        <button
                          onClick={() => deleteHabit(habit.id)}
                          className="text-gray-400 hover:text-red-500"
                        >
                          <X className="w-5 h-5" />
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Breathing Exercise */}
          {activeTab === 'breathing' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Box Breathing</h2>
              <p className="text-gray-600 mb-6">Find your calm with guided breathing</p>
              
              <div className="flex flex-col items-center">
                <div className={`relative w-64 h-64 mb-8 transition-all duration-1000 ${
                  breathingActive ? 'scale-100' : 'scale-95'
                }`}>
                  <div className={`absolute inset-0 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 transition-all duration-4000 ${
                    breathPhase === 'inhale' || breathPhase === 'hold' ? 'scale-100 opacity-100' : 'scale-75 opacity-60'
                  }`}></div>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center text-white">
                      <p className="text-2xl font-bold capitalize mb-2">{breathPhase}</p>
                      {breathingActive && <p className="text-lg">Cycle {breathCount + 1}</p>}
                    </div>
                  </div>
                </div>

                {!breathingActive ? (
                  <button
                    onClick={startBreathing}
                    className="flex items-center gap-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white px-8 py-3 rounded-lg hover:from-blue-600 hover:to-purple-600 transition-all text-lg font-medium"
                  >
                    <Wind className="w-5 h-5" />
                    Start Breathing
                  </button>
                ) : (
                  <button
                    onClick={stopBreathing}
                    className="flex items-center gap-2 bg-gray-500 text-white px-8 py-3 rounded-lg hover:bg-gray-600 transition-all text-lg font-medium"
                  >
                    Stop
                  </button>
                )}

                <div className="mt-8 text-center text-gray-600">
                  <p className="mb-2">Follow the breathing pattern:</p>
                  <ul className="space-y-1">
                    <li>Inhale for 4 seconds</li>
                    <li>Hold for 4 seconds</li>
                    <li>Exhale for 4 seconds</li>
                    <li>Hold for 4 seconds</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Affirmations */}
          {activeTab === 'affirmations' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Daily Affirmations</h2>
              <p className="text-gray-600 mb-6">Positive thoughts for a positive day</p>
              
              <div className="flex flex-col items-center">
                <div className="bg-gradient-to-br from-yellow-50 to-orange-50 border-2 border-yellow-200 rounded-xl p-8 mb-6 text-center max-w-xl">
                  <Sparkles className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
                  <p className="text-2xl font-medium text-gray-800 leading-relaxed">{currentAffirmation}</p>
                </div>

                <button
                  onClick={randomAffirmation}
                  className="flex items-center gap-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-white px-6 py-3 rounded-lg hover:from-yellow-600 hover:to-orange-600 transition-all font-medium"
                >
                  <Sparkles className="w-5 h-5" />
                  New Affirmation
                </button>

                <div className="mt-10 w-full max-w-xl">
                  <h3 className="text-lg font-semibold text-gray-700 mb-4">All Affirmations</h3>
                  <div className="space-y-2">
                    {affirmations.map((affirmation, index) => (
                      <div key={index} className="bg-gray-50 p-3 rounded-lg text-gray-700">
                        {affirmation}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Meditation Timer */}
          {activeTab === 'meditation' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Meditation Timer</h2>
              <p className="text-gray-600 mb-6">Take time for mindful meditation</p>
              
              <div className="flex flex-col items-center">
                {!meditationActive ? (
                  <>
                    <div className="mb-8 text-center">
                      <p className="text-gray-700 mb-4">Choose meditation duration:</p>
                      <div className="flex gap-3 justify-center">
                        {[5, 10, 15, 20].map(mins => (
                          <button
                            key={mins}
                            onClick={() => setMeditationTime(mins)}
                            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                              meditationTime === mins
                                ? 'bg-purple-500 text-white'
                                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            }`}
                          >
                            {mins} min
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="w-64 h-64 mb-8 rounded-full bg-gradient-to-br from-purple-200 to-blue-200 flex items-center justify-center">
                      <div className="text-center">
                        <Clock className="w-16 h-16 text-purple-600 mx-auto mb-2" />
                        <p className="text-4xl font-bold text-gray-800">{meditationTime}:00</p>
                      </div>
                    </div>

                    <button
                      onClick={startMeditation}
                      className="flex items-center gap-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white px-8 py-3 rounded-lg hover:from-purple-600 hover:to-blue-600 transition-all text-lg font-medium"
                    >
                      <Clock className="w-5 h-5" />
                      Start Meditation
                    </button>
                  </>
                ) : (
                  <>
                    <div className="w-64 h-64 mb-8 rounded-full bg-gradient-to-br from-purple-400 to-blue-400 flex items-center justify-center animate-pulse">
                      <div className="text-center text-white">
                        <p className="text-5xl font-bold mb-2">
                          {formatTime((meditationTime * 60) - meditationSeconds)}
                        </p>
                        <p className="text-lg">Breathe deeply</p>
                      </div>
                    </div>

                    <button
                      onClick={stopMeditation}
                      className="flex items-center gap-2 bg-gray-500 text-white px-8 py-3 rounded-lg hover:bg-gray-600 transition-all text-lg font-medium"
                    >
                      End Session
                    </button>
                  </>
                )}

                <div className="mt-8 text-center text-gray-600 max-w-md">
                  <p className="mb-4">Tips for meditation:</p>
                  <ul className="space-y-2 text-left">
                    <li>• Find a quiet, comfortable space</li>
                    <li>• Sit in a relaxed but upright position</li>
                    <li>• Focus on your breath</li>
                    <li>• When your mind wanders, gently bring it back</li>
                    <li>• Be kind to yourself</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Self-Care Activities */}
          {activeTab === 'selfcare' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Self-Care Activities</h2>
              <p className="text-gray-600 mb-6">Choose an activity to nurture yourself</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {selfCareActivities.map((item, index) => (
                  <div
                    key={index}
                    className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg hover:shadow-md transition-shadow cursor-pointer border-2 border-transparent hover:border-purple-300"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-4xl">{item.icon}</span>
                      <div>
                        <p className="font-medium text-gray-800">{item.activity}</p>
                        <span className="text-xs text-purple-600 bg-purple-100 px-2 py-1 rounded-full">
                          {item.category}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-8 bg-blue-50 border-2 border-blue-200 p-6 rounded-lg">
                <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                  <Sun className="w-5 h-5 text-blue-600" />
                  Self-Care Reminder
                </h3>
                <p className="text-gray-700">
                  Remember that self-care isn't selfish. Taking care of yourself helps you be there for others. 
                  Even small acts of self-care can make a big difference in your mental well-being.
                </p>
              </div>
            </div>
          )}

          {/* Resources */}
          {activeTab === 'resources' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Mental Health Resources</h2>
              <p className="text-gray-600 mb-6">Help is always available</p>

              <div className="space-y-4">
                <div className="bg-red-50 border-2 border-red-300 p-6 rounded-lg">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-bold text-red-900 mb-2">Crisis Support - Available 24/7</h3>
                      <div className="space-y-2 text-gray-700">
                        <p><strong>National Suicide Prevention Lifeline:</strong> 988 or 1-800-273-8255</p>
                        <p><strong>Crisis Text Line:</strong> Text "HELLO" to 741741</p>
                        <p><strong>International:</strong> Visit findahelpline.com</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-blue-50 border-2 border-blue-200 p-6 rounded-lg">
                  <div className="flex items-start gap-3">
                    <Phone className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-bold text-blue-900 mb-2">Mental Health Support</h3>
                      <div className="space-y-2 text-gray-700">
                        <p><strong>SAMHSA National Helpline:</strong> 1-800-662-4357 (Free, confidential, 24/7)</p>
                        <p><strong>Anxiety & Depression Association:</strong> adaa.org</p>
                        <p><strong>NAMI (National Alliance on Mental Illness):</strong> 1-800-950-6264</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-green-50 border-2 border-green-200 p-6 rounded-lg">
                  <div className="flex items-start gap-3">
                    <Users className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-bold text-green-900 mb-2">Professional Help</h3>
                      <div className="space-y-2 text-gray-700">
                        <p><strong>Find a Therapist:</strong> psychologytoday.com/us/therapists</p>
                        <p><strong>Online Therapy:</strong> BetterHelp, Talkspace, 7 Cups</p>
                        <p><strong>Free/Low-Cost Therapy:</strong> Check local community health centers</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-purple-50 border-2 border-purple-200 p-6 rounded-lg">
                  <div className="flex items-start gap-3">
                    <Book className="w-6 h-6 text-purple-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-bold text-purple-900 mb-2">Self-Help Resources</h3>
                      <div className="space-y-2 text-gray-700">
                        <p><strong>Mental Health Apps:</strong> Headspace, Calm, Sanvello, Moodfit</p>
                        <p><strong>Websites:</strong> mindful.org, mentalhealth.gov</p>
                        <p><strong>Books:</strong> "The Anxiety & Phobia Workbook", "Feeling Good" by David Burns</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-yellow-50 border-2 border-yellow-200 p-6 rounded-lg">
                  <h3 className="font-bold text-yellow-900 mb-2">Remember</h3>
                  <p className="text-gray-700">
                    Seeking help is a sign of strength, not weakness. You deserve support, and recovery is possible. 
                    If you're struggling, please reach out to a mental health professional or crisis line.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-600">
          <p className="text-sm">Remember: You're doing great. Take it one day at a time. 💜</p>
        </div>
      </div>
    </div>
  );
}