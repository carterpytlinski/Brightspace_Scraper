from brightspace_scraper.utils.url_builder import buildAssignmentDropboxUrl

# TODO: Refactor codebase to be more readable


# GETS ALL THE ASSIGNMENTS FOR EACH COURSE
async def courseLinks(COURSE_IDS: list[str]):
    return [buildAssignmentDropboxUrl(cid) for cid in COURSE_IDS]


# Scrape all assignments for each course
# TODO: fix assignments that are turned in but no grade to be turned in
async def getAssignments(page, course_ids: list[str]):
    results = {}

    for cid in course_ids:
        course_url = f"https://learn.truman.edu/d2l/lms/dropbox/user/folders_list.d2l?ou={cid}"
        print(f"\nNavigating to: {course_url}")
        await page.goto(course_url)

        try:
            await page.wait_for_selector("tbody tr", timeout=10000)
        except Exception:
            print(f"No assignments found for course {cid}")
            results[cid] = []
            continue

        rows = page.locator("tbody tr")
        count = await rows.count()
        print(f"Found {count} assignments in course {cid}")

        course_assignments = []

        for i in range(count):
            row = rows.nth(i)

            # --- TITLE ---
            title_locator = row.locator("a.d2l-link[href*='folder_submit_files']").first
            if not await title_locator.count():
                continue  # skip rows without a valid assignment title

            title = (await title_locator.text_content()).strip()

            # --- DUE DATE ---
            due_locator = row.locator(".d2l-folderdates-wrapper strong").filter(has_text="Due on")
            if await due_locator.count() > 0:
                raw_due = (await due_locator.first.text_content()).strip()
                due_date = raw_due.replace("Due on ", "").strip()
            else:
                due_date = None

            # --- TURNED IN STATUS ---
            status_locator = row.locator("td:last-child a.d2l-link")
            if await status_locator.count() > 0:
                status_text = (await status_locator.first.text_content()).strip()
                turned_in = status_text.lower() != "not submitted"
            else:
                turned_in = False

            # --- SCORE PERCENT ---
            score_percent = None
            if turned_in:
                percent_locator = row.locator(".d2l-grades-score label", has_text="%")
                if await percent_locator.count() > 0:
                    score_percent = (await percent_locator.first.text_content()).strip()

            course_assignments.append({
                "title": title,
                "due_date": due_date,
                "turned_in": turned_in,
                "score_percent": score_percent
            })

        results[cid] = course_assignments

    return results