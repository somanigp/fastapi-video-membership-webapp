from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns  # For columns
import uuid
from app.config import get_settings
from . import validators, security


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
    password = columns.Text()  # NOTE password is not required because it does not have any constraints (i.e., no primary_key=True, no required=True, and no default value). In Cassandra, non-primary key columns are optional unless explicitly marked as required. 
    # NOTE If password is not provided while creating a User object, it will be stored as NULL in Cassandra.

    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):  # representation : The __repr__ method is a special method (dunder method) in Python that returns a string representation of an object. print(repr(p))  # Calls __repr__()
        return f"User(email={self.email}, user_id={self.user_id})"
    
    def verify_password(self, pwd):  # Input is raw password which user gives.
        pwd_hash = self.password  # We are string password in objects in hashed form.
        verified, _ = security.verify_hash(pwd_hash, pwd)  # _ is used we are not using a variable.
        return verified
    
    def set_password(self, pwd, commit=False):  # if boolean, true not passed then commit will be False. And data not saved in db.
        pwd_hash = security.generate_hash(pwd)
        self.password = pwd_hash  # This is a class method. In the static method (nothing to do with objects and can be called directly using class name ) below we create a User object and call set password on that to put pwd in password attribute of that object.
        if commit:
            self.save()  # Same as obj.save(), here self is obj created in static method. Thus saving that object in db.
        return True
    
    @staticmethod
    def create_user(email, password=None):
        qs = User.objects.filter(email=email)  # Filter down based on primary keys, there can be only filter applied in Cassander.
        # print(qs) # SELECT "user_id", "password" FROM video_membership_app.user WHERE "email" = %(0)s LIMIT 10000
        if qs.count() != 0:  # Type of qs is <class 'cassandra.cqlengine.query.ModelQuerySet'>
            raise Exception("User already has a account.")
        
        valid, msg, email = validators.check_email_validity(email)
        if not valid:
            raise Exception(f"Invalid email : {msg}")
        
        obj = User(email=email)  # Create an User object/Instance.
        obj.set_password(password) # in set_password func commit will go as false, thus object won't be saved in db in that function, but will happen below. 
        obj.save()  # Saves an object to the database. This is where it adds object to database.
        return obj

# Security concern
# 1. password cant be raw text.
# 2. If user created through User.objects.create(email="", password=""), we can create 2 users with same email. 
