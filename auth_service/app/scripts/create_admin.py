import asyncio
import sys

from app.core.database import new_session
from app.core.security import hash_password
from app.models.user import UserRole
from app.repositories.user import UserRepository


async def main():
    if len(sys.argv) < 3:
        print("Usage: python -m app.scripts.create_admin <email> <password>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]

    async with new_session() as session:
        repo = UserRepository(session)
        user = await repo.get_by_email(email)
        if user:
            await repo.update(user, {"role": UserRole.ADMIN, "is_active": True})
            print(f"User {email} promoted to admin")
        else:
            await repo.create(
                {
                    "email": email,
                    "hashed_password": hash_password(password),
                    "role": UserRole.ADMIN,
                    "is_active": True,
                }
            )
            print(f"Admin {email} created successfully")


if __name__ == "__main__":
    asyncio.run(main())
