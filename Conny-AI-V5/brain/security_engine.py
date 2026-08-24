class SecurityEngine:
    """
    CONNY AI Security Engine V15

    Checks user input before it reaches the
    main intelligence pipeline.
    """

    def __init__(self):

        self.blocked_words = {
            # Add inappropriate words here.
            # Keep this list maintained separately
            # from the main Brain.
        }

        self.blocked_phrases = {
            # Add blocked phrases here.
        }

        self.last_result = {
            "allowed": True,
            "reason": None
        }

    # ==================================================
    # CHECK
    # ==================================================

    def check(self, message):

        text = str(message).lower().strip()

        # ----------------------------------------------
        # Empty input
        # ----------------------------------------------

        if not text:

            return self._result(
                True,
                None
            )

        # ----------------------------------------------
        # Check phrases
        # ----------------------------------------------

        for phrase in self.blocked_phrases:

            if phrase in text:

                return self._result(
                    False,
                    "inappropriate language"
                )

        # ----------------------------------------------
        # Check individual words
        # ----------------------------------------------

        words = text.split()

        for word in words:

            cleaned = word.strip(
                ".,!?;:'\"()[]{}"
            )

            if cleaned in self.blocked_words:

                return self._result(
                    False,
                    "inappropriate language"
                )

        # ----------------------------------------------
        # Allowed
        # ----------------------------------------------

        return self._result(
            True,
            None
        )

    # ==================================================
    # RESULT
    # ==================================================

    def _result(
        self,
        allowed,
        reason
    ):

        self.last_result = {
            "allowed": allowed,
            "reason": reason
        }

        print(
            "DEBUG Security:",
            "ALLOWED" if allowed else "BLOCKED"
        )

        if reason:

            print(
                "DEBUG Security Reason:",
                reason
            )

        return self.last_result

    # ==================================================
    # LAST RESULT
    # ==================================================

    def get_last_result(self):

        return self.last_result
