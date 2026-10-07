# ==============================================================================
# AI KARMAYOGI — AUTHENTICATION & SECURITY UNIT VERIFICATION
# Validates Token Generation, Password Complexity, and RBAC Claims
# ==============================================================================

import uuid
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    create_refresh_token,
    decode_refresh_token,
    validate_password_strength,
)

def test_password_hashing():
    pwd = "Karmayogi2026!"
    hashed = get_password_hash(pwd)
    assert verify_password(pwd, hashed), "Password verification failed"
    assert not verify_password("WrongPassword!", hashed), "Invalid password accepted"
    print("[PASS] Password hashing & verification passed.")

def test_password_policy():
    valid, _ = validate_password_strength("Karmayogi2026!")
    assert valid, "Strong password was rejected"

    weak, msg = validate_password_strength("weak")
    assert not weak, "Weak password was accepted"

    no_digit, _ = validate_password_strength("Karmayogi!")
    assert not no_digit, "Password missing digit was accepted"
    print("[PASS] Password complexity rules passed.")

def test_jwt_access_tokens():
    user_id = str(uuid.uuid4())
    token = create_access_token(
        subject=user_id,
        role="admin",
        department_id="DEPT-DOPT",
        work_role="Director"
    )
    payload = decode_access_token(token)
    assert payload is not None, "Token decoding failed"
    assert payload["sub"] == user_id, "Subject mismatch"
    assert payload["role"] == "admin", "Role claim mismatch"
    assert payload["dept"] == "DEPT-DOPT", "Dept claim mismatch"
    assert payload["work_role"] == "Director", "Work role claim mismatch"
    print("[PASS] JWT Access Token creation & claims validation passed.")

def test_jwt_refresh_tokens():
    user_id = str(uuid.uuid4())
    token = create_refresh_token(subject=user_id)
    payload = decode_refresh_token(token)
    assert payload is not None, "Refresh token decoding failed"
    assert payload["sub"] == user_id, "Subject mismatch"
    assert payload.get("type") == "refresh", "Token type claim mismatch"
    print("[PASS] JWT Refresh Token rotation & claims validation passed.")

if __name__ == "__main__":
    print("\n--- Running AI Karmayogi Auth & Security Tests ---")
    test_password_hashing()
    test_password_policy()
    test_jwt_access_tokens()
    test_jwt_refresh_tokens()
    print("All auth & security unit tests passed successfully!\n")
