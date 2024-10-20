# agents/feedback_agent.py

class FeedbackAgent:
    def generate_feedback(self, questions, answers):
        feedback = []
        # Example feedback based on the user's answers
        for i, answer in enumerate(answers):
            if "improve" in answer.lower():
                feedback.append(f"Good response to Question {i+1}, but provide more specific actions.")
            else:
                feedback.append(f"Try to focus on actionable strategies for Question {i+1}.")
        return feedback
        
    def collect_rating(self, feedback_index, rating):
        """
        Collects the user's rating for a specific feedback point.

        Args:
            feedback_index (int): The index of the feedback item being rated.
            rating (int): The user's rating (e.g., 1 to 5).

        Returns:
            None
        """
        # Initialize the ratings list if it doesn't exist
        if not hasattr(self, 'ratings'):
            self.ratings = []
        
        # Ensure the ratings list is large enough
        while len(self.ratings) <= feedback_index:
            self.ratings.append(None)
        
        # Store the rating
        self.ratings[feedback_index] = rating