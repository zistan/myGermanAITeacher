"""
Seed achievements and badges for gamification.
Run this script to populate the achievements table with default achievements.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app.models.achievement import Achievement


def create_achievements():
    """Create default achievements."""
    achievements = [
        # ========== CONVERSATION ACHIEVEMENTS ==========
        {
            "name": "First Steps",
            "description": "Complete your first conversation session",
            "category": "conversation",
            "badge_icon": "chat",
            "badge_color": "#94a3b8",
            "criteria_type": "conversation_sessions",
            "criteria_value": 1,
            "tier": "bronze",
            "points": 10
        },
        {
            "name": "Conversationalist",
            "description": "Complete 10 conversation sessions",
            "category": "conversation",
            "badge_icon": "chat_multiple",
            "badge_color": "#60a5fa",
            "criteria_type": "conversation_sessions",
            "criteria_value": 10,
            "tier": "silver",
            "points": 50
        },
        {
            "name": "Master Communicator",
            "description": "Complete 50 conversation sessions",
            "category": "conversation",
            "badge_icon": "chat_star",
            "badge_color": "#fbbf24",
            "criteria_type": "conversation_sessions",
            "criteria_value": 50,
            "tier": "gold",
            "points": 200
        },
        {
            "name": "Language Expert",
            "description": "Complete 100 conversation sessions",
            "category": "conversation",
            "badge_icon": "chat_crown",
            "badge_color": "#a78bfa",
            "criteria_type": "conversation_sessions",
            "criteria_value": 100,
            "tier": "platinum",
            "points": 500
        },

        # ========== GRAMMAR ACHIEVEMENTS ==========
        {
            "name": "Grammar Beginner",
            "description": "Master your first grammar topic",
            "category": "grammar",
            "badge_icon": "book",
            "badge_color": "#94a3b8",
            "criteria_type": "topics_mastered",
            "criteria_value": 1,
            "tier": "bronze",
            "points": 15
        },
        {
            "name": "Grammar Apprentice",
            "description": "Master 5 grammar topics",
            "category": "grammar",
            "badge_icon": "book_open",
            "badge_color": "#60a5fa",
            "criteria_type": "topics_mastered",
            "criteria_value": 5,
            "tier": "silver",
            "points": 75
        },
        {
            "name": "Grammar Scholar",
            "description": "Master 20 grammar topics",
            "category": "grammar",
            "badge_icon": "book_star",
            "badge_color": "#fbbf24",
            "criteria_type": "topics_mastered",
            "criteria_value": 20,
            "tier": "gold",
            "points": 300
        },
        {
            "name": "Grammar Perfectionist",
            "description": "Achieve 90%+ grammar accuracy over 100 exercises",
            "category": "grammar",
            "badge_icon": "check_circle",
            "badge_color": "#10b981",
            "criteria_type": "grammar_accuracy",
            "criteria_value": 90,
            "tier": "gold",
            "points": 250
        },
        {
            "name": "Grammar Master",
            "description": "Master 50 grammar topics",
            "category": "grammar",
            "badge_icon": "book_crown",
            "badge_color": "#a78bfa",
            "criteria_type": "topics_mastered",
            "criteria_value": 50,
            "tier": "platinum",
            "points": 750
        },

        # ========== VOCABULARY ACHIEVEMENTS ==========
        {
            "name": "Word Collector",
            "description": "Learn your first 10 words",
            "category": "vocabulary",
            "badge_icon": "card",
            "badge_color": "#94a3b8",
            "criteria_type": "words_learned",
            "criteria_value": 10,
            "tier": "bronze",
            "points": 10
        },
        {
            "name": "Vocabulary Builder",
            "description": "Learn 100 words",
            "category": "vocabulary",
            "badge_icon": "cards",
            "badge_color": "#60a5fa",
            "criteria_type": "words_learned",
            "criteria_value": 100,
            "tier": "silver",
            "points": 100
        },
        {
            "name": "Lexicon Expert",
            "description": "Learn 500 words",
            "category": "vocabulary",
            "badge_icon": "cards_star",
            "badge_color": "#fbbf24",
            "criteria_type": "words_learned",
            "criteria_value": 500,
            "tier": "gold",
            "points": 500
        },
        {
            "name": "Word Master",
            "description": "Fully master 100 words (level 5)",
            "category": "vocabulary",
            "badge_icon": "trophy",
            "badge_color": "#fbbf24",
            "criteria_type": "words_mastered",
            "criteria_value": 100,
            "tier": "gold",
            "points": 300
        },
        {
            "name": "Polyglot",
            "description": "Learn 1000 words",
            "category": "vocabulary",
            "badge_icon": "cards_crown",
            "badge_color": "#a78bfa",
            "criteria_type": "words_learned",
            "criteria_value": 1000,
            "tier": "platinum",
            "points": 1000
        },
        {
            "name": "Vocabulary Precision",
            "description": "Achieve 90%+ vocabulary review accuracy",
            "category": "vocabulary",
            "badge_icon": "target",
            "badge_color": "#10b981",
            "criteria_type": "vocabulary_accuracy",
            "criteria_value": 90,
            "tier": "gold",
            "points": 200
        },

        # ========== ACTIVITY ACHIEVEMENTS ==========
        {
            "name": "Getting Started",
            "description": "Complete 5 total sessions",
            "category": "activity",
            "badge_icon": "rocket",
            "badge_color": "#94a3b8",
            "criteria_type": "sessions_count",
            "criteria_value": 5,
            "tier": "bronze",
            "points": 20
        },
        {
            "name": "Consistent Learner",
            "description": "Complete 25 total sessions",
            "category": "activity",
            "badge_icon": "star",
            "badge_color": "#60a5fa",
            "criteria_type": "sessions_count",
            "criteria_value": 25,
            "tier": "silver",
            "points": 100
        },
        {
            "name": "Dedicated Student",
            "description": "Complete 100 total sessions",
            "category": "activity",
            "badge_icon": "star_multiple",
            "badge_color": "#fbbf24",
            "criteria_type": "sessions_count",
            "criteria_value": 100,
            "tier": "gold",
            "points": 400
        },
        {
            "name": "Learning Machine",
            "description": "Complete 250 total sessions",
            "category": "activity",
            "badge_icon": "lightning",
            "badge_color": "#a78bfa",
            "criteria_type": "sessions_count",
            "criteria_value": 250,
            "tier": "platinum",
            "points": 1000
        },

        # ========== STREAK ACHIEVEMENTS ==========
        {
            "name": "Week Warrior",
            "description": "Study for 7 days in a row",
            "category": "activity",
            "badge_icon": "fire",
            "badge_color": "#f97316",
            "criteria_type": "streak_days",
            "criteria_value": 7,
            "tier": "bronze",
            "points": 50
        },
        {
            "name": "Two Week Champion",
            "description": "Study for 14 days in a row",
            "category": "activity",
            "badge_icon": "fire_double",
            "badge_color": "#f97316",
            "criteria_type": "streak_days",
            "criteria_value": 14,
            "tier": "silver",
            "points": 100
        },
        {
            "name": "Month Master",
            "description": "Study for 30 days in a row",
            "category": "activity",
            "badge_icon": "fire_star",
            "badge_color": "#ef4444",
            "criteria_type": "streak_days",
            "criteria_value": 30,
            "tier": "gold",
            "points": 300
        },
        {
            "name": "Unstoppable",
            "description": "Study for 100 days in a row",
            "category": "activity",
            "badge_icon": "fire_crown",
            "badge_color": "#dc2626",
            "criteria_type": "streak_days",
            "criteria_value": 100,
            "tier": "platinum",
            "points": 1000
        },

        # ========== SPECIAL ACHIEVEMENTS ==========
        {
            "name": "Early Bird",
            "description": "Complete a session before 8 AM",
            "category": "activity",
            "badge_icon": "sunrise",
            "badge_color": "#fbbf24",
            "criteria_type": "early_session",
            "criteria_value": 1,
            "tier": "bronze",
            "points": 25
        },
        {
            "name": "Night Owl",
            "description": "Complete a session after 10 PM",
            "category": "activity",
            "badge_icon": "moon",
            "badge_color": "#6366f1",
            "criteria_type": "late_session",
            "criteria_value": 1,
            "tier": "bronze",
            "points": 25
        },
        {
            "name": "Weekend Warrior",
            "description": "Study on 10 different weekends",
            "category": "activity",
            "badge_icon": "calendar",
            "badge_color": "#10b981",
            "criteria_type": "weekend_sessions",
            "criteria_value": 10,
            "tier": "silver",
            "points": 100
        },
        {
            "name": "Marathon Learner",
            "description": "Complete a 60+ minute session",
            "category": "activity",
            "badge_icon": "clock",
            "badge_color": "#8b5cf6",
            "criteria_type": "long_session",
            "criteria_value": 60,
            "tier": "silver",
            "points": 75
        },
        {
            "name": "Speedster",
            "description": "Complete 10 sessions in one day",
            "category": "activity",
            "badge_icon": "zap",
            "badge_color": "#eab308",
            "criteria_type": "daily_sessions",
            "criteria_value": 10,
            "tier": "gold",
            "points": 200
        },
        {
            "name": "Perfectionist",
            "description": "Complete 20 exercises in a row with 100% accuracy",
            "category": "grammar",
            "badge_icon": "diamond",
            "badge_color": "#06b6d4",
            "criteria_type": "perfect_streak",
            "criteria_value": 20,
            "tier": "platinum",
            "points": 500
        },
    ]

    return achievements


def seed_achievements():
    """Seed the database with achievements."""
    db = SessionLocal()

    try:
        print("🏆 Starting achievement seeding...")

        # Check if achievements already exist
        existing_count = db.query(Achievement).count()
        if existing_count > 0:
            print(f"⚠️  Found {existing_count} existing achievements. Clearing...")
            db.query(Achievement).delete()
            db.commit()

        achievements = create_achievements()

        # Add achievements
        for achievement_data in achievements:
            achievement = Achievement(**achievement_data)
            db.add(achievement)

        db.commit()

        print(f"✅ Successfully seeded {len(achievements)} achievements!")
        print("\nAchievements by category:")

        categories = {}
        for achievement in achievements:
            category = achievement["category"]
            categories[category] = categories.get(category, 0) + 1

        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} achievements")

        print("\nAchievements by tier:")
        tiers = {}
        for achievement in achievements:
            tier = achievement["tier"]
            tiers[tier] = tiers.get(tier, 0) + 1

        for tier in ["bronze", "silver", "gold", "platinum"]:
            count = tiers.get(tier, 0)
            print(f"  {tier}: {count} achievements")

        total_points = sum(a["points"] for a in achievements)
        print(f"\nTotal achievement points available: {total_points}")

    except Exception as e:
        print(f"❌ Error seeding achievements: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_achievements()
