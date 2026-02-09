# app/services/exceptions.py
class ServiceException(Exception):
    """Exceção base para serviços"""
    pass

class NotFoundException(ServiceException):
    """Recurso não encontrado"""
    pass

class BusinessRuleException(ServiceException):
    """Violação de regra de negócio"""
    pass