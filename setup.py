from database import init_db, db_session
from models import *

init_db()

#Test Org
if db_session.query(Tags).first() is None:
    flavortext = "Founded in 1944, Boys & Girls Clubs of Silicon Valley (BGCSV) is a non-profit youth development organization that offers innovative and effective afterschool and summer enrichment programs primarily for low income, at-risk Santa Clara County youth ages 6-18 years. BGCSV serves approximately 5,000 regular members at 33 Clubhouses locations in San Jose, Morgan Hill, Gilroy and beyond. The majority of the youth we serve are living in economically depressed, high crime neighborhoods with an absence of positive adult role models or mentors. BGCSV takes a holistic approach to creating well-rounded, confident, and healthy youth and aims to provide programs and services that speak to all aspects of a child’s development. To achieve these goals, comprehensive curricula are provided within the following Core Enrichment Program Areas that address the academic, linguistic and cognitive growth, and emotional and social needs of youth. Core Program Areas are age and developmentally appropriate; are supportive of the diversity of children and families served, including culture and language; and are operationally efficient and effective."
    SVBGC = Organization("Silicon Valley Boy's and Girl's Club", flavortext, "0-1", "Medium")
    db_session.add(SVBGC)
    db_session.commit()
    org = db_session.query(Organization).first()

#TAGS
if db_session.query(Tags).first() is None:
    mental = Tags("mental-health")
    housing = Tags("housing")
    envir = Tags("environment")
    addreco = Tags("addiction-recovery")
    eldcare = Tags("elder-care")
    foodsec = Tags("food-security")
    lit = Tags("literacy")

    tags = [mental, housing, envir, addreco, eldcare, foodsec, lit]

    for tag in tags:
        db_session.add(tag)
    db_session.commit()

