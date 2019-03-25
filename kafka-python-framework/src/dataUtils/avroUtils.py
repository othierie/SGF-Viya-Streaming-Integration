from uuid import uuid4
from confluent_kafka import avro

# Parse Schema used for serializing User class
record_schema = avro.loads("""
    {
        "namespace": "confluent.io.examples.serialization.avro",
        "name": "User",
        "type": "record",
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "favorite_number", "type": "int"},
            {"name": "favorite_color", "type": "string"}
        ]
    }
""")



deloitte_kafka_schema = avro.loads("""
{"namespace": "be.deloitte.kafka",
  "type": "record",
  "name": "Image",
  "fields": [
      {"name": "imageId" , "type": "string"},
      {"name": "timestamp", "type": { "type": "long", "logicalType": "timestamp-millis" }},
      {"name": "numOfBoats", "type": "int"},
      {"name": "occupancyRate", "type": "double"},
      {"name": "image", "type" : "string"}
  ]
 }
""")

sap_kafka_schema = avro.loads("""
{"namespace": "be.deloitte.kafka",
  "type": "record",
  "name": "Image",
  "fields": [
      {"name": "imageId" , "type": "string"},
      {"name": "timestamp", "type": { "type": "long", "logicalType": "timestamp-millis" }},
      {"name": "numOfBoats", "type": "int"},
      {"name": "occupancyRate", "type": "double"}
  ]
 }
""")

class User(object):
    """
        User stores the deserialized user Avro record.
    """

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["name", "favorite_number", "favorite_color", "id"]

    def __init__(self, name=None, favorite_number=None, favorite_color=None):
        self.name = name
        self.favorite_number = favorite_number
        self.favorite_color = favorite_color
        # Unique id used to track produce request success/failures.
        # Do *not* include in the serialized object.
        self.id = uuid4()

    def to_dict(self):
        """
            The Avro Python library does not support code generation.
            For this reason we must provide a dict representation of our class for serialization.
        """
        return {
            "name": self.name,
            "favorite_number": self.favorite_number,
            "favorite_color": self.favorite_color
        }

class ImageRecord(object):
    """
        User stores the deserialized user Avro record.
    """

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["imageId","timestamp", "numOfBoats","occupancyRate","image","id"]

    def __init__(self, imageId=None, timestamp=None, numOfBoats=None,occupancyRate=None,image=None):
        self.imageId = imageId
        self.timestamp = timestamp
        self.numOfBoats = numOfBoats
        self.occupancyRate = occupancyRate
        self.image = image
        # Unique id used to track produce request success/failures.
        # Do *not* include in the serialized object.
        self.id = uuid4()

    def to_dict(self):
        """
            The Avro Python library does not support code generation.
            For this reason we must provide a dict representation of our class for serialization.
        """
        return {
            "imageId": self.imageId,
            "timestamp": self.timestamp,
            "numOfBoats": self.numOfBoats,
            "occupancyRate": self.occupancyRate,
            "image": self.image
        }

class SapImageRecord(object):
    """
        User stores the deserialized user Avro record.
    """

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["imageId","timestamp", "numOfBoats","occupancyRate","id"]

    def __init__(self, imageId=None, timestamp=None, numOfBoats=None,occupancyRate=None):
        self.imageId = imageId
        self.timestamp = timestamp
        self.numOfBoats = numOfBoats
        self.occupancyRate = occupancyRate
        # Unique id used to track produce request success/failures.
        # Do *not* include in the serialized object.
        self.id = uuid4()

    def to_dict(self):
        """
            The Avro Python library does not support code generation.
            For this reason we must provide a dict representation of our class for serialization.
        """
        return {
            "imageId": self.imageId,
            "timestamp": self.timestamp,
            "numOfBoats": self.numOfBoats,
            "occupancyRate": self.occupancyRate,
        }