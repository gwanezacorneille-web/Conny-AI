class IntegrationSecurityGate:

    def validate_session(self, account, token):
        if account is None:
            return False

        if not account.is_active:
            return False

        if not token:
            return False

        return True

    def validate_account_boundary(self, owner_id, requested_id):
        if not owner_id or not requested_id:
            return False

        return owner_id == requested_id
