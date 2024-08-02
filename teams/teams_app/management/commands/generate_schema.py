import os

from django.core.management.base import BaseCommand
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.renderers import OpenApiYamlRenderer


class Command(BaseCommand):
    help = "Generates OpenAPI schema in YAML format"

    def handle(self, *args, **kwargs):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=None, public=True)
        yaml_content = OpenApiYamlRenderer().render(
            schema, renderer_context={}
        )

        output_path = "openapi_schema.yaml"
        with open(output_path, "wb") as file:
            file.write(yaml_content)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated {output_path}")
        )
