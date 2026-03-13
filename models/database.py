"""
Database utility functions
Handles SQLite connection and common database operations
"""

import sqlite3
from flask import g
import os

DATABASE = 'placement_portal.db'

def dict_factory(cursor, row):
    """Convert sqlite3.Row to dictionary"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    """Get database connection for current request"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db

def get_cursor():
    """Get database cursor"""
    return get_db().cursor()

def init_db(app):
    """Initialize database connection - called by Flask app"""
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
    
    # Ensure database file exists
    if not os.path.exists(DATABASE):
        from database_sqlite import init_database
        init_database()
    
    return None  # For compatibility with MySQL version

def execute_query(query, params=None, commit=False, fetch_one=False, fetch_all=False):
    """
    Execute a database query
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        commit: Whether to commit the transaction
        fetch_one: Return single row
        fetch_all: Return all rows
    
    Returns:
        Query result or None
    """
    try:
        # Convert MySQL placeholders %s to SQLite placeholders ?
        if params and '%s' in query:
            query = query.replace('%s', '?')
        
        db = get_db()
        cursor = db.cursor()
        
        if params:
            if isinstance(params, dict):
                cursor.execute(query, params)
            else:
                cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if commit:
            db.commit()
            return cursor.lastrowid
        
        if fetch_one:
            result = cursor.fetchone()
            cursor.close()
            return result
        
        if fetch_all:
            result = cursor.fetchall()
            cursor.close()
            return result
        
        cursor.close()
        return None
        
    except Exception as e:
        if commit:
            get_db().rollback()
        print(f"Database error: {str(e)}")
        raise e

def close_db():
    """Close database connection"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
