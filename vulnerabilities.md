XSS vulnerability in `news.js`, `renderNews` function concatenated unescaped strings into HTML that was dynamically added to the document.
Fixed by escaping HTML with the `escapeHtml` function.

SQL injection vulnerability in `notes.py`, `search_notes` route executed a raw SQL query after concatenating the user's search term into the string. It also didn't filter by user_id so upon hitting search the user could see everyone else's notes.
Fixed by switching to a SQLAlchemy ORM-style query and adding the user_id filter.

Access control vulnerability in `notes.py`, `delete_note` route only verified that user was logged in and that note existed before deleting it, allowing any logged in user to delete any user's note as long as they had the ID. Fixed by checking if the note's user id is the same as the deleter's.