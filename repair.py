from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.apps import apps
import re

def sync_perms():
    for model in apps.get_models():
        content_type = ContentType.objects.filter(model=model.__name__.lower()).first()
        if content_type:
            word_formatted = " ".join(re.findall('[A-Z][^A-Z]*', model.__name__))
            for code in ['add', 'delete', 'view', 'change']:
                if not Permission.objects.filter(content_type=content_type, codename=f"{code}_{model.__name__.lower()}").exists():
                    Permission.objects.create(content_type_id=content_type.id,codename=f"{code}_{model.__name__.lower()}",name=f"Can {code.title()} {word_formatted}")