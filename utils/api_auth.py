# В фикстуре page:
page.goto("about:blank")
page.evaluate("() => { localStorage.setItem('token', arguments[0]) }", token)