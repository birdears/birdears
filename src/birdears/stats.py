import sqlite3
import datetime
from contextlib import contextmanager

class Stats:
    def __init__(self, filename=None):
        self.filename = filename if filename else 'birdears.sqlite'
        self._create_table()

    def _create_table(self):
        with self._get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    exercise_type TEXT,
                    mode TEXT,
                    tonic TEXT,
                    octave INTEGER,
                    is_descending BOOLEAN,
                    is_chromatic BOOLEAN,
                    user_answer TEXT,
                    correct_answer TEXT,
                    is_correct BOOLEAN
                )
            ''')

    @contextmanager
    def _get_cursor(self):
        conn = sqlite3.connect(self.filename)
        try:
            yield conn.cursor()
            conn.commit()
        finally:
            conn.close()

    def record_attempt(self, exercise_type, question, response):
        """
        Records an attempt into the database.

        Args:
            exercise_type (str): The type of exercise (e.g., 'melodic', 'harmonic').
            question (QuestionBase): The question object containing exercise parameters.
            response (dict): The response dictionary from check_question, containing 'is_correct', 'user_response_str', etc.
        """

        timestamp = datetime.datetime.now()

        # Extract question parameters
        mode = question.mode
        tonic = question.tonic_str
        octave = question.octave
        is_descending = question.is_descending
        is_chromatic = question.is_chromatic

        # Extract response details
        # For interval questions, response is dict with user_response_str.
        # For some others it might vary, but user_response_str is standard in print_response.
        user_answer = response.get('user_response_str', str(response.get('user_interval', '')))
        correct_answer = response.get('correct_response_str', str(response.get('correct_interval', '')))
        is_correct = response['is_correct']

        with self._get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO attempts (
                    timestamp, exercise_type, mode, tonic, octave,
                    is_descending, is_chromatic, user_answer, correct_answer, is_correct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp, exercise_type, mode, tonic, octave,
                is_descending, is_chromatic, user_answer, correct_answer, is_correct
            ))

    def get_session_summary(self, session_start_time):
        """
        Retrieves a summary of the current session's attempts.

        Args:
            session_start_time (datetime): The start time of the session.

        Returns:
            dict: A dictionary containing session stats (total, correct, percent).
        """
        with self._get_cursor() as cursor:
            # Note: sqlite stores DATETIME as string usually, but we are passing python datetime object
            # which sqlite3 adapter converts. Comparison should work if consistency is maintained.
            cursor.execute('''
                SELECT COUNT(*), SUM(CASE WHEN is_correct THEN 1 ELSE 0 END)
                FROM attempts
                WHERE timestamp >= ?
            ''', (session_start_time,))
            row = cursor.fetchone()

            total = row[0] if row[0] else 0
            correct = row[1] if row[1] else 0
            percent = (correct / total * 100) if total > 0 else 0.0

            return {
                'total': total,
                'correct': correct,
                'percent': percent
            }

    def get_global_stats(self):
        """
        Retrieves aggregated global statistics by exercise type.

        Returns:
            list: A list of dictionaries, one for each exercise type.
        """
        with self._get_cursor() as cursor:
            cursor.execute('''
                SELECT exercise_type, COUNT(*), SUM(CASE WHEN is_correct THEN 1 ELSE 0 END)
                FROM attempts
                GROUP BY exercise_type
            ''')
            rows = cursor.fetchall()

            stats = []
            for row in rows:
                # row: (exercise_type, count, correct_sum)
                total = row[1]
                correct = row[2] if row[2] else 0
                percent = (correct / total * 100) if total > 0 else 0.0
                stats.append({
                    'exercise_type': row[0],
                    'total': total,
                    'correct': correct,
                    'percent': percent
                })
            return stats

    def get_detailed_stats(self):
        """
        Retrieves detailed statistics grouped by exercise, mode, tonic, and octave.

        Returns:
            list: A list of dictionaries.
        """
        with self._get_cursor() as cursor:
            cursor.execute('''
                SELECT exercise_type, mode, tonic, octave,
                       COUNT(*), SUM(CASE WHEN is_correct THEN 1 ELSE 0 END)
                FROM attempts
                GROUP BY exercise_type, mode, tonic, octave
                ORDER BY exercise_type, mode, tonic, octave
            ''')
            rows = cursor.fetchall()

            stats = []
            for row in rows:
                # row: (exercise_type, mode, tonic, octave, total, correct)
                total = row[4]
                correct = row[5] if row[5] else 0
                percent = (correct / total * 100) if total > 0 else 0.0
                stats.append({
                    'exercise_type': row[0],
                    'mode': row[1],
                    'tonic': row[2],
                    'octave': row[3],
                    'total': total,
                    'correct': correct,
                    'percent': percent
                })
            return stats
