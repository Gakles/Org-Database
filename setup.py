from database import init_db, db_session
from models import *

init_db()

# TAGS
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

# Test Org
if db_session.query(Organization).first() is None:
    flavortext = "Founded in 1944, Boys & Girls Clubs of Silicon Valley (BGCSV) is a non-profit youth development organization that offers innovative and effective afterschool and summer enrichment programs primarily for low income, at-risk Santa Clara County youth ages 6-18 years. BGCSV serves approximately 5,000 regular members at 33 Clubhouses locations in San Jose, Morgan Hill, Gilroy and beyond. The majority of the youth we serve are living in economically depressed, high crime neighborhoods with an absence of positive adult role models or mentors. BGCSV takes a holistic approach to creating well-rounded, confident, and healthy youth and aims to provide programs and services that speak to all aspects of a child’s development. To achieve these goals, comprehensive curricula are provided within the following Core Enrichment Program Areas that address the academic, linguistic and cognitive growth, and emotional and social needs of youth. Core Program Areas are age and developmentally appropriate; are supportive of the diversity of children and families served, including culture and language; and are operationally efficient and effective."
    SVBGC = Organization(
        "Silicon Valley Boy's and Girl's Club", flavortext, "0-1", "Monthly","Whole Bay","https://www.bgclub.org"
    )
    db_session.add(SVBGC)
    db_session.commit()
    
    org = db_session.query(Organization).first()
    PawPatrol = Organization(
        "East Bay Paw Patrol",
        "The East Bay chapter of Paw Patrol, an organization dedicated to animal assistance.",
        "1-2",
        "Weekly",
        "East Bay",
        "https://cnn.com" 
    )
    db_session.add(PawPatrol)
    db_session.commit()
    
    fitkids = Organization("Fit Kids Foundation", "Dedicated to providing physical education to underserved communities", "2+", "Weekly", "Menlo Park", "https://fitkids.org")
    db_session.add(fitkids)
    db_session.commit()
