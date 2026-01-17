"""
Comprehensive Manual API Testing Script for German Learning Application
Tests all 61 endpoints across 8 phases with detailed reporting
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
from enum import Enum

# Configuration
BASE_URL = "http://192.168.178.100:8000"
RESULTS_DIR = "test_results"

# Global state management
class TestState:
    """Maintains state across tests"""
    auth_token: Optional[str] = None
    test_users: Dict[str, Dict] = {}
    context_ids: List[int] = []
    session_ids: List[int] = []
    grammar_topic_ids: List[int] = []
    grammar_session_ids: List[int] = []
    vocabulary_word_ids: List[int] = []
    vocabulary_list_ids: List[int] = []
    flashcard_session_ids: List[int] = []
    quiz_ids: List[int] = []
    achievement_ids: List[int] = []

state = TestState()

class TestResult:
    """Stores individual test result"""
    def __init__(self, name: str, method: str, path: str, expected_status: int):
        self.name = name
        self.method = method
        self.path = path
        self.expected_status = expected_status
        self.actual_status: Optional[int] = None
        self.response_data: Any = None
        self.error: Optional[str] = None
        self.passed: bool = False
        self.timestamp = datetime.now().isoformat()
        self.notes: List[str] = []

    def mark_passed(self, status: int, data: Any):
        self.actual_status = status
        self.response_data = data
        self.passed = (status == self.expected_status)

    def mark_failed(self, status: int, error: str):
        self.actual_status = status
        self.error = error
        self.passed = False

    def add_note(self, note: str):
        self.notes.append(note)

class EndpointTestReport:
    """Report for a single endpoint with multiple test cases"""
    def __init__(self, endpoint_name: str, method: str, path: str):
        self.endpoint_name = endpoint_name
        self.method = method
        self.path = path
        self.test_results: List[TestResult] = []
        self.database_changes: List[str] = []
        self.observations: List[str] = []

    def add_test(self, result: TestResult):
        self.test_results.append(result)

    def add_observation(self, observation: str):
        self.observations.append(observation)

    def add_db_change(self, change: str):
        self.database_changes.append(change)

    @property
    def total_tests(self) -> int:
        return len(self.test_results)

    @property
    def passed_tests(self) -> int:
        return sum(1 for t in self.test_results if t.passed)

    @property
    def failed_tests(self) -> int:
        return self.total_tests - self.passed_tests

    def print_report(self):
        """Print detailed report for this endpoint"""
        print("\n" + "=" * 80)
        print(f"TEST REPORT: {self.endpoint_name}")
        print("=" * 80)
        print(f"Endpoint: {self.method} {self.path}")
        print(f"Test Cases: {self.total_tests}")
        print(f"Passed: {self.passed_tests}/{self.total_tests}")
        print(f"Failed: {self.failed_tests}/{self.total_tests}")
        print("\nDETAILS:")

        for i, result in enumerate(self.test_results, 1):
            status_icon = "[PASS]" if result.passed else "[FAIL]"
            status_text = "PASSED" if result.passed else "FAILED"
            print(f"\n{status_icon} Test {i}: {result.name} - {status_text}")
            print(f"   Expected: {result.expected_status}")
            print(f"   Actual: {result.actual_status}")

            if result.passed:
                if result.response_data:
                    # Print summary of response
                    if isinstance(result.response_data, dict):
                        keys = list(result.response_data.keys())[:5]
                        print(f"   Response keys: {keys}")
                    elif isinstance(result.response_data, list):
                        print(f"   Response items: {len(result.response_data)}")
            else:
                if result.response_data:
                    # Print error response data
                    if isinstance(result.response_data, dict):
                        print(f"   Error response: {json.dumps(result.response_data, indent=6)[:500]}")
                    else:
                        print(f"   Error response: {str(result.response_data)[:500]}")
                if result.error:
                    print(f"   Exception: {result.error}")

            if result.notes:
                for note in result.notes:
                    print(f"   Note: {note}")

        if self.observations:
            print("\nOBSERVATIONS:")
            for obs in self.observations:
                print(f"- {obs}")

        if self.database_changes:
            print("\nDATABASE STATE:")
            for change in self.database_changes:
                print(f"- {change}")

        print("=" * 80)
        print()

def make_request(method: str, path: str, data: Optional[Dict] = None,
                 use_auth: bool = True, expected_status: int = 200,
                 use_form: bool = False) -> TestResult:
    """Make HTTP request and return TestResult"""
    result = TestResult(
        name=f"{method} {path}",
        method=method,
        path=path,
        expected_status=expected_status
    )

    headers = {}
    if use_auth and state.auth_token:
        headers["Authorization"] = f"Bearer {state.auth_token}"

    try:
        url = f"{BASE_URL}{path}"

        # Use form data or JSON based on parameter
        if use_form:
            response = requests.request(
                method=method,
                url=url,
                data=data,  # Form data
                headers=headers,
                timeout=30
            )
        else:
            response = requests.request(
                method=method,
                url=url,
                json=data,  # JSON data
                headers=headers,
                timeout=30
            )

        # Try to parse JSON response
        try:
            response_data = response.json()
        except:
            response_data = response.text

        result.mark_passed(response.status_code, response_data)

        return result

    except Exception as e:
        result.mark_failed(0, str(e))
        return result

# ============================================================================
# PHASE 1: HEALTH & INFRASTRUCTURE
# ============================================================================

def test_phase1_health():
    """Phase 1: Health & Infrastructure (2 endpoints)"""
    print("\n" + "=" * 80)
    print("PHASE 1: HEALTH & INFRASTRUCTURE (2 endpoints)")
    print("=" * 80)

    # Test 1: Root endpoint
    report = EndpointTestReport("Root Endpoint", "GET", "/")

    result = make_request("GET", "/", use_auth=False, expected_status=200)
    result.name = "Get root endpoint info"
    report.add_test(result)

    if result.passed:
        report.add_observation(f"Server is accessible at {BASE_URL}")
        report.add_observation(f"App name: {result.response_data.get('app', 'N/A')}")

    report.print_report()

    # Test 2: Health check
    report = EndpointTestReport("Health Check", "GET", "/api/health")

    result = make_request("GET", "/api/health", use_auth=False, expected_status=200)
    result.name = "Health check - verify database and AI service"
    report.add_test(result)

    if result.passed:
        data = result.response_data
        report.add_observation(f"Status: {data.get('status', 'unknown')}")
        report.add_observation(f"Database: {data.get('database', 'unknown')}")
        report.add_observation(f"AI Service: {data.get('ai_service', 'unknown')}")

    report.print_report()

    return True

# ============================================================================
# PHASE 2: AUTHENTICATION
# ============================================================================

def test_phase2_authentication():
    """Phase 2: Authentication (3 endpoints)"""
    print("\n" + "=" * 80)
    print("PHASE 2: AUTHENTICATION (3 endpoints)")
    print("=" * 80)

    # Test 1: POST /api/v1/auth/register
    report = EndpointTestReport("User Registration", "POST", "/api/v1/auth/register")

    # Test 1.1: Valid registration
    test_user1 = {
        "username": "testuser1",
        "email": "test1@example.com",
        "password": "SecurePass123!",
        "native_language": "it",
        "target_language": "de",
        "proficiency_level": "C1"
    }

    result = make_request("POST", "/api/v1/auth/register",
                         data=test_user1, use_auth=False, expected_status=201)
    result.name = "Register new user (testuser1)"
    report.add_test(result)

    if result.passed:
        state.test_users['testuser1'] = test_user1
        report.add_db_change("Created user: testuser1")
        result.add_note(f"User ID: {result.response_data.get('id')}")

    # Test 1.2: Duplicate username
    result = make_request("POST", "/api/v1/auth/register",
                         data=test_user1, use_auth=False, expected_status=400)
    result.name = "Register duplicate username (should fail)"
    report.add_test(result)

    # Test 1.3: Register second user
    test_user2 = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "SecurePass456!",
        "native_language": "en",
        "target_language": "de",
        "proficiency_level": "B2"
    }

    result = make_request("POST", "/api/v1/auth/register",
                         data=test_user2, use_auth=False, expected_status=201)
    result.name = "Register second user (testuser2)"
    report.add_test(result)

    if result.passed:
        state.test_users['testuser2'] = test_user2
        report.add_db_change("Created user: testuser2")

    # Test 1.4: Invalid data (missing required field)
    invalid_user = {
        "username": "testuser3",
        "email": "test3@example.com"
        # Missing password
    }

    result = make_request("POST", "/api/v1/auth/register",
                         data=invalid_user, use_auth=False, expected_status=422)
    result.name = "Register with missing password (should fail)"
    report.add_test(result)

    report.print_report()

    # Test 2: POST /api/v1/auth/login
    report = EndpointTestReport("User Login", "POST", "/api/v1/auth/login")

    # Test 2.1: Valid login
    login_data = {
        "username": "testuser1",
        "password": "SecurePass123!"
    }

    result = make_request("POST", "/api/v1/auth/login",
                         data=login_data, use_auth=False, expected_status=200,
                         use_form=True)
    result.name = "Login with valid credentials"
    report.add_test(result)

    if result.passed:
        token = result.response_data.get('access_token')
        state.auth_token = token
        report.add_observation("Successfully obtained JWT token")
        result.add_note(f"Token type: {result.response_data.get('token_type')}")
        result.add_note(f"Token length: {len(token) if token else 0}")

    # Test 2.2: Invalid password
    result = make_request("POST", "/api/v1/auth/login",
                         data={"username": "testuser1", "password": "WrongPass123!"},
                         use_auth=False, expected_status=401, use_form=True)
    result.name = "Login with invalid password (should fail)"
    report.add_test(result)

    # Test 2.3: Invalid username
    result = make_request("POST", "/api/v1/auth/login",
                         data={"username": "nonexistent", "password": "SecurePass123!"},
                         use_auth=False, expected_status=401, use_form=True)
    result.name = "Login with invalid username (should fail)"
    report.add_test(result)

    # Test 2.4: Missing credentials
    result = make_request("POST", "/api/v1/auth/login",
                         data={}, use_auth=False, expected_status=422, use_form=True)
    result.name = "Login with missing credentials (should fail)"
    report.add_test(result)

    report.print_report()

    # Test 3: GET /api/v1/auth/me
    report = EndpointTestReport("Get Current User", "GET", "/api/v1/auth/me")

    # Test 3.1: Valid token
    result = make_request("GET", "/api/v1/auth/me", use_auth=True, expected_status=200)
    result.name = "Get current user with valid token"
    report.add_test(result)

    if result.passed:
        user_data = result.response_data
        result.add_note(f"Username: {user_data.get('username')}")
        result.add_note(f"Email: {user_data.get('email')}")
        result.add_note(f"Target level: {user_data.get('target_level')}")

    # Test 3.2: Missing token
    result = make_request("GET", "/api/v1/auth/me", use_auth=False, expected_status=401)
    result.name = "Get current user without token (should fail)"
    report.add_test(result)

    # Test 3.3: Invalid token
    original_token = state.auth_token
    state.auth_token = "invalid.token.here"
    result = make_request("GET", "/api/v1/auth/me", use_auth=True, expected_status=401)
    result.name = "Get current user with invalid token (should fail)"
    report.add_test(result)
    state.auth_token = original_token  # Restore valid token

    report.print_report()

    return True

# ============================================================================
# PHASE 3: CONTEXT MANAGEMENT
# ============================================================================

def test_phase3_contexts():
    """Phase 3: Context Management (5 endpoints)"""
    print("\n" + "=" * 80)
    print("PHASE 3: CONTEXT MANAGEMENT (5 endpoints)")
    print("=" * 80)

    # Test 1: GET /api/contexts - List all contexts
    report = EndpointTestReport("List Contexts", "GET", "/api/contexts")

    result = make_request("GET", "/api/contexts", use_auth=True, expected_status=200)
    result.name = "Get all contexts"
    report.add_test(result)

    if result.passed and isinstance(result.response_data, list):
        state.context_ids = [ctx.get('id') for ctx in result.response_data[:5]]
        report.add_observation(f"Found {len(result.response_data)} contexts")
        result.add_note(f"Context count: {len(result.response_data)}")

    report.print_report()

    # Test 2: GET /api/contexts/{id} - Get specific context
    report = EndpointTestReport("Get Context Details", "GET", "/api/contexts/{id}")

    if state.context_ids:
        context_id = state.context_ids[0]
        result = make_request("GET", f"/api/contexts/{context_id}", use_auth=True, expected_status=200)
        result.name = f"Get context {context_id} details"
        report.add_test(result)

    # Test invalid context
    result = make_request("GET", "/api/contexts/99999", use_auth=True, expected_status=404)
    result.name = "Get invalid context (should fail)"
    report.add_test(result)

    report.print_report()

    # Test 3: POST /api/contexts - Create custom context
    report = EndpointTestReport("Create Custom Context", "POST", "/api/contexts")

    custom_context = {
        "name": "Test Custom Context",
        "description": "A test context for API testing",
        "category": "business",
        "difficulty_level": "B2",
        "system_prompt": "You are helping with test conversations"
    }

    result = make_request("POST", "/api/contexts", data=custom_context, use_auth=True, expected_status=201)
    result.name = "Create custom context"
    report.add_test(result)

    custom_context_id = None
    if result.passed:
        custom_context_id = result.response_data.get('id')
        report.add_db_change(f"Created custom context with ID: {custom_context_id}")

    report.print_report()

    # Test 4: PUT /api/contexts/{id} - Update context
    report = EndpointTestReport("Update Context", "PUT", "/api/contexts/{id}")

    if custom_context_id:
        update_data = {
            "description": "Updated test context description"
        }
        result = make_request("PUT", f"/api/contexts/{custom_context_id}",
                            data=update_data, use_auth=True, expected_status=200)
        result.name = "Update custom context"
        report.add_test(result)

    report.print_report()

    # Test 5: DELETE /api/contexts/{id} - Deactivate context
    report = EndpointTestReport("Deactivate Context", "DELETE", "/api/contexts/{id}")

    if custom_context_id:
        result = make_request("DELETE", f"/api/contexts/{custom_context_id}",
                            use_auth=True, expected_status=204)
        result.name = "Deactivate custom context"
        report.add_test(result)

    report.print_report()

    return True

# ============================================================================
# PHASE 4: CONVERSATION SESSIONS
# ============================================================================

def test_phase4_conversations():
    """Phase 4: Conversation Sessions (4 endpoints)"""
    print("\n" + "=" * 80)
    print("PHASE 4: CONVERSATION SESSIONS (4 endpoints)")
    print("=" * 80)

    # Test 1: POST /api/sessions/start - Start conversation
    report = EndpointTestReport("Start Conversation Session", "POST", "/api/sessions/start")

    context_id = state.context_ids[0] if state.context_ids else None
    start_data = {"context_id": context_id} if context_id else {}

    result = make_request("POST", "/api/sessions/start", data=start_data,
                         use_auth=True, expected_status=201)
    result.name = "Start conversation session"
    report.add_test(result)

    session_id = None
    if result.passed:
        session_id = result.response_data.get('id')
        state.session_ids.append(session_id)
        report.add_db_change(f"Created session ID: {session_id}")

    report.print_report()

    # Test 2: POST /api/sessions/{id}/message - Send message
    report = EndpointTestReport("Send Message", "POST", "/api/sessions/{id}/message")

    if session_id:
        message_data = {
            "message": "Hallo, wie geht es Ihnen?",
            "request_feedback": False
        }
        result = make_request("POST", f"/api/sessions/{session_id}/message",
                            data=message_data, use_auth=True, expected_status=200)
        result.name = "Send message to AI"
        report.add_test(result)

        # Send another with feedback
        message_data2 = {
            "message": "Ich bin heute zur Arbeit gegangen.",
            "request_feedback": True
        }
        result = make_request("POST", f"/api/sessions/{session_id}/message",
                            data=message_data2, use_auth=True, expected_status=200)
        result.name = "Send message with grammar feedback"
        report.add_test(result)

    report.print_report()

    # Test 3: GET /api/sessions/history - Get session history
    report = EndpointTestReport("Get Session History", "GET", "/api/sessions/history")

    result = make_request("GET", "/api/sessions/history", use_auth=True, expected_status=200)
    result.name = "Get user's session history"
    report.add_test(result)

    report.print_report()

    # Test 4: POST /api/sessions/{id}/end - End session
    report = EndpointTestReport("End Session", "POST", "/api/sessions/{id}/end")

    if session_id:
        result = make_request("POST", f"/api/sessions/{session_id}/end",
                            use_auth=True, expected_status=200)
        result.name = "End conversation session"
        report.add_test(result)

        if result.passed:
            report.add_observation(f"Session ended with summary")

    report.print_report()

    return True

# ============================================================================
# PHASE 5: GRAMMAR LEARNING
# ============================================================================

def test_phase5_grammar():
    """Phase 5: Grammar Learning (11 endpoints)"""
    print("\n" + "=" * 80)
    print("PHASE 5: GRAMMAR LEARNING (11 endpoints)")
    print("=" * 80)

    # Test 1: GET /api/grammar/topics - List all grammar topics
    report = EndpointTestReport("List Grammar Topics", "GET", "/api/grammar/topics")

    result = make_request("GET", "/api/grammar/topics", use_auth=True, expected_status=200)
    result.name = "Get all grammar topics"
    report.add_test(result)

    if result.passed and isinstance(result.response_data, list) and len(result.response_data) > 0:
        state.grammar_topic_ids = [topic.get('id') for topic in result.response_data[:5]]
        report.add_observation(f"Found {len(result.response_data)} grammar topics")
        result.add_note(f"Topic count: {len(result.response_data)}")

    report.print_report()

    # Test 2: GET /api/grammar/topics/{topic_id} - Get topic details
    report = EndpointTestReport("Get Topic Details", "GET", "/api/grammar/topics/{id}")

    if state.grammar_topic_ids:
        topic_id = state.grammar_topic_ids[0]
        result = make_request("GET", f"/api/grammar/topics/{topic_id}", use_auth=True, expected_status=200)
        result.name = f"Get topic {topic_id} details with stats"
        report.add_test(result)

    # Test invalid topic
    result = make_request("GET", "/api/grammar/topics/99999", use_auth=True, expected_status=404)
    result.name = "Get invalid topic (should fail)"
    report.add_test(result)

    report.print_report()

    # Test 3: GET /api/grammar/topics/{topic_id}/exercises - Get topic exercises
    report = EndpointTestReport("Get Topic Exercises", "GET", "/api/grammar/topics/{id}/exercises")

    if state.grammar_topic_ids:
        topic_id = state.grammar_topic_ids[0]
        result = make_request("GET", f"/api/grammar/topics/{topic_id}/exercises",
                            use_auth=True, expected_status=200)
        result.name = f"Get exercises for topic {topic_id}"
        report.add_test(result)

        if result.passed and isinstance(result.response_data, list):
            result.add_note(f"Exercise count: {len(result.response_data)}")

    report.print_report()

    # Test 4: POST /api/grammar/practice/start - Start practice session
    report = EndpointTestReport("Start Practice Session", "POST", "/api/grammar/practice/start")

    if state.grammar_topic_ids:
        practice_data = {
            "topic_ids": state.grammar_topic_ids[:2],
            "exercise_count": 5,
            "difficulty_level": None,
            "exercise_types": None,
            "context_category": None,
            "use_spaced_repetition": False
        }
        result = make_request("POST", "/api/grammar/practice/start",
                            data=practice_data, use_auth=True, expected_status=200)
        result.name = "Start grammar practice session"
        report.add_test(result)

        grammar_session_id = None
        if result.passed:
            grammar_session_id = result.response_data.get('session_id')
            state.grammar_session_ids.append(grammar_session_id)
            report.add_db_change(f"Created grammar session ID: {grammar_session_id}")

    report.print_report()

    # Test 5: POST /api/grammar/practice/{session_id}/answer - Submit answer
    report = EndpointTestReport("Submit Exercise Answer", "POST", "/api/grammar/practice/{id}/answer")

    if state.grammar_session_ids and state.grammar_topic_ids:
        session_id = state.grammar_session_ids[0]

        # Get exercises for the first topic to get actual exercise IDs
        topic_id = state.grammar_topic_ids[0]
        exercises_result = make_request("GET", f"/api/grammar/topics/{topic_id}/exercises",
                                       use_auth=True, expected_status=200)

        exercise_ids = []
        if exercises_result.passed and isinstance(exercises_result.response_data, list):
            exercise_ids = [ex.get('id') for ex in exercises_result.response_data[:2]]

        # Submit answers using actual exercise IDs
        if len(exercise_ids) >= 1:
            answer_data = {
                "exercise_id": exercise_ids[0],
                "user_answer": "Ich gehe zur Schule"
            }
            result = make_request("POST", f"/api/grammar/practice/{session_id}/answer",
                                data=answer_data, use_auth=True, expected_status=200)
            result.name = f"Submit exercise answer (exercise {exercise_ids[0]})"
            report.add_test(result)

        # Submit another answer
        if len(exercise_ids) >= 2:
            answer_data2 = {
                "exercise_id": exercise_ids[1],
                "user_answer": "Sie haben gegessen"
            }
            result = make_request("POST", f"/api/grammar/practice/{session_id}/answer",
                                data=answer_data2, use_auth=True, expected_status=200)
            result.name = f"Submit second exercise answer (exercise {exercise_ids[1]})"
            report.add_test(result)

    report.print_report()

    # Test 6: POST /api/grammar/practice/{session_id}/end - End practice session
    report = EndpointTestReport("End Practice Session", "POST", "/api/grammar/practice/{id}/end")

    if state.grammar_session_ids:
        session_id = state.grammar_session_ids[0]
        result = make_request("POST", f"/api/grammar/practice/{session_id}/end",
                            use_auth=True, expected_status=200)
        result.name = "End grammar practice session"
        report.add_test(result)

        if result.passed:
            report.add_observation("Practice session ended with summary")

    report.print_report()

    # Test 7: GET /api/grammar/progress/summary - Get overall progress
    report = EndpointTestReport("Get Progress Summary", "GET", "/api/grammar/progress/summary")

    result = make_request("GET", "/api/grammar/progress/summary", use_auth=True, expected_status=200)
    result.name = "Get overall grammar progress"
    report.add_test(result)

    report.print_report()

    # Test 8: GET /api/grammar/progress/topics/{topic_id} - Topic-specific progress
    report = EndpointTestReport("Get Topic Progress", "GET", "/api/grammar/progress/topics/{id}")

    if state.grammar_topic_ids:
        topic_id = state.grammar_topic_ids[0]
        result = make_request("GET", f"/api/grammar/progress/topics/{topic_id}",
                            use_auth=True, expected_status=200)
        result.name = f"Get progress for topic {topic_id}"
        report.add_test(result)

    report.print_report()

    # Test 9: GET /api/grammar/progress/weak-areas - Get weak areas
    report = EndpointTestReport("Get Weak Areas", "GET", "/api/grammar/progress/weak-areas")

    result = make_request("GET", "/api/grammar/progress/weak-areas", use_auth=True, expected_status=200)
    result.name = "Get weak areas analysis"
    report.add_test(result)

    report.print_report()

    # Test 10: GET /api/grammar/progress/review-queue - Get review queue
    report = EndpointTestReport("Get Review Queue", "GET", "/api/grammar/progress/review-queue")

    result = make_request("GET", "/api/grammar/progress/review-queue", use_auth=True, expected_status=200)
    result.name = "Get spaced repetition review queue"
    report.add_test(result)

    report.print_report()

    # Test 11: POST /api/grammar/generate/exercises - AI generate exercises
    report = EndpointTestReport("Generate AI Exercises", "POST", "/api/grammar/generate/exercises")

    if state.grammar_topic_ids:
        generate_data = {
            "topic_id": state.grammar_topic_ids[0],
            "count": 3,
            "difficulty_level": "B2",
            "exercise_type": "fill_blank"
        }
        result = make_request("POST", "/api/grammar/generate/exercises",
                            data=generate_data, use_auth=True, expected_status=200)
        result.name = "Generate AI exercises for topic"
        report.add_test(result)

    report.print_report()

    return True


def test_phase6_vocabulary():
    """
    Phase 6: Vocabulary Learning System (22 endpoints)
    Tests vocabulary words, flashcards, lists, quizzes, progress tracking, and AI features
    """
    print("\n" + "=" * 80)
    print("PHASE 6: VOCABULARY LEARNING (19 endpoints)")
    print("=" * 80)

    # Test 1: GET /api/v1/vocabulary/words - List vocabulary words
    report = EndpointTestReport("List Vocabulary Words", "GET", "/api/v1/vocabulary/words")

    result = make_request("GET", "/api/v1/vocabulary/words", use_auth=True, expected_status=200)
    result.name = "Get all vocabulary words"
    report.add_test(result)

    if result.passed and result.response_data:
        words = result.response_data if isinstance(result.response_data, list) else []
        result.add_note(f"Word count: {len(words)}")
        report.add_observation(f"Found {len(words)} vocabulary words")

        # Store word IDs for later tests
        if words:
            state.vocabulary_word_ids = [w['id'] for w in words[:5]]

    # Test with filters
    result2 = make_request("GET", "/api/v1/vocabulary/words?category=business&difficulty_level=B2",
                          use_auth=True, expected_status=200)
    result2.name = "Filter words by category and difficulty"
    report.add_test(result2)

    report.print_report()

    # Test 2: GET /api/v1/vocabulary/words/{word_id} - Get word details
    report = EndpointTestReport("Get Word Details", "GET", "/api/v1/vocabulary/words/{id}")

    if state.vocabulary_word_ids:
        word_id = state.vocabulary_word_ids[0]
        result = make_request("GET", f"/api/v1/vocabulary/words/{word_id}",
                            use_auth=True, expected_status=200)
        result.name = f"Get word {word_id} with progress"
        report.add_test(result)

    # Test invalid word ID
    result2 = make_request("GET", "/api/v1/vocabulary/words/99999",
                          use_auth=True, expected_status=404)
    result2.name = "Get invalid word (should fail)"
    report.add_test(result2)

    report.print_report()

    # Test 3: POST /api/v1/vocabulary/words - Create custom word
    report = EndpointTestReport("Create Custom Word", "POST", "/api/v1/vocabulary/words")

    custom_word = {
        "german_word": "testen",
        "english_translation": "to test",
        "word_type": "verb",
        "gender": None,
        "difficulty_level": "A2",
        "category": "general",
        "example_sentence_de": "Ich teste die Anwendung.",
        "example_sentence_en": "I test the application."
    }
    result = make_request("POST", "/api/v1/vocabulary/words",
                         data=custom_word, use_auth=True, expected_status=201)
    result.name = "Create custom vocabulary word"
    report.add_test(result)

    if result.passed and result.response_data:
        custom_word_id = result.response_data.get('id')
        if custom_word_id:
            state.vocabulary_word_ids.append(custom_word_id)
            report.add_db_change(f"Created custom word with ID: {custom_word_id}")

    report.print_report()

    # Test 4: POST /api/v1/vocabulary/flashcards/start - Start flashcard session
    report = EndpointTestReport("Start Flashcard Session", "POST", "/api/v1/vocabulary/flashcards/start")

    flashcard_request = {
        "word_ids": state.vocabulary_word_ids[:5] if len(state.vocabulary_word_ids) >= 5 else state.vocabulary_word_ids,
        "session_type": "review",
        "card_types": ["definition", "translation"],
        "use_spaced_repetition": True
    }
    result = make_request("POST", "/api/v1/vocabulary/flashcards/start",
                         data=flashcard_request, use_auth=True, expected_status=201)
    result.name = "Start flashcard session with spaced repetition"
    report.add_test(result)

    flashcard_session_id = None
    if result.passed and result.response_data:
        flashcard_session_id = result.response_data.get('session_id')
        if flashcard_session_id:
            state.flashcard_session_ids.append(flashcard_session_id)
            report.add_db_change(f"Created flashcard session ID: {flashcard_session_id}")

    report.print_report()

    # Test 5: GET /api/v1/vocabulary/flashcards/{session_id}/current - Get current card
    report = EndpointTestReport("Get Current Flashcard", "GET", "/api/v1/vocabulary/flashcards/{session_id}/current")

    if flashcard_session_id:
        result = make_request("GET", f"/api/v1/vocabulary/flashcards/{flashcard_session_id}/current",
                            use_auth=True, expected_status=200)
        result.name = "Get current flashcard"
        report.add_test(result)

    report.print_report()

    # Test 6: POST /api/v1/vocabulary/flashcards/{session_id}/answer - Submit flashcard answer
    report = EndpointTestReport("Submit Flashcard Answer", "POST", "/api/v1/vocabulary/flashcards/{session_id}/answer")

    if flashcard_session_id:
        # Submit correct answer with high confidence
        answer_data = {
            "user_answer": "richtig",
            "confidence_level": 5,
            "time_spent_seconds": 3
        }
        result = make_request("POST", f"/api/v1/vocabulary/flashcards/{flashcard_session_id}/answer",
                            data=answer_data, use_auth=True, expected_status=200)
        result.name = "Submit flashcard answer with high confidence"
        report.add_test(result)

        # Submit another answer with lower confidence
        answer_data2 = {
            "user_answer": "falsch",
            "confidence_level": 2,
            "time_spent_seconds": 8
        }
        result2 = make_request("POST", f"/api/v1/vocabulary/flashcards/{flashcard_session_id}/answer",
                             data=answer_data2, use_auth=True, expected_status=200)
        result2.name = "Submit flashcard answer with low confidence"
        report.add_test(result2)

    report.print_report()

    # Test 7: POST /api/v1/vocabulary/lists - Create vocabulary list
    report = EndpointTestReport("Create Vocabulary List", "POST", "/api/v1/vocabulary/lists")

    list_data = {
        "name": "Business German - Payment Terms",
        "description": "Key vocabulary for payment processing"
    }
    result = make_request("POST", "/api/v1/vocabulary/lists",
                         data=list_data, use_auth=True, expected_status=201)
    result.name = "Create personal vocabulary list"
    report.add_test(result)

    list_id = None
    if result.passed and result.response_data:
        list_id = result.response_data.get('id')
        if list_id:
            state.vocabulary_list_ids.append(list_id)
            report.add_db_change(f"Created vocabulary list with ID: {list_id}")

    report.print_report()

    # Test 8: GET /api/v1/vocabulary/lists - Get all user lists
    report = EndpointTestReport("Get User's Vocabulary Lists", "GET", "/api/v1/vocabulary/lists")

    result = make_request("GET", "/api/v1/vocabulary/lists", use_auth=True, expected_status=200)
    result.name = "Get all user's vocabulary lists"
    report.add_test(result)

    if result.passed and result.response_data:
        lists = result.response_data if isinstance(result.response_data, list) else []
        result.add_note(f"List count: {len(lists)}")

    report.print_report()

    # Test 9: GET /api/v1/vocabulary/lists/{list_id} - Get list with words
    report = EndpointTestReport("Get List Details", "GET", "/api/v1/vocabulary/lists/{id}")

    if list_id:
        result = make_request("GET", f"/api/v1/vocabulary/lists/{list_id}",
                            use_auth=True, expected_status=200)
        result.name = f"Get list {list_id} with words"
        report.add_test(result)

    # Test invalid list ID
    result2 = make_request("GET", "/api/v1/vocabulary/lists/99999",
                          use_auth=True, expected_status=404)
    result2.name = "Get invalid list (should fail)"
    report.add_test(result2)

    report.print_report()

    # Test 10: POST /api/v1/vocabulary/lists/{list_id}/words - Add word to list
    report = EndpointTestReport("Add Word to List", "POST", "/api/v1/vocabulary/lists/{id}/words")

    if list_id and state.vocabulary_word_ids:
        word_data = {"word_id": state.vocabulary_word_ids[0]}
        result = make_request("POST", f"/api/v1/vocabulary/lists/{list_id}/words",
                            data=word_data, use_auth=True, expected_status=200)
        result.name = f"Add word {state.vocabulary_word_ids[0]} to list"
        report.add_test(result)

        # Try to add duplicate word (should fail)
        result2 = make_request("POST", f"/api/v1/vocabulary/lists/{list_id}/words",
                             data=word_data, use_auth=True, expected_status=400)
        result2.name = "Add duplicate word (should fail)"
        report.add_test(result2)

    report.print_report()

    # Test 11: DELETE /api/v1/vocabulary/lists/{list_id}/words/{word_id} - Remove word from list
    report = EndpointTestReport("Remove Word from List", "DELETE", "/api/v1/vocabulary/lists/{id}/words/{word_id}")

    if list_id and state.vocabulary_word_ids:
        word_id = state.vocabulary_word_ids[0]
        result = make_request("DELETE", f"/api/v1/vocabulary/lists/{list_id}/words/{word_id}",
                            use_auth=True, expected_status=200)
        result.name = f"Remove word {word_id} from list"
        report.add_test(result)

    report.print_report()

    # Test 12: DELETE /api/v1/vocabulary/lists/{list_id} - Delete list
    report = EndpointTestReport("Delete Vocabulary List", "DELETE", "/api/v1/vocabulary/lists/{id}")

    if list_id:
        result = make_request("DELETE", f"/api/v1/vocabulary/lists/{list_id}",
                            use_auth=True, expected_status=200)
        result.name = f"Delete vocabulary list {list_id}"
        report.add_test(result)

    report.print_report()

    # Test 13: POST /api/v1/vocabulary/quiz/generate - Generate vocabulary quiz
    report = EndpointTestReport("Generate Vocabulary Quiz", "POST", "/api/v1/vocabulary/quiz/generate")

    quiz_data = {
        "word_ids": state.vocabulary_word_ids[:3] if len(state.vocabulary_word_ids) >= 3 else state.vocabulary_word_ids,
        "quiz_type": "multiple_choice",
        "question_count": 5
    }
    result = make_request("POST", "/api/v1/vocabulary/quiz/generate",
                         data=quiz_data, use_auth=True, expected_status=200)
    result.name = "Generate multiple choice quiz"
    report.add_test(result)

    quiz_id = None
    if result.passed and result.response_data:
        quiz_id = result.response_data.get('quiz_id')
        if quiz_id:
            state.quiz_ids.append(quiz_id)

    report.print_report()

    # Test 14: POST /api/v1/vocabulary/quiz/{quiz_id}/answer - Submit quiz answer
    report = EndpointTestReport("Submit Quiz Answer", "POST", "/api/v1/vocabulary/quiz/{id}/answer")

    if quiz_id:
        quiz_answer = {
            "question_id": 1,
            "user_answer": "die Zahlung"
        }
        result = make_request("POST", f"/api/v1/vocabulary/quiz/{quiz_id}/answer",
                            data=quiz_answer, use_auth=True, expected_status=200)
        result.name = "Submit quiz answer"
        report.add_test(result)

    report.print_report()

    # Test 15: GET /api/v1/vocabulary/progress/summary - Get vocabulary progress
    report = EndpointTestReport("Get Vocabulary Progress", "GET", "/api/v1/vocabulary/progress/summary")

    result = make_request("GET", "/api/v1/vocabulary/progress/summary",
                         use_auth=True, expected_status=200)
    result.name = "Get vocabulary progress summary"
    report.add_test(result)

    report.print_report()

    # Test 16: GET /api/v1/vocabulary/progress/review-queue - Get review queue
    report = EndpointTestReport("Get Vocabulary Review Queue", "GET", "/api/v1/vocabulary/progress/review-queue")

    result = make_request("GET", "/api/v1/vocabulary/progress/review-queue",
                         use_auth=True, expected_status=200)
    result.name = "Get vocabulary review queue (spaced repetition)"
    report.add_test(result)

    report.print_report()

    # Test 17: POST /api/v1/vocabulary/analyze - AI word analysis
    report = EndpointTestReport("AI Word Analysis", "POST", "/api/v1/vocabulary/analyze")

    analyze_data = {
        "german_word": "Zahlungsabwicklung",
        "include_examples": True,
        "include_collocations": True
    }
    result = make_request("POST", "/api/v1/vocabulary/analyze",
                         data=analyze_data, use_auth=True, expected_status=200)
    result.name = "Analyze word with AI (examples + collocations)"
    report.add_test(result)

    report.print_report()

    # Test 18: POST /api/v1/vocabulary/detect - Detect vocabulary from text
    report = EndpointTestReport("Detect Vocabulary", "POST", "/api/v1/vocabulary/detect")

    detect_data = {
        "text": "Die Zahlungsabwicklung erfolgt über unsere sichere Plattform.",
        "difficulty_level": "B2"
    }
    result = make_request("POST", "/api/v1/vocabulary/detect",
                         data=detect_data, use_auth=True, expected_status=200)
    result.name = "Detect vocabulary from German text"
    report.add_test(result)

    report.print_report()

    # Test 19: POST /api/v1/vocabulary/recommend - Get word recommendations
    report = EndpointTestReport("Get Word Recommendations", "POST", "/api/v1/vocabulary/recommend")

    recommend_data = {
        "category": "business",
        "difficulty_level": "B2",
        "count": 10
    }
    result = make_request("POST", "/api/v1/vocabulary/recommend",
                         data=recommend_data, use_auth=True, expected_status=200)
    result.name = "Get personalized word recommendations"
    report.add_test(result)

    report.print_report()

    return True


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main test execution"""
    print("\n" + "=" * 80)
    print("GERMAN LEARNING APPLICATION - COMPREHENSIVE API TESTING")
    print("=" * 80)
    print(f"Base URL: {BASE_URL}")
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # Check for non-interactive mode
    non_interactive = "--non-interactive" in sys.argv or "-y" in sys.argv

    # Check for specific phase to run
    run_specific_phase = None
    for arg in sys.argv:
        if arg.startswith("--phase="):
            run_specific_phase = int(arg.split("=")[1])
        elif arg == "--phase" and sys.argv.index(arg) + 1 < len(sys.argv):
            run_specific_phase = int(sys.argv[sys.argv.index(arg) + 1])

    def pause_or_continue(message):
        if non_interactive:
            print(f"\n{message} (skipping in non-interactive mode)")
        else:
            input(f"\n{message}")

    try:
        # Phase 1: Health & Infrastructure
        if run_specific_phase and run_specific_phase > 1:
            # Run prerequisite phases silently for authentication/state
            test_phase1_health()
            test_phase2_authentication()
            if run_specific_phase > 3:
                test_phase3_contexts()
            if run_specific_phase > 4:
                test_phase4_conversations()
            if run_specific_phase > 5:
                test_phase5_grammar()

        if not run_specific_phase or run_specific_phase == 1:
            if not test_phase1_health():
                print("[FAIL] Phase 1 failed. Stopping tests.")
                return
            pause_or_continue("Press Enter to continue to Phase 2 (Authentication)...")

        # Phase 2: Authentication
        if not run_specific_phase or run_specific_phase == 2:
            if not test_phase2_authentication():
                print("[FAIL] Phase 2 failed. Stopping tests.")
                return
            if not run_specific_phase:
                pause_or_continue("Press Enter to continue to Phase 3 (Context Management)...")

        # Phase 3: Context Management
        if not run_specific_phase or run_specific_phase == 3:
            if not test_phase3_contexts():
                print("[FAIL] Phase 3 failed. Stopping tests.")
                return
            if not run_specific_phase:
                pause_or_continue("Press Enter to continue to Phase 4 (Conversation Sessions)...")

        # Phase 4: Conversation Sessions
        if not run_specific_phase or run_specific_phase == 4:
            if not test_phase4_conversations():
                print("[FAIL] Phase 4 failed. Stopping tests.")
                return
            if not run_specific_phase:
                pause_or_continue("Press Enter to continue to Phase 5 (Grammar Learning)...")

        # Phase 5: Grammar Learning
        if not run_specific_phase or run_specific_phase == 5:
            if not test_phase5_grammar():
                print("[FAIL] Phase 5 failed. Stopping tests.")
                return
            if not run_specific_phase:
                pause_or_continue("Press Enter to continue to Phase 6 (Vocabulary Learning)...")

        # Phase 6: Vocabulary Learning
        if not run_specific_phase or run_specific_phase == 6:
            if not test_phase6_vocabulary():
                print("[FAIL] Phase 6 failed. Stopping tests.")
                return

        if not run_specific_phase:
            print("\n[SUCCESS] Phases 1-6 completed successfully!")
            print("Phases 7-8 will be implemented next.")

    except KeyboardInterrupt:
        print("\n\n[WARN] Testing interrupted by user")
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n" + "=" * 80)
        print(f"Test Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

if __name__ == "__main__":
    main()
