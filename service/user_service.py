# from model.user import User
#
# async def is_email_existed(user: User):
#     user = await User.find_one(User.email == user.email)
#     return user is not None
#
# async def is_username_existed(user: User):
#     user = await User.find_one(User.username == user.username)
#     return user is not None
#
# async def create(user: User):
#     user.username = user.email
#     return await User.insert_one(user)
