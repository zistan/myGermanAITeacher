"""
Batch Execution Tracker

Track batch executions, enforce daily/weekly caps, maintain execution history.
Persists execution history to JSON file for audit trail and analytics.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class BatchExecutionTracker:
    """Track and manage batch execution history"""

    def __init__(self, log_path: str, retention_days: int = 90):
        """
        Initialize tracker

        Args:
            log_path: Path to JSON log file
            retention_days: How many days to keep execution history
        """
        self.log_path = log_path
        self.retention_days = retention_days
        self.executions = self._load_executions()

        # Ensure log directory exists
        log_dir = os.path.dirname(log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            logger.info(f"Created log directory: {log_dir}")

    def _load_executions(self) -> List[Dict]:
        """Load execution history from JSON file"""
        if not os.path.exists(self.log_path):
            logger.info(f"No existing log file at {self.log_path}, starting fresh")
            return []

        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('executions', [])
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse log file: {e}")
            # Backup corrupted file
            backup_path = f"{self.log_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(self.log_path, backup_path)
            logger.info(f"Backed up corrupted log to {backup_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading executions: {e}")
            return []

    def _save_executions(self):
        """Save execution history to JSON file"""
        try:
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'executions': self.executions,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save executions: {e}")
            raise

    def can_execute_vocabulary(self, requested_count: int, daily_cap: int, weekly_cap: int, global_cap: int) -> Tuple[bool, str]:
        """
        Check if vocabulary batch can run (caps enforcement)

        Args:
            requested_count: Number of words requested
            daily_cap: Daily limit
            weekly_cap: Weekly limit
            global_cap: Total limit

        Returns:
            (can_execute, reason) tuple
        """
        # Get current totals
        current_total = self._get_total_vocabulary()
        daily_total = self.get_daily_totals()['words']
        weekly_total = self.get_weekly_totals()['words']

        # Check global cap
        if current_total >= global_cap:
            return False, f"Global vocabulary cap reached ({current_total}/{global_cap})"

        if current_total + requested_count > global_cap:
            available = global_cap - current_total
            return False, f"Request exceeds global cap (requested: {requested_count}, available: {available})"

        # Check daily cap
        if daily_total >= daily_cap:
            return False, f"Daily vocabulary cap reached ({daily_total}/{daily_cap})"

        if daily_total + requested_count > daily_cap:
            available = daily_cap - daily_total
            return False, f"Request exceeds daily cap (requested: {requested_count}, available: {available})"

        # Check weekly cap
        if weekly_total >= weekly_cap:
            return False, f"Weekly vocabulary cap reached ({weekly_total}/{weekly_cap})"

        if weekly_total + requested_count > weekly_cap:
            available = weekly_cap - weekly_total
            return False, f"Request exceeds weekly cap (requested: {requested_count}, available: {available})"

        return True, "OK"

    def can_execute_grammar(self, requested_count: int, daily_cap: int, weekly_cap: int, global_cap: int) -> Tuple[bool, str]:
        """
        Check if grammar batch can run (caps enforcement)

        Args:
            requested_count: Number of exercises requested
            daily_cap: Daily limit
            weekly_cap: Weekly limit
            global_cap: Total limit

        Returns:
            (can_execute, reason) tuple
        """
        # Get current totals
        current_total = self._get_total_grammar()
        daily_total = self.get_daily_totals()['exercises']
        weekly_total = self.get_weekly_totals()['exercises']

        # Check global cap
        if current_total >= global_cap:
            return False, f"Global grammar cap reached ({current_total}/{global_cap})"

        if current_total + requested_count > global_cap:
            available = global_cap - current_total
            return False, f"Request exceeds global cap (requested: {requested_count}, available: {available})"

        # Check daily cap
        if daily_total >= daily_cap:
            return False, f"Daily grammar cap reached ({daily_total}/{daily_cap})"

        if daily_total + requested_count > daily_cap:
            available = daily_cap - daily_total
            return False, f"Request exceeds daily cap (requested: {requested_count}, available: {available})"

        # Check weekly cap
        if weekly_total >= weekly_cap:
            return False, f"Weekly grammar cap reached ({weekly_total}/{weekly_cap})"

        if weekly_total + requested_count > weekly_cap:
            available = weekly_cap - weekly_total
            return False, f"Request exceeds weekly cap (requested: {requested_count}, available: {available})"

        return True, "OK"

    def log_execution(self, execution_data: Dict):
        """
        Persist execution to JSON log

        Args:
            execution_data: Execution details to log
        """
        # Add timestamp if not present
        if 'timestamp' not in execution_data:
            execution_data['timestamp'] = datetime.now().isoformat()

        # Add daily/weekly totals snapshot
        execution_data['daily_totals'] = self.get_daily_totals()
        execution_data['weekly_totals'] = self.get_weekly_totals()

        # Add to executions list
        self.executions.append(execution_data)

        # Save to file
        self._save_executions()

        logger.info(f"✅ Logged execution: {execution_data.get('execution_id', 'unknown')}")

    def get_daily_totals(self) -> Dict[str, int]:
        """
        Get totals for today

        Returns:
            {"words": X, "exercises": Y}
        """
        today = datetime.now().date()
        words = 0
        exercises = 0

        for execution in self.executions:
            exec_date = datetime.fromisoformat(execution['timestamp']).date()
            if exec_date == today:
                results = execution.get('results', {})
                if execution.get('type') == 'vocabulary':
                    words += results.get('inserted', 0)
                elif execution.get('type') == 'grammar':
                    exercises += results.get('exercises_inserted', 0)

        return {'words': words, 'exercises': exercises}

    def get_weekly_totals(self) -> Dict[str, int]:
        """
        Get totals for this week (Monday to Sunday)

        Returns:
            {"words": X, "exercises": Y}
        """
        today = datetime.now().date()
        # Get Monday of current week
        monday = today - timedelta(days=today.weekday())
        words = 0
        exercises = 0

        for execution in self.executions:
            exec_date = datetime.fromisoformat(execution['timestamp']).date()
            if monday <= exec_date <= today:
                results = execution.get('results', {})
                if execution.get('type') == 'vocabulary':
                    words += results.get('inserted', 0)
                elif execution.get('type') == 'grammar':
                    exercises += results.get('exercises_inserted', 0)

        return {'words': words, 'exercises': exercises}

    def _get_total_vocabulary(self) -> int:
        """Get total vocabulary words generated (all time)"""
        total = 0
        for execution in self.executions:
            if execution.get('type') == 'vocabulary' and execution.get('status') == 'completed':
                results = execution.get('results', {})
                total += results.get('inserted', 0)
        return total

    def _get_total_grammar(self) -> int:
        """Get total grammar exercises generated (all time)"""
        total = 0
        for execution in self.executions:
            if execution.get('type') == 'grammar' and execution.get('status') == 'completed':
                results = execution.get('results', {})
                total += results.get('exercises_inserted', 0)
        return total

    def cleanup_old_executions(self):
        """Remove executions older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        original_count = len(self.executions)

        self.executions = [
            execution for execution in self.executions
            if datetime.fromisoformat(execution['timestamp']) >= cutoff_date
        ]

        removed_count = original_count - len(self.executions)
        if removed_count > 0:
            self._save_executions()
            logger.info(f"🧹 Cleaned up {removed_count} old executions (older than {self.retention_days} days)")

    def get_recent_executions(self, limit: int = 10) -> List[Dict]:
        """
        Get most recent executions

        Args:
            limit: Number of executions to return

        Returns:
            List of execution dictionaries (most recent first)
        """
        # Sort by timestamp descending
        sorted_executions = sorted(
            self.executions,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        return sorted_executions[:limit]

    def get_execution_summary(self) -> Dict:
        """
        Get comprehensive execution summary

        Returns:
            Dictionary with total statistics
        """
        vocab_executions = [e for e in self.executions if e.get('type') == 'vocabulary']
        grammar_executions = [e for e in self.executions if e.get('type') == 'grammar']

        vocab_success = [e for e in vocab_executions if e.get('status') == 'completed']
        grammar_success = [e for e in grammar_executions if e.get('status') == 'completed']

        return {
            'total_executions': len(self.executions),
            'vocabulary': {
                'total_executions': len(vocab_executions),
                'successful': len(vocab_success),
                'total_words_generated': self._get_total_vocabulary(),
            },
            'grammar': {
                'total_executions': len(grammar_executions),
                'successful': len(grammar_success),
                'total_exercises_generated': self._get_total_grammar(),
            },
            'daily_totals': self.get_daily_totals(),
            'weekly_totals': self.get_weekly_totals(),
        }

    def get_history_display(self, limit: int = 10) -> str:
        """
        Get formatted execution history for display

        Args:
            limit: Number of recent executions to show

        Returns:
            Formatted string
        """
        recent = self.get_recent_executions(limit)

        if not recent:
            return "No execution history available"

        lines = [
            "============================================================",
            f"EXECUTION HISTORY (Last {min(limit, len(recent))} runs)",
            "============================================================",
            ""
        ]

        for i, execution in enumerate(recent, 1):
            timestamp = datetime.fromisoformat(execution['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            exec_type = execution.get('type', 'unknown').upper()
            status = execution.get('status', 'unknown')
            status_icon = "✅" if status == "completed" else "❌"

            lines.append(f"{i}. {status_icon} {timestamp} - {exec_type}")

            results = execution.get('results', {})
            if exec_type == "VOCABULARY":
                generated = results.get('generated', 0)
                inserted = results.get('inserted', 0)
                skipped = results.get('skipped_duplicates', 0)
                lines.append(f"   Generated: {generated}, Inserted: {inserted}, Skipped: {skipped}")
            elif exec_type == "GRAMMAR":
                generated = results.get('exercises_generated', 0)
                inserted = results.get('exercises_inserted', 0)
                skipped = results.get('skipped_duplicates', 0)
                lines.append(f"   Generated: {generated}, Inserted: {inserted}, Skipped: {skipped}")

            duration = results.get('duration_seconds', 0)
            lines.append(f"   Duration: {duration:.1f}s")
            lines.append("")

        lines.append("============================================================")
        return "\n".join(lines)


if __name__ == "__main__":
    # Test tracker
    logging.basicConfig(level=logging.INFO)

    tracker = BatchExecutionTracker("logs/batch_execution_test.json")

    # Test execution logging
    test_execution = {
        "execution_id": "test_20260123_120000",
        "type": "vocabulary",
        "status": "completed",
        "results": {
            "generated": 50,
            "inserted": 48,
            "skipped_duplicates": 2,
            "duration_seconds": 45.5
        }
    }

    tracker.log_execution(test_execution)

    # Test cap checking
    can_run, reason = tracker.can_execute_vocabulary(50, 50, 200, 25000)
    print(f"Can execute vocabulary: {can_run} - {reason}")

    # Test summary
    summary = tracker.get_execution_summary()
    print(f"\nSummary: {summary}")

    # Test history display
    print(tracker.get_history_display())
