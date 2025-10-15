import asyncio 

async def login(PAGE, BRIGHTSPACE_URL: str, USER_USERNAME: str, USER_PASSWORD: str):
    TRUMAN_LOGIN_BUTTON: str = "text='Truman Login'"
    USERNAME_FIELD: str = "#username"
    PASSWORD_FIELD: str = "#password"
    BRIGHTSPACE_LOGIN_BUTTON: str = "text='LOGIN'"

    await PAGE.goto(BRIGHTSPACE_URL)
    await PAGE.click(TRUMAN_LOGIN_BUTTON)
    await PAGE.fill(USERNAME_FIELD, USER_USERNAME)
    await PAGE.fill(PASSWORD_FIELD, USER_PASSWORD)
    await PAGE.click(BRIGHTSPACE_LOGIN_BUTTON)

