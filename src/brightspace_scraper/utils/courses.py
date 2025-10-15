import asyncio

async def getCourses(PAGE):
    COURSE_CARDS_HTML: str = "d2l-my-courses-content >> d2l-card"
    await PAGE.wait_for_selector(COURSE_CARDS_HTML)
    COURSE_CARDS = PAGE.locator(COURSE_CARDS_HTML)
    COURSE_COUNT: int = await COURSE_CARDS.count()

    courses: dict[str] = []
    
    for i in range(COURSE_COUNT):
        card = COURSE_CARDS.nth(i)

        RAW_TITLE, RAW_COURSE_ID = await card.get_attribute("text"), await card.get_attribute("href")

        TITLE: str = RAW_TITLE.split(",")[0].strip()
        COURSE_ID: str = RAW_COURSE_ID.split("/")[-1]
        courses.append({"title": TITLE, "course_id": COURSE_ID})

    return courses

async def getCourseId(COURSES: list[str]):
    course_ids: list[str] = []
    for COURSE in COURSES:
        COURSE_ID: str = COURSE['course_id']

        course_ids.append(COURSE_ID)
    
    return course_ids
    




