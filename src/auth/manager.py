from typing import Optional

from fastapi_users import exceptions, models
from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin
from starlette import status
from starlette.responses import RedirectResponse

from .utils import get_user_db
from config import SECRET

from auth.models import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_login(
            self,
            user: models.UP,
            request: Optional[Request] = None,
            response: Optional[Response] = None,
    ) -> RedirectResponse:
        is_admin = getattr(user, 'is_superuser', False)

        # Определение целевого URL-адреса в зависимости от типа пользователя
        target_url = "/pages/admin" if is_admin else "/pages/base"

        # Устанавливаем целевой URL-адрес в заголовке Location
        response.headers["Location"] = target_url

        # Возвращаем объект RedirectResponse с кодом 303
        return response

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def get(self, id: models.ID) -> models.UP:
        """
        Get a user by id.

        :param id: Id. of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get(id)

        if user is None:
            raise exceptions.UserNotExists()

        return user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
