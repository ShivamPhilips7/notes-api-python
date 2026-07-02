from app.security.jwt_handler import (
    create_access_token,
    decode_access_token,
)


def test_create_token():

    token = create_access_token(
        {
            "sub": "ash"
        }
    )

    assert token is not None


def test_decode_token():

    token = create_access_token(
        {
            "sub": "ash"
        }
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "ash"