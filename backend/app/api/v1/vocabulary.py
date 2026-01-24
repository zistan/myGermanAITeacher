"""
Vocabulary learning API endpoints.
Handles flashcards, quizzes, personal lists, and progress tracking.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_, desc
from typing import List, Optional
from datetime import datetime, timedelta
import random
import hashlib
import json

from app.database import get_db
from app.models.user import User
from app.models.vocabulary import (
    Vocabulary, UserVocabularyProgress, UserVocabularyList,
    VocabularyListWord, VocabularyReview, FlashcardSession, VocabularyQuiz
)
from app.schemas.vocabulary import (
    VocabularyResponse, VocabularyWithProgress, VocabularyCreate,
    FlashcardResponse, FlashcardSessionResponse, StartFlashcardSessionRequest,
    SubmitFlashcardAnswerRequest, SubmitFlashcardAnswerResponse,
    PersonalVocabularyListCreate, PersonalVocabularyListResponse,
    PersonalVocabularyListWithWords, AddWordToListRequest,
    VocabularyQuizRequest, VocabularyQuizResponse, VocabularyQuizQuestion,
    SubmitQuizAnswerRequest, SubmitQuizAnswerResponse,
    VocabularyProgressSummary, WordMasteryDetail, VocabularyReviewQueueResponse,
    AnalyzeWordRequest, WordAnalysisResponse,
    DetectVocabularyRequest, DetectVocabularyResponse, DetectedVocabularyItem,
    VocabularyStatistics, WordRecommendationRequest, WordRecommendationResponse
)
from app.services.vocabulary_ai_service import VocabularyAIService
from app.api.deps import get_current_user

router = APIRouter()


# ========== VOCABULARY WORD ENDPOINTS ==========

@router.get("/v1/vocabulary/words", response_model=List[VocabularyResponse])
def get_vocabulary_words(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    part_of_speech: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get vocabulary words with optional filters."""
    query = db.query(Vocabulary)

    if category:
        query = query.filter(Vocabulary.category == category)
    if difficulty:
        query = query.filter(Vocabulary.difficulty == difficulty)
    if part_of_speech:
        query = query.filter(Vocabulary.part_of_speech == part_of_speech)
    if search:
        query = query.filter(
            or_(
                Vocabulary.word.ilike(f"%{search}%"),
                Vocabulary.translation_it.ilike(f"%{search}%")
            )
        )

    words = query.offset(skip).limit(limit).all()

    # Convert booleans from integer to boolean for schema validation
    result = []
    for word in words:
        word_dict = {
            "id": word.id,
            "word": word.word,
            "translation_it": word.translation_it,
            "part_of_speech": word.part_of_speech,
            "gender": word.gender,
            "plural_form": word.plural_form,
            "difficulty": word.difficulty,
            "category": word.category,
            "example_de": word.example_de,
            "example_it": word.example_it,
            "pronunciation": word.pronunciation,
            "definition_de": word.definition_de,
            "usage_notes": word.usage_notes,
            "synonyms": [],  # TODO: Parse JSON from synonyms column
            "antonyms": [],  # TODO: Parse JSON from antonyms column
            "is_idiom": bool(word.is_idiom),
            "is_compound": bool(word.is_compound),
            "is_separable_verb": bool(word.is_separable_verb),
            "created_at": word.created_at
        }
        result.append(word_dict)

    return result


@router.get("/v1/vocabulary/words/{word_id}", response_model=VocabularyWithProgress)
def get_vocabulary_word(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single vocabulary word with user's progress."""
    word = db.query(Vocabulary).filter(Vocabulary.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    # Get user's progress for this word
    progress = db.query(UserVocabularyProgress).filter(
        UserVocabularyProgress.user_id == current_user.id,
        UserVocabularyProgress.word_id == word_id
    ).first()

    # Build response with progress
    word_dict = {
        "id": word.id,
        "word": word.word,
        "translation_it": word.translation_it,
        "part_of_speech": word.part_of_speech,
        "gender": word.gender,
        "plural_form": word.plural_form,
        "difficulty": word.difficulty,
        "category": word.category,
        "example_de": word.example_de,
        "example_it": word.example_it,
        "pronunciation": word.pronunciation,
        "definition_de": word.definition_de,
        "usage_notes": word.usage_notes,
        "synonyms": [],  # TODO: Parse JSON from synonyms column
        "antonyms": [],  # TODO: Parse JSON from antonyms column
        "is_idiom": bool(word.is_idiom),
        "is_compound": bool(word.is_compound),
        "is_separable_verb": bool(word.is_separable_verb),
        "created_at": word.created_at,
        "mastery_level": progress.mastery_level if progress else None,
        "times_reviewed": progress.times_reviewed if progress else 0,
        "last_reviewed": progress.last_reviewed if progress else None,
        "next_review_due": progress.next_review_date if progress else None,
        "accuracy_rate": (progress.times_correct / progress.times_reviewed * 100) if (progress and progress.times_reviewed > 0) else None
    }

    return word_dict


@router.post("/v1/vocabulary/words", response_model=VocabularyResponse)
def create_vocabulary_word(
    word_data: VocabularyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new vocabulary word (admin only for now)."""
    # Check if word already exists
    existing = db.query(Vocabulary).filter(Vocabulary.word == word_data.word).first()
    if existing:
        raise HTTPException(status_code=400, detail="Word already exists")

    word = Vocabulary(
        word=word_data.word,
        translation_it=word_data.translation_it,
        part_of_speech=word_data.part_of_speech,
        gender=word_data.gender,
        plural_form=word_data.plural_form,
        difficulty=word_data.difficulty,
        category=word_data.category,
        example_de=word_data.example_de,
        example_it=word_data.example_it,
        pronunciation=word_data.pronunciation,
        definition_de=word_data.definition_de,
        usage_notes=word_data.usage_notes,
        synonyms=None,  # TODO: Convert list to JSON string
        antonyms=None,  # TODO: Convert list to JSON string
        is_idiom=1 if word_data.is_idiom else 0,
        is_compound=1 if word_data.is_compound else 0,
        is_separable_verb=1 if word_data.is_separable_verb else 0
    )

    db.add(word)
    db.commit()
    db.refresh(word)

    # Build response with boolean conversion
    return {
        "id": word.id,
        "word": word.word,
        "translation_it": word.translation_it,
        "part_of_speech": word.part_of_speech,
        "gender": word.gender,
        "plural_form": word.plural_form,
        "difficulty": word.difficulty,
        "category": word.category,
        "example_de": word.example_de,
        "example_it": word.example_it,
        "pronunciation": word.pronunciation,
        "definition_de": word.definition_de,
        "usage_notes": word.usage_notes,
        "synonyms": [],
        "antonyms": [],
        "is_idiom": bool(word.is_idiom),
        "is_compound": bool(word.is_compound),
        "is_separable_verb": bool(word.is_separable_verb),
        "created_at": word.created_at
    }


# ========== FLASHCARD ENDPOINTS ==========


@router.post("/v1/vocabulary/flashcards/start", response_model=FlashcardSessionResponse)
def start_flashcard_session(
    request: StartFlashcardSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a new flashcard practice session."""
    query = db.query(Vocabulary)

    # Filter words
    if request.word_ids:
        query = query.filter(Vocabulary.id.in_(request.word_ids))
    if request.category:
        query = query.filter(Vocabulary.category == request.category)
    if request.difficulty:
        query = query.filter(Vocabulary.difficulty == request.difficulty)

    # Get words
    available_words = query.all()
    if not available_words:
        raise HTTPException(status_code=404, detail="No words found matching criteria")

    # Prioritize words using spaced repetition
    if request.use_spaced_repetition:
        word_priorities = []
        for word in available_words:
            progress = db.query(UserVocabularyProgress).filter(
                UserVocabularyProgress.user_id == current_user.id,
                UserVocabularyProgress.word_id == word.id
            ).first()

            if not progress or progress.next_review_date is None:
                priority = 100  # New words get high priority
            elif progress.next_review_date <= datetime.utcnow():
                days_overdue = (datetime.utcnow() - progress.next_review_date).days
                priority = 50 + days_overdue * 10  # Overdue words get priority
            else:
                priority = 1  # Not due yet

            word_priorities.append((word, priority))

        # Sort by priority and take top words
        word_priorities.sort(key=lambda x: x[1], reverse=True)
        selected_words = [w for w, _ in word_priorities[:request.card_count]]
    else:
        # Random selection
        selected_words = random.sample(available_words, min(request.card_count, len(available_words)))

    # Determine card types
    card_types = request.card_types or ["definition", "translation", "usage"]

    # Generate flashcards
    ai_service = VocabularyAIService()
    cards = []

    for word in selected_words:
        card_type = random.choice(card_types)

        word_info = {
            "translation_it": word.translation_it,
            "definition_de": word.definition_de,
            "part_of_speech": word.part_of_speech,
            "usage_notes": word.usage_notes,
            "examples": [{"de": word.example_de, "it": word.example_it}] if word.example_de else []
        }

        card_content = ai_service.generate_flashcard_content(word.word, word_info, card_type)

        card_id = hashlib.md5(f"{word.id}_{card_type}_{datetime.utcnow().timestamp()}".encode()).hexdigest()

        # Ensure required fields have default values if AI service fails
        front = card_content.get("front") or f"What does '{word.word}' mean?"
        back = card_content.get("back") or word.translation_it or "Translation not available"

        cards.append({
            "card_id": card_id,
            "word_id": word.id,
            "word": word.word,
            "card_type": card_type,
            "front": front,
            "back": back,
            "hint": card_content.get("hint", ""),
            "difficulty": word.difficulty
        })

    # Create session in database
    db_session = FlashcardSession(
        user_id=current_user.id,
        total_cards=len(cards),
        current_index=0,
        cards_data=json.dumps(cards),  # Store cards as JSON string
        use_spaced_repetition=1 if request.use_spaced_repetition else 0,
        category=request.category,
        difficulty=request.difficulty
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return {
        "session_id": db_session.id,
        "total_cards": len(cards),
        "current_card_number": 1,
        "current_card": cards[0]
    }


@router.post("/v1/vocabulary/flashcards/{session_id}/answer", response_model=SubmitFlashcardAnswerResponse)
def submit_flashcard_answer(
    session_id: int,
    request: SubmitFlashcardAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit answer to a flashcard and get next card."""
    # Query session from database
    db_session = db.query(FlashcardSession).filter(
        FlashcardSession.id == session_id
    ).first()

    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    if db_session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your session")

    # Parse cards from JSON
    cards = json.loads(db_session.cards_data)

    # Find the card
    card = next((c for c in cards if c["card_id"] == request.card_id), None)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    # Evaluate answer
    correct_answer = card["back"]
    user_answer = request.user_answer.strip().lower()
    is_correct = user_answer in correct_answer.lower()

    # Update user progress
    progress = db.query(UserVocabularyProgress).filter(
        UserVocabularyProgress.user_id == current_user.id,
        UserVocabularyProgress.word_id == card["word_id"]
    ).first()

    if not progress:
        progress = UserVocabularyProgress(
            user_id=current_user.id,
            word_id=card["word_id"],
            mastery_level=0,
            times_reviewed=0,
            times_correct=0,
            times_incorrect=0,
            current_streak=0,
            confidence_score=0.0
        )
        db.add(progress)

    progress.times_reviewed += 1
    progress.last_reviewed = datetime.utcnow()

    if is_correct:
        progress.times_correct += 1
        progress.current_streak += 1

        # Spaced repetition algorithm (SM-2 inspired)
        if progress.mastery_level < 5:
            progress.mastery_level += 1

        # Calculate next review interval based on confidence and mastery
        base_interval = [1, 3, 7, 14, 30, 60][progress.mastery_level]
        confidence_multiplier = request.confidence_level / 3.0
        interval_days = int(base_interval * confidence_multiplier)
    else:
        # Reset on failure
        progress.times_incorrect += 1
        progress.current_streak = 0
        if progress.mastery_level > 0:
            progress.mastery_level -= 1
        interval_days = 1

    progress.next_review_date = datetime.utcnow() + timedelta(days=interval_days)
    # Note: accuracy_rate is calculated dynamically, not stored in the model

    # Record review
    review = VocabularyReview(
        user_id=current_user.id,
        word_id=card["word_id"],
        review_type="flashcard",
        was_correct=1 if is_correct else 0,
        time_spent_seconds=request.time_spent_seconds,
        confidence_rating=request.confidence_level
    )
    db.add(review)
    db.commit()

    # Generate feedback
    if is_correct:
        if request.confidence_level >= 4:
            feedback = "Perfekt! Du kennst dieses Wort sehr gut."
        else:
            feedback = "Richtig! Weiter so!"
    else:
        feedback = f"Nicht ganz. Die richtige Antwort ist: {correct_answer}"

    # Get next card and update database
    db_session.current_index += 1
    db.commit()

    next_card = None
    if db_session.current_index < len(cards):
        next_card = cards[db_session.current_index]

    return {
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "feedback": feedback,
        "next_review_interval_days": interval_days,
        "next_card": next_card
    }


@router.get("/v1/vocabulary/flashcards/{session_id}/current", response_model=FlashcardResponse)
def get_current_flashcard(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the current flashcard in a session."""
    # Query session from database
    db_session = db.query(FlashcardSession).filter(
        FlashcardSession.id == session_id
    ).first()

    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    if db_session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your session")

    # Parse cards from JSON
    cards = json.loads(db_session.cards_data)

    if db_session.current_index >= len(cards):
        raise HTTPException(status_code=400, detail="Session completed")

    return cards[db_session.current_index]


# ========== PERSONAL VOCABULARY LIST ENDPOINTS ==========

@router.post("/v1/vocabulary/lists", response_model=PersonalVocabularyListResponse)
def create_vocabulary_list(
    list_data: PersonalVocabularyListCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a personal vocabulary list."""
    vocab_list = UserVocabularyList(
        user_id=current_user.id,
        name=list_data.name,
        description=list_data.description,
        is_public=1 if list_data.is_public else 0
    )

    db.add(vocab_list)
    db.commit()
    db.refresh(vocab_list)

    return {
        "id": vocab_list.id,
        "name": vocab_list.name,
        "description": vocab_list.description,
        "is_public": bool(vocab_list.is_public),
        "word_count": 0,
        "created_at": vocab_list.created_at,
        "updated_at": vocab_list.updated_at
    }


@router.get("/v1/vocabulary/lists", response_model=List[PersonalVocabularyListResponse])
def get_vocabulary_lists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all personal vocabulary lists."""
    lists = db.query(UserVocabularyList).filter(
        UserVocabularyList.user_id == current_user.id
    ).all()

    result = []
    for vocab_list in lists:
        word_count = db.query(VocabularyListWord).filter(
            VocabularyListWord.list_id == vocab_list.id
        ).count()

        result.append({
            "id": vocab_list.id,
            "name": vocab_list.name,
            "description": vocab_list.description,
            "is_public": bool(vocab_list.is_public),
            "word_count": word_count,
            "created_at": vocab_list.created_at,
            "updated_at": vocab_list.updated_at
        })

    return result


@router.get("/v1/vocabulary/lists/{list_id}", response_model=PersonalVocabularyListWithWords)
def get_vocabulary_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a vocabulary list with all its words."""
    vocab_list = db.query(UserVocabularyList).filter(
        UserVocabularyList.id == list_id
    ).first()

    if not vocab_list:
        raise HTTPException(status_code=404, detail="List not found")

    if vocab_list.user_id != current_user.id and not vocab_list.is_public:
        raise HTTPException(status_code=403, detail="Access denied")

    # Get words in list
    list_words = db.query(VocabularyListWord).filter(
        VocabularyListWord.list_id == list_id
    ).all()

    words = []
    for list_word in list_words:
        word = db.query(Vocabulary).filter(Vocabulary.id == list_word.word_id).first()
        if word:
            progress = db.query(UserVocabularyProgress).filter(
                UserVocabularyProgress.user_id == current_user.id,
                UserVocabularyProgress.word_id == word.id
            ).first()

            words.append({
                "id": word.id,
                "word": word.word,
                "translation_it": word.translation_it,
                "part_of_speech": word.part_of_speech,
                "gender": word.gender,
                "plural_form": word.plural_form,
                "difficulty": word.difficulty,
                "category": word.category,
                "example_de": word.example_de,
                "example_it": word.example_it,
                "pronunciation": word.pronunciation,
                "definition_de": word.definition_de,
                "usage_notes": word.usage_notes,
                "synonyms": [],  # TODO: Parse JSON
                "antonyms": [],  # TODO: Parse JSON
                "is_idiom": bool(word.is_idiom),
                "is_compound": bool(word.is_compound),
                "is_separable_verb": bool(word.is_separable_verb),
                "created_at": word.created_at,
                "mastery_level": progress.mastery_level if progress else None,
                "times_reviewed": progress.times_reviewed if progress else 0,
                "last_reviewed": progress.last_reviewed if progress else None,
                "next_review_due": progress.next_review_date if progress else None,
                "accuracy_rate": (progress.times_correct / progress.times_reviewed * 100) if (progress and progress.times_reviewed > 0) else None
            })

    return {
        "id": vocab_list.id,
        "name": vocab_list.name,
        "description": vocab_list.description,
        "is_public": bool(vocab_list.is_public),
        "word_count": len(words),
        "created_at": vocab_list.created_at,
        "updated_at": vocab_list.updated_at,
        "words": words
    }


@router.post("/v1/vocabulary/lists/{list_id}/words")
def add_word_to_list(
    list_id: int,
    request: AddWordToListRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a word to a personal vocabulary list."""
    vocab_list = db.query(UserVocabularyList).filter(
        UserVocabularyList.id == list_id,
        UserVocabularyList.user_id == current_user.id
    ).first()

    if not vocab_list:
        raise HTTPException(status_code=404, detail="List not found")

    # Check if word exists
    word = db.query(Vocabulary).filter(Vocabulary.id == request.word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    # Check if already added
    existing = db.query(VocabularyListWord).filter(
        VocabularyListWord.list_id == list_id,
        VocabularyListWord.word_id == request.word_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Word already in list")

    list_word = VocabularyListWord(
        list_id=list_id,
        word_id=request.word_id,
        notes=request.notes
    )

    db.add(list_word)
    vocab_list.updated_at = datetime.utcnow()
    db.commit()

    return {"message": "Word added to list"}


@router.delete("/v1/vocabulary/lists/{list_id}/words/{word_id}")
def remove_word_from_list(
    list_id: int,
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a word from a personal vocabulary list."""
    vocab_list = db.query(UserVocabularyList).filter(
        UserVocabularyList.id == list_id,
        UserVocabularyList.user_id == current_user.id
    ).first()

    if not vocab_list:
        raise HTTPException(status_code=404, detail="List not found")

    list_word = db.query(VocabularyListWord).filter(
        VocabularyListWord.list_id == list_id,
        VocabularyListWord.word_id == word_id
    ).first()

    if not list_word:
        raise HTTPException(status_code=404, detail="Word not in list")

    db.delete(list_word)
    vocab_list.updated_at = datetime.utcnow()
    db.commit()

    return {"message": "Word removed from list"}


@router.delete("/v1/vocabulary/lists/{list_id}")
def delete_vocabulary_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a personal vocabulary list."""
    vocab_list = db.query(UserVocabularyList).filter(
        UserVocabularyList.id == list_id,
        UserVocabularyList.user_id == current_user.id
    ).first()

    if not vocab_list:
        raise HTTPException(status_code=404, detail="List not found")

    db.delete(vocab_list)
    db.commit()

    return {"message": "List deleted"}


# ========== VOCABULARY QUIZ ENDPOINTS ==========


@router.post("/v1/vocabulary/quiz/generate", response_model=VocabularyQuizResponse)
def generate_vocabulary_quiz(
    request: VocabularyQuizRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a vocabulary quiz."""
    query = db.query(Vocabulary)

    # Filter words
    if request.word_ids:
        query = query.filter(Vocabulary.id.in_(request.word_ids))
    if request.category:
        query = query.filter(Vocabulary.category == request.category)
    if request.difficulty:
        query = query.filter(Vocabulary.difficulty == request.difficulty)

    words = query.limit(request.question_count).all()

    if not words:
        raise HTTPException(status_code=404, detail="No words found matching criteria")

    # Generate quiz using AI
    ai_service = VocabularyAIService()
    word_list = [w.word for w in words]

    quiz_questions = ai_service.generate_vocabulary_quiz(
        words=word_list,
        quiz_type=request.quiz_type,
        difficulty=request.difficulty or "B2"
    )

    # Store quiz in database
    db_quiz = VocabularyQuiz(
        user_id=current_user.id,
        quiz_type=request.quiz_type,
        total_questions=len(quiz_questions),
        questions_data=json.dumps(quiz_questions),  # Store questions as JSON string
        category=request.category,
        difficulty=request.difficulty
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    # Format questions
    formatted_questions = []
    for i, q in enumerate(quiz_questions):
        question_id = f"{db_quiz.id}_{i}"
        formatted_questions.append({
            "question_id": question_id,
            "question": q.get("question", ""),
            "question_type": request.quiz_type,
            "options": q.get("options"),
            "correct_answer": q.get("correct_answer", ""),
            "word_tested": q.get("word_tested", ""),
            "explanation": q.get("explanation", "")
        })

    estimated_duration = len(formatted_questions) * 2  # 2 minutes per question

    return {
        "quiz_id": db_quiz.id,
        "questions": formatted_questions,
        "total_questions": len(formatted_questions),
        "estimated_duration_minutes": estimated_duration
    }


@router.post("/v1/vocabulary/quiz/{quiz_id}/answer", response_model=SubmitQuizAnswerResponse)
def submit_quiz_answer(
    quiz_id: int,
    request: SubmitQuizAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit an answer to a quiz question."""
    # Query quiz from database
    db_quiz = db.query(VocabularyQuiz).filter(
        VocabularyQuiz.id == quiz_id
    ).first()

    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if db_quiz.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your quiz")

    # Parse questions from JSON
    questions = json.loads(db_quiz.questions_data)

    # Parse question_id
    parts = request.question_id.split("_")
    if len(parts) != 2:
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question_index = int(parts[1])
    if question_index >= len(questions):
        raise HTTPException(status_code=404, detail="Question not found")

    question = questions[question_index]
    correct_answer = question.get("correct_answer", "")
    is_correct = request.user_answer.strip().lower() == correct_answer.lower()

    points_earned = 10 if is_correct else 0

    return {
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "explanation": question.get("explanation", ""),
        "points_earned": points_earned
    }


@router.post("/v1/vocabulary/quiz/{quiz_id}/complete")
def complete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a vocabulary quiz as completed."""
    # Query quiz from database
    db_quiz = db.query(VocabularyQuiz).filter(
        VocabularyQuiz.id == quiz_id
    ).first()

    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if db_quiz.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your quiz")

    # Update completed_at timestamp
    db_quiz.completed_at = datetime.utcnow()
    db.commit()

    return {
        "quiz_id": quiz_id,
        "completed_at": db_quiz.completed_at,
        "message": "Quiz completed successfully"
    }


# ========== VOCABULARY PROGRESS ENDPOINTS ==========

@router.get("/v1/vocabulary/progress/summary", response_model=VocabularyProgressSummary)
def get_vocabulary_progress_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get overall vocabulary learning progress."""
    # Get all user's progress
    all_progress = db.query(UserVocabularyProgress).filter(
        UserVocabularyProgress.user_id == current_user.id
    ).all()

    total_words = len(all_progress)

    # Words by level
    words_by_level = {}
    for progress in all_progress:
        word = db.query(Vocabulary).filter(Vocabulary.id == progress.word_id).first()
        if word:
            level = word.difficulty
            words_by_level[level] = words_by_level.get(level, 0) + 1

    # Words by category
    words_by_category = {}
    for progress in all_progress:
        word = db.query(Vocabulary).filter(Vocabulary.id == progress.word_id).first()
        if word:
            category = word.category
            words_by_category[category] = words_by_category.get(category, 0) + 1

    # Mastery breakdown
    mastery_breakdown = {}
    for progress in all_progress:
        level = f"level_{progress.mastery_level}"
        mastery_breakdown[level] = mastery_breakdown.get(level, 0) + 1

    # Review time (from reviews)
    total_time = db.query(func.sum(VocabularyReview.time_spent_seconds)).filter(
        VocabularyReview.user_id == current_user.id
    ).scalar() or 0

    # Streak (simplified - days with reviews)
    recent_reviews = db.query(VocabularyReview).filter(
        VocabularyReview.user_id == current_user.id,
        VocabularyReview.reviewed_at >= datetime.utcnow() - timedelta(days=30)
    ).all()

    review_dates = set(r.reviewed_at.date() for r in recent_reviews)
    current_streak = 0
    check_date = datetime.utcnow().date()
    while check_date in review_dates:
        current_streak += 1
        check_date -= timedelta(days=1)

    # Words due today
    words_due_today = db.query(UserVocabularyProgress).filter(
        UserVocabularyProgress.user_id == current_user.id,
        UserVocabularyProgress.next_review_date <= datetime.utcnow()
    ).count()

    # Words due this week
    week_end = datetime.utcnow() + timedelta(days=7)
    words_due_week = db.query(UserVocabularyProgress).filter(
        UserVocabularyProgress.user_id == current_user.id,
        UserVocabularyProgress.next_review_date <= week_end
    ).count()

    return {
        "total_words_learned": total_words,
        "words_by_level": words_by_level,
        "words_by_category": words_by_category,
        "mastery_breakdown": mastery_breakdown,
        "total_review_time_minutes": total_time // 60,
        "current_streak_days": current_streak,
        "words_due_today": words_due_today,
        "words_due_this_week": words_due_week
    }


@router.get("/v1/vocabulary/progress/review-queue", response_model=VocabularyReviewQueueResponse)
def get_vocabulary_review_queue(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get words due for review based on spaced repetition."""
    now = datetime.utcnow()

    # Overdue words
    overdue = db.query(UserVocabularyProgress).filter(
        UserVocabularyProgress.user_id == current_user.id,
        UserVocabularyProgress.next_review_date < now - timedelta(days=1)
    ).all()

    # Due today
    today_end = now.replace(hour=23, minute=59, second=59)
    due_today = db.query(UserVocabularyProgress).filter(
        UserVocabularyProgress.user_id == current_user.id,
        UserVocabularyProgress.next_review_date >= now - timedelta(days=1),
        UserVocabularyProgress.next_review_date <= today_end
    ).all()

    # Upcoming (next 7 days)
    week_end = now + timedelta(days=7)
    upcoming = db.query(UserVocabularyProgress).filter(
        UserVocabularyProgress.user_id == current_user.id,
        UserVocabularyProgress.next_review_date > today_end,
        UserVocabularyProgress.next_review_date <= week_end
    ).limit(20).all()

    def format_progress(progress_list):
        result = []
        for progress in progress_list:
            word = db.query(Vocabulary).filter(Vocabulary.id == progress.word_id).first()
            if word:
                result.append({
                    "id": word.id,
                    "word": word.word,
                    "translation_it": word.translation_it,
                    "part_of_speech": word.part_of_speech,
                    "gender": word.gender,
                    "plural_form": word.plural_form,
                    "difficulty": word.difficulty,
                    "category": word.category,
                    "example_de": word.example_de,
                    "example_it": word.example_it,
                    "pronunciation": word.pronunciation,
                    "definition_de": word.definition_de,
                    "usage_notes": word.usage_notes,
                    "synonyms": [],  # TODO: Parse JSON
                    "antonyms": [],  # TODO: Parse JSON
                    "is_idiom": bool(word.is_idiom),
                    "is_compound": bool(word.is_compound),
                    "is_separable_verb": bool(word.is_separable_verb),
                    "created_at": word.created_at,
                    "mastery_level": progress.mastery_level,
                    "times_reviewed": progress.times_reviewed,
                    "last_reviewed": progress.last_reviewed,
                    "next_review_due": progress.next_review_date,
                    "accuracy_rate": (progress.times_correct / progress.times_reviewed * 100) if progress.times_reviewed > 0 else None
                })
        return result

    return {
        "overdue_count": len(overdue),
        "due_today_count": len(due_today),
        "upcoming_count": len(upcoming),
        "overdue_words": format_progress(overdue),
        "due_today_words": format_progress(due_today),
        "upcoming_words": format_progress(upcoming)
    }


# ========== AI-POWERED ANALYSIS ENDPOINTS ==========

@router.post("/v1/vocabulary/analyze", response_model=WordAnalysisResponse)
def analyze_word(
    request: AnalyzeWordRequest,
    current_user: User = Depends(get_current_user)
):
    """Analyze a German word using AI."""
    try:
        ai_service = VocabularyAIService()

        analysis = ai_service.analyze_word(
            word=request.word,
            user_level="B2",  # Could get from user profile
            include_examples=request.include_examples
        )

        # Check if analysis failed
        if "error" in analysis:
            raise HTTPException(
                status_code=500,
                detail=f"Word analysis failed: {analysis.get('error', 'Unknown error')}"
            )

        # Ensure all required fields are present with defaults
        return {
            "word": analysis.get("word", request.word),
            "translation_it": analysis.get("translation_it", "Traduzione non disponibile"),
            "part_of_speech": analysis.get("part_of_speech", "unknown"),
            "gender": analysis.get("gender"),
            "plural_form": analysis.get("plural_form"),
            "difficulty_level": analysis.get("difficulty_level", "B2"),
            "pronunciation": analysis.get("pronunciation", ""),
            "definition_de": analysis.get("definition_de", "Definition nicht verfügbar"),
            "usage_notes": analysis.get("usage_notes"),
            "synonyms": analysis.get("synonyms", []),
            "antonyms": analysis.get("antonyms", []),
            "examples": analysis.get("examples", []),
            "collocations": analysis.get("collocations", []),
            "is_compound": analysis.get("is_compound", False),
            "compound_parts": analysis.get("compound_parts"),
            "is_separable": analysis.get("is_separable", False),
            "separable_prefix": analysis.get("separable_prefix"),
            "register": analysis.get("register", "neutral"),
            "frequency": analysis.get("frequency", "common")
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing word: {str(e)}"
        )


@router.post("/v1/vocabulary/detect", response_model=DetectVocabularyResponse)
def detect_vocabulary_from_text(
    request: DetectVocabularyRequest,
    current_user: User = Depends(get_current_user)
):
    """Detect important vocabulary from German text using AI."""
    ai_service = VocabularyAIService()

    detected = ai_service.detect_vocabulary_from_text(
        text=request.text,
        user_level="B2",
        min_difficulty=request.min_difficulty
    )

    detected = detected[:request.max_words]

    return {
        "detected_words": detected,
        "total_detected": len(detected)
    }


@router.post("/v1/vocabulary/recommend", response_model=WordRecommendationResponse)
def get_word_recommendations(
    request: WordRecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get personalized word recommendations."""
    query = db.query(Vocabulary)

    # Filter by category and difficulty
    if request.category:
        query = query.filter(Vocabulary.category == request.category)
    if request.difficulty:
        query = query.filter(Vocabulary.difficulty == request.difficulty)

    # Get words user hasn't learned yet
    learned_word_ids = db.query(UserVocabularyProgress.word_id).filter(
        UserVocabularyProgress.user_id == current_user.id
    ).all()
    learned_ids = [w[0] for w in learned_word_ids]

    if learned_ids:
        query = query.filter(~Vocabulary.id.in_(learned_ids))

    words = query.limit(request.count).all()

    # Format as words with progress
    result = []
    for word in words:
        result.append({
            "id": word.id,
            "word": word.word,
            "translation_it": word.translation_it,
            "part_of_speech": word.part_of_speech,
            "gender": word.gender,
            "plural_form": word.plural_form,
            "difficulty": word.difficulty,
            "category": word.category,
            "example_de": word.example_de,
            "example_it": word.example_it,
            "pronunciation": word.pronunciation,
            "definition_de": word.definition_de,
            "usage_notes": word.usage_notes,
            "synonyms": [],  # TODO: Parse JSON
            "antonyms": [],  # TODO: Parse JSON
            "is_idiom": bool(word.is_idiom),
            "is_compound": bool(word.is_compound),
            "is_separable_verb": bool(word.is_separable_verb),
            "created_at": word.created_at,
            "mastery_level": None,
            "times_reviewed": 0,
            "last_reviewed": None,
            "next_review_due": None,
            "accuracy_rate": None
        })

    reason = f"These words match your criteria ({request.recommendation_type}) and haven't been learned yet."

    return {
        "recommended_words": result,
        "reason": reason
    }
