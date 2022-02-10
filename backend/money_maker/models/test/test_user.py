from money_maker.extensions import bcrypt, faker_data
from money_maker.models.user import User


def test_text():
    """
    GIVEN valid user_details
    WHEN a new user is created
    THEN check that the email and password are created

    """
    email = faker_data.ascii_safe_email()
    password = faker_data.password(length=10, special_chars=False)
    new_user = User(email=email, hashed_password=password)
    assert new_user.email == email
    assert bcrypt.check_password_hash(new_user.hashed_password, password)
    