from datetime import datetime

from sqlalchemy import inspect


def model_to_dict(obj):
    inspector = inspect(obj)
    result = {}
    
    for column in inspector.mapper.columns:
        value = getattr(obj, column.key)
        if isinstance(value, datetime):
            value = value.isoformat()
        result[column.key] = value
        
    return result
