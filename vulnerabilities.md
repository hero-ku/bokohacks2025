XSS vulnerability in `news.js`, `renderNews` function concatenated unescaped strings into HTML that was dynamically added to the document.
Fixed by escaping HTML with the `escapeHtml` function.