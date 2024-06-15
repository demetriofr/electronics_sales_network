from os import getenv
from dotenv import load_dotenv
from django.core.management import BaseCommand

from users.models import User


load_dotenv()


class Command(BaseCommand):
    """Create a superuser."""

    def handle(self, *args, **options):
        """Function for creation superuser."""

        # Create the superuser
        csu = User.objects.create(
            email=getenv('CSU_USERNAME'),
            password=getenv('CSU_PASSWORD'),

            first_name=getenv('CSU_FIRST_NAME'),
            last_name=getenv('CSU_LAST_NAME'),

            is_staff=True,
            is_superuser=True,
        )

        # Setting the password for the superuser
        csu.set_password(getenv('CSU_PASSWORD'))

        csu.save()
