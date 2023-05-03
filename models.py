"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

# TODO: Complete your models
class Organization(Base):
    __tablename__ = "organizations"
    #columns
    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    description = Column("description", TEXT, nullable=False)
    tags = relationship("Tags", secondary="organization_tag", back_populates="organizations")
    #Constructor
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Tags(Base):
    __tablename__ = "tags"
    #columns
    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    organizations = relationship("Organization", secondary="organization_tag", back_populates="tags")
    def __init__(self, name):
        self.name = name

class Org_Tags(Base):
    __tablename__ = "organization_tag"
    #columns
    organization_id = Column(INTEGER, ForeignKey("organizations.id"), primary_key = True)
    tag_id = Column(INTEGER, ForeignKey("tags.id"), primary_key = True)

class User(Base):
    __tablename__ = "users"
    id = Column("id", INTEGER, primary_key=True, autoincrement=True)
    username = Column("username", TEXT, nullable="False")
    password = Column("password", TEXT, nullable="False")

    def __init__(self, username, password):
        self.username = username
        self.password = password
    def __repr__(self):
        return("Account: " + self.username + " with password: " + self.password)