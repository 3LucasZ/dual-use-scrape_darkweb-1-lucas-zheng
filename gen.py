from faker import Faker
fake = Faker()
with open('custom.html', 'w') as f:
    f.write('<!DOCTYPE html>\n<html>\n<body>\n')
    f.write('<h1>CONTACT INFORMATION!!!</h1>\n')
    f.write("<a href='github.com/jefffffy'>JEFFFY</a>")
    for i in range(100):
        username = fake.user_name()
        email = fake.email()
        phone_number = fake.phone_number()
        f.write(f'<p>{username} | {email} | {phone_number}</p>\n')
    f.write('</body>\n</html>\n')
