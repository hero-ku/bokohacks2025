XSS vulnerability in `news.js`, `renderNews` function concatenated unescaped strings into HTML that was dynamically added to the document.
Fixed by escaping HTML with the `escapeHtml` function.

SQL injection vulnerability in `notes.py`, `search_notes` route executed a raw SQL query after concatenating the user's search term into the string. It also didn't filter by user_id so upon hitting search the user could see everyone else's notes.
Fixed by switching to a SQLAlchemy ORM-style query and adding the user_id filter.

Access control vulnerability in `notes.py`, `delete_note` route only verified that user was logged in and that note existed before deleting it, allowing any logged in user to delete any user's note as long as they had the ID. Fixed by checking if the note's user id is the same as the deleter's.

Access control vulnerability in `notes.py`, `debug` route was usable by any user regardless of whether the Debug flag in app.py was set to true when running.
Fixed by early returning with a 403 Forbidden status if the Debug flag is not enabled. Responsibility of the one launching the app in production to make sure the Debug flag is off.

Authentication vulnerability in `register.py`, `register` route allowed user to sign up with insecure passwords that contained no special characters and enforced no minimum length.
Fixed by requiring the user to enter a password that is at least 8 characters long and contains one special character, uppercase letter, and digit.

Insecure design vulnerability in `retirement.py`, `contribute` route allowed user to schedule multiple contributions occur before the subsequent contributions finished, bypassing the fund validation, and allowing funds to go into the negatives.
Fixed by first transitioning retirement fund storage to the database and then adding check constraints.

Insecure design vulnerability in `captcha.py`, `captcha/generate` route doesn't return a randomly generated CAPTCHA, removing any challenge for botted registration.

Insecure design vulnerability in `files.py`, `upload` route didn't actually verify that the filetype was allowed.
Fixed with simple if clause.