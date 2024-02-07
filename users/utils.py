import uuid
import random
import string



def generate_code():
    return str(uuid.uuid4()).replace('-', '').upper()[:10]


def random_email():
    random_email = ''.join(random.choices(string.ascii_letters,  k = 10)) + '@gmail.com'
    return random_email