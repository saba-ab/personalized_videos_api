from accounts.models import User
from accounts.factories import UserFactory
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Deletes all users and then creates 10 new users"

    def handle(self, *args, **options) -> str | None:

        User.objects.all().delete()

        UserFactory.create_batch(10)

        User.objects.create_superuser(
            username="admin",
            email="admin@admin.com",
            password="admin",
            first_name="Admin",
            last_name="Adminadze",
            bio="udzlieresi admini",
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded data"))
