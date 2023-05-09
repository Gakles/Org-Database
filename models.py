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
    time_commitment = Column("time_commitment", TEXT, nullable=False)
    impact = Column("impact", TEXT, nullable=False)
    #Constructor
    def __init__(self, name, description, time_commitment, impact):
        self.name = name
        self.description = description
        self.time_commitment = time_commitment
        self.impact = impact
    def __repr__(self):
        return("Organization: " + self.name + " with time commitment: " + self.time_commitment + " and impact: " + self.impact)

class Tags(Base):
    __tablename__ = "tags"
    #columns
    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TEXT, nullable=False)
    organizations = relationship("Organization", secondary="organization_tag", back_populates="tags")
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return ("Tag: " + self.name)

class Org_Tags(Base):
    __tablename__ = "organization_tag"
    #columns
    organization_id = Column(INTEGER, ForeignKey("organizations.id"), primary_key = True)
    tag_id = Column(INTEGER, ForeignKey("tags.id"), primary_key = True)
    def __init__(self, org, tag):
        self.organization_id = org.id
        self.tag_id = tag.id

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