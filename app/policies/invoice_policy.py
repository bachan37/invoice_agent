from app.constants import INVOICE_STATUS
from app.repository.sql_repository.user_repository import UserRepository
from app.repository.sql_repository.invoice_repository import InvoiceRepository
from app.models import User
from app.policies.base_policy import BasePolicy
from app.policies.core.types import Action, ResourceContext
from typing import List

class InvoicePolicy(BasePolicy):
    def can_perform(self, action: Action) -> bool:
        if(action == Action.READ):
            return self.__can_read()
        elif(action == Action.CREATE):
            return self.__can_create()
        elif(action == Action.DELETE):
            return self.__can_delete()
        elif(action == Action.UPDATE):
            return self.__can_update()
        elif(action == Action.REVIEW):
            return self.__can_review()
        else:
            return False
    
    def __can_read(self) -> bool:
        """admin and reviewer can read it. 
        Others can read if invoice is not in PENDING_REVIEW state"""

        if bool(set(["admin", "reviewer"]) & set(self.role_names)):
            return True

        return self.resource_context.attributes['status'] != INVOICE_STATUS.PENDING_REVIEW

    
    def __can_create(self) -> bool:
        return True
    
    def __can_delete(self) -> bool:
        return True
    
    def __can_review(self) -> bool:
        """only reviewer can review(approve/reject) it"""
        return "reviewer" in self.role_names 
        