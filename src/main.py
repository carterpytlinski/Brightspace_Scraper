from playwright.async_api import async_playwright
import asyncio
from dotenv import load_dotenv
import os
import time
from brightspace_scraper.modules.auth import login
from brightspace_scraper.utils.credentials import getUserCredentials
from brightspace_scraper.utils.courses import getCourses, getCourseId
from brightspace_scraper.modules.assignments import getAssignments

load_dotenv()

BRIGHTSPACE_URL = os.environ.get("BRIGHTSPACE_URL")


async def main():
    async with async_playwright() as p:
        BROWSER = await p.chromium.launch(headless=False)
        CONTEXT = await BROWSER.new_context()
        PAGE = await CONTEXT.new_page()

        USER_USERNAME, USER_PASSWORD = getUserCredentials()['username'], getUserCredentials()['password']

        await login(PAGE, BRIGHTSPACE_URL, USER_USERNAME, USER_PASSWORD)

        COURSES: dict[str] = await getCourses(PAGE)
        COURSE_ID: list[str] = await getCourseId(COURSES)

        ASSIGNMENTS: list[str] = await getAssignments(PAGE, COURSE_ID)

        
if __name__ == "__main__":
    asyncio.run(main())
        















