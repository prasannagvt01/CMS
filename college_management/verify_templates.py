import os
import django
from django.template import loader, TemplateDoesNotExist
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_management.settings')
django.setup()

def verify_templates():
    template_dir = os.path.join(settings.BASE_DIR, 'templates', 'college')
    templates = [f for f in os.listdir(template_dir) if f.endswith('.html')]
    
    print(f"Verifying {len(templates)} templates...")
    errors = 0
    
    for template_name in templates:
        full_name = f'college/{template_name}'
        try:
            loader.get_template(full_name)
            print(f"PASS: {full_name}")
        except Exception as e:
            print(f"FAIL: {full_name} - {e}")
            errors += 1
            
    if errors == 0:
        print("\nAll templates passed verification!")
    else:
        print(f"\nVerification failed with {errors} errors.")

if __name__ == "__main__":
    verify_templates()
