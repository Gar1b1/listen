from fastapi import APIRouter, HTTPException, status
from database.models.user import User
from database import db
from sqlalchemy.exc import IntegrityError, NoResultFound

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user_id: str):
    try:
        with db.session() as session:
            session.add(User(user_id=user_id))
            session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with user_id: {user_id} already exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return "User Created Successfully"


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: str):
    try:
        with db.session() as session:
            user = session.query(User).filter_by(user_id=user_id).one()
        return {"user": user.__dict__}
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all_users")
def get_all_users():
    try:
        with db.session() as session:
            users = session.query(User.user_id).all()
        user_ids = [u[0] for u in users]
        return {"users": user_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    try:
        with db.session() as session:
            user = session.query(User).filter_by(user_id=user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            session.delete(user)
            session.commit()
            return  # 204 No Content doesn't return a body
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
