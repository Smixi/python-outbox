from sqlalchemy.orm import registry

# equivalent to Base = declarative_base()

mapper_registry = registry()
Base = mapper_registry.generate_base()
