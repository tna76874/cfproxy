#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
db class for logging
"""
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text, func, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import hashlib

Base = declarative_base()

class Redirect(Base):
    __tablename__ = 'redirect'
    id = Column(Integer, primary_key=True, autoincrement=True)
    to = Column(String)
    source = Column(String)  # Neuer Eintrag für die Source-Spalte
    date = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///data.db', echo=False)
        
        Base.metadata.create_all(self.engine)

    def add_event(self, to, source):
        hashed_source = self.hash_string(source)
        with self.get_session() as session:
            new_redirect = Redirect(to=to, source=hashed_source, date=datetime.now())
            session.add(new_redirect)
            session.commit()
            
    def hash_string(self, input_string):
        return hashlib.sha256(input_string.encode()).hexdigest()

    def get_redirect_statistics(self):
        with self.get_session() as session:
            total_entries = session.query(func.count(Redirect.id)).scalar()
            unique_sources = session.query(func.count(func.distinct(Redirect.source))).scalar()
            
            # Zeitraum für die Statistik (z.B., letzten 7 Tage)
            time_span_start = datetime.now() - timedelta(days=7)
            redirects_last_week = session.query(func.count(Redirect.id)).filter(Redirect.date >= time_span_start).scalar()

            print(f"Total Redirect Entries: {total_entries}")
            print(f"Unique Sources: {unique_sources}")
            print(f"Redirects in the Last 7 Days: {redirects_last_week}")

            # Anzahl der Redirects pro Tag in den letzten 7 Tagen
            redirects_per_day = (
                session.query(func.strftime('%Y-%m-%d', Redirect.date), func.count(Redirect.id))
                .filter(Redirect.date >= time_span_start)
                .group_by(func.strftime('%Y-%m-%d', Redirect.date))
                .all()
            )

            print("\nRedirects Per Day (Last 7 Days):")
            for entry in redirects_per_day:
                print(f"{entry[0]}: {entry[1]} redirects")

    @contextmanager
    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            yield session
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()
        finally:
            session.close()
            

if __name__ == "__main__":
    # Beispiel für die Nutzung der DatabaseManager-Klasse
    db_manager = DatabaseManager()
    
    db_manager.get_redirect_statistics()
    
    # Eintrag in die Tabelle hinzufügen
    db_manager.add_event(source='https://example1.com', to='https://example2.com')

    # Beispiel: Einträge aus der Tabelle abfragen
    with db_manager.get_session() as session:
        redirects = session.query(Redirect).all()
        for redirect in redirects:
            print(f'from: {redirect.source}, To: {redirect.to}, Date: {redirect.date}')