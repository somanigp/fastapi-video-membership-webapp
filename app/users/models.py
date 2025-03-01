from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns  # For columns
import uuid
from app.config import get_settings


# NOTE UUID (Universally Unique Identifier) is a 128-bit identifier that is guaranteed to be unique across space and time. It is often used to uniquely identify objects in a distributed system. It consists of 32 hexadecimal characters, divided into five groups: 8-4-4-4-12.
# 1. Guaranteed Uniqueness Across Systems : Unlike auto-incremented integer IDs, which may collide in distributed databases, UUIDs are unique by design.
# 2. Scalability in Distributed Databases : UUIDs allow multiple servers to generate unique IDs independently, so no bottleneck
# 3. No Need for Centralized ID Generation : In traditional databases, a single point of ID generation (like a primary key sequence) can create a bottleneck. UUIDs don't require a central authority, so any server can generate them independently.
# 4. Useful for Cross-System Integrations

# NOTE A UUID consists of 128 bits (16 bytes), typically written as 32 hexadecimal characters. This results in a total of 2¹²⁸ possible UUIDs. This is an astronomically large number, making collisions virtually impossible. There are 2 types : UUID v1 (Timestamp-based), UUID v4 (Random-based), etc.
# Cassandra DB is hosted on multiple servers, all writing together. Thus uuid helps so data generate at same time doesn't have same user_id


settings = get_settings()  # Cached instance will be called

class User(Model):
    __keyspace__ = settings.astradb_keyspace  # Attaching the table to a keyspace
    # NOTE First primary declared will be used for indexing.
    email = columns.Text(primary_key=True) # Text, as want table to be indexed.
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)  # UUID1 -> UUID1 comes with a timestamp. Ideal way to store IDs. primary_key is true to enable additional filtering capabilities on this model.
    # default used so it is created each time. Here uuid.uuid1() is an executable, so a new uuid created through this function which columns.UUID() calls. So a new uuid value is generated and goes as default each time. default=new_value.
    password = columns.Text()
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):  # representation : The __repr__ method is a special method (dunder method) in Python that returns a string representation of an object. print(repr(p))  # Calls __repr__()
        return f"User(email={self.email}, user_id={self.user_id})"


# Security concern
# 1. password cant be raw text.
# 2. If user created through User.objects.create(email="", password=""), we can create 2 users with same email. 
