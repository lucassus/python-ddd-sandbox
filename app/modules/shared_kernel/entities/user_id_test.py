import uuid

from app.modules.shared_kernel.entities.user_id import UserID


def test_user_id_generate():
    user_id = UserID.generate()

    assert isinstance(user_id, UserID)
    assert isinstance(user_id._uuid, uuid.UUID)
    assert len(str(user_id)) == 36


def test_user_id_eq():
    user_id1 = UserID.generate()
    user_id2 = UserID(user_id1._uuid)

    assert user_id1 == user_id2
