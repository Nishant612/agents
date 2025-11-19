# interruption_filter.py

class InterruptionFilter:
    """
    Intelligent interruption handler for LiveKit agents.
    Prevents fillers like “uh”, “umm”, “haan”, “hmm” from interrupting TTS.

    Logic:
    - If user is speaking a filler → ignore
    - If confidence is too low → ignore
    - If agent is speaking & user says a real phrase → true interruption
    """

    def __init__(self):
        # Common filler / hesitation sounds
        self.filler_words = {
            "uh", "umm", "um", "hmm", "haan", "huh",
            "hmmm", "mmm", "hmm", "aa", "arey", "hmm?", 
            "huh?", "haan?", "hmm.", "uhh", "er", "eh"
        }

        self.agent_is_speaking = False

    def update_speaking(self, is_speaking: bool):
        """
        Called each time the agent's speaking state changes.
        """
        self.agent_is_speaking = is_speaking

    def _is_filler(self, text: str) -> bool:
        """
        Determine if the text is mostly filler, hesitation, or meaningless sound.
        """
        t = text.strip().lower()

        # Direct filler match
        if t in self.filler_words:
            return True

        # Very short sounds (<=2 chars), mostly vowels, are fillers
        if len(t) <= 2 and all(ch in "aeiouhmn" for ch in t):
            return True

        # Repeated characters like "hmmm", "uhhhh"
        if len(set(t)) <= 2 and any(c in t for c in ["h", "m", "u"]):
            return True

        return False

    def should_interrupt(self, transcript: str, confidence: float) -> bool:
        """
        Determine whether the agent should stop speaking because the user interrupted.
        """

        text = transcript.strip().lower()

        # Ignore extremely low-confidence transcripts
        if confidence is not None and confidence < 0.50:
            return False

        # If the transcript is filler-like → ignore
        if self._is_filler(text):
            return False

        # If the agent is NOT speaking → no interruption required
        if not self.agent_is_speaking:
            return False

        # User said something meaningful → interrupt!
        return True
