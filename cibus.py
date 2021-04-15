import subprocess


def run(command):
    return subprocess.check_output(command, shell=True)



def get_balance(username, password):
    run(f"curl 'https://www.mysodexo.co.il/' -H 'Connection: keep-alive' -H 'Origin: https://www.mysodexo.co.il'  -H 'Content-Type: application/x-www-form-urlencoded'   -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'   -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'   -H 'Referer: https://www.mysodexo.co.il/'   --data-raw '__VIEWSTATE=S7Vca9h0ihqiy4m0asl2ybYgednoCBRZ9t%2Br%2B4Fjm6fePg%2B8BdflxxYWKMLkgZDBM7U6HVq5hwV3NcGHFHEJmdqsslRS8%2FezSInY7pBkOw0JsVgyNU8z5MweyY3Ip7549HoRXfP9OOMwVT3KaO7tAimfsdd2z%2FXlJ%2Fi3Z2kYlJ00xrWeOebc40Z4aLFYhwFZPROR%2FFY%2FEhOlHcu9wKGn1clIc5v3UHhbwDZSQdBWe%2F15giWp5R%2B530U8IBSar9VJyEYvf4dXhfmgkb8%2Bsml5U1n0yEONmgbz6YyNpT930WqnFBrNpe%2FxvwcD3Bo%2BTC9SbCeXzijvcqVFjTt%2B4F%2FbDveDmvtWmq4JnxMkcfqFzH0QSxGVJcnfPnN7bVX4MSMmnXOOSw%3D%3D&__VIEWSTATEGENERATOR=E12A6B22&txtUsr={username}&txtPas={password}&ctl12=&txtPhone=&g-recaptcha-response=&ctl19='   --compressed   --cookie-jar /tmp/cookie")
    state = run("curl 'https://www.mysodexo.co.il/new_ajax_service.aspx?getBdgt=1'  --cookie /tmp/cookie")
    run('rm /tmp/cookie')


    return state.decode('utf8')