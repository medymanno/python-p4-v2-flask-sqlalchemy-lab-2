from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


# -------------------------------
# Customer
# -------------------------------
class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)   # <-- allow NULL (tests expect this)

    # Relationships
    reviews = relationship("Review", back_populates="customer", cascade="all, delete-orphan")

    # Association Proxy
    items = association_proxy("reviews", "item")

    # Serialization Rules
    serialize_rules = ("-reviews.customer",)

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"


# -------------------------------
# Item
# -------------------------------
class Item(db.Model, SerializerMixin):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)   # <-- allow NULL
    price = db.Column(db.Float, nullable=True)   # <-- allow NULL

    # Relationships
    reviews = relationship("Review", back_populates="item", cascade="all, delete-orphan")

    # Serialization Rules
    serialize_rules = ("-reviews.item",)

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, {self.price}>"


# -------------------------------
# Review
# -------------------------------
class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=True)  # <-- allow NULL too

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    # Relationships
    customer = relationship("Customer", back_populates="reviews")
    item = relationship("Item", back_populates="reviews")

    # Serialization Rules
    serialize_rules = ("-customer.reviews", "-item.reviews")

    def __repr__(self):
        return f"<Review {self.id}, Cust:{self.customer_id}, Item:{self.item_id}>"
