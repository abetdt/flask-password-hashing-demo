"""
Password management service
"""
from typing import Optional, Tuple, List, Dict, Any
from app.models.service import Service
from app.models.user import User
from app import db
import logging

logger = logging.getLogger(__name__)

class PasswordService:
    """Service for handling password management logic"""
    
    @staticmethod
    def add_service(user_id: int, service_data: Dict[str, Any], master_password: str) -> Tuple[bool, Optional[str]]:
        """
        Add new service with encrypted password
        
        Args:
            user_id (int): User ID
            service_data (dict): Service data
            master_password (str): Master password for encryption
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            # Create new service
            service = Service(
                user_id=user_id,
                service_name=service_data['service_name'],
                service_username=service_data['service_username'],
                service_url=service_data.get('service_url', ''),
                notes=service_data.get('notes', '')
            )
            
            # Encrypt password
            service.set_service_password(service_data['service_password'], master_password)
            
            # Save to database
            db.session.add(service)
            db.session.commit()
            
            logger.info(f"Service {service_data['service_name']} added successfully for user {user_id}")
            return True, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding service for user {user_id}: {e}")
            return False, "Có lỗi xảy ra khi thêm dịch vụ."

    @staticmethod
    def update_service(service_id: int, user_id: int, service_data: Dict[str, Any], master_password: str) -> Tuple[bool, Optional[str]]:
        """
        Update existing service
        
        Args:
            service_id (int): Service ID
            user_id (int): User ID
            service_data (dict): Updated service data
            master_password (str): Master password for encryption
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            service = Service.query.get(service_id)
            
            if not service or service.user_id != user_id:
                return False, "Dịch vụ không tồn tại hoặc bạn không có quyền chỉnh sửa."
            
            # Update service data
            service.service_name = service_data['service_name']
            service.service_username = service_data['service_username']
            service.service_url = service_data.get('service_url', '')
            service.notes = service_data.get('notes', '')
            
            # Update encrypted password if provided
            if 'service_password' in service_data:
                service.set_service_password(service_data['service_password'], master_password)
            
            db.session.commit()
            
            logger.info(f"Service {service_id} updated successfully")
            return True, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating service {service_id}: {e}")
            return False, "Có lỗi xảy ra khi cập nhật dịch vụ."

    @staticmethod
    def delete_service(service_id: int, user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Soft delete service (set is_active to False)
        
        Args:
            service_id (int): Service ID
            user_id (int): User ID
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            service = Service.query.get(service_id)
            
            if not service or service.user_id != user_id:
                return False, "Dịch vụ không tồn tại hoặc bạn không có quyền xóa."
            
            # Soft delete
            service.is_active = False
            db.session.commit()
            
            logger.info(f"Service {service_id} soft deleted successfully")
            return True, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting service {service_id}: {e}")
            return False, "Có lỗi xảy ra khi xóa dịch vụ."

    @staticmethod
    def get_service(service_id: int, user_id: int, include_password: bool = False, master_password: str = None) -> Optional[Service]:
        """
        Get service by ID
        
        Args:
            service_id (int): Service ID
            user_id (int): User ID
            include_password (bool): Include decrypted password
            master_password (str): Master password for decryption
            
        Returns:
            Service: Service object or None if not found
        """
        try:
            service = Service.query.get(service_id)
            
            if not service or service.user_id != user_id or not service.is_active:
                return None
                
            return service
            
        except Exception as e:
            logger.error(f"Error getting service {service_id}: {e}")
            return None

    @staticmethod
    def get_user_services(user_id: int, include_passwords: bool = False, master_password: str = None) -> List[Dict[str, Any]]:
        """
        Get all active services for user
        
        Args:
            user_id (int): User ID
            include_passwords (bool): Include decrypted passwords
            master_password (str): Master password for decryption
            
        Returns:
            list: List of service dictionaries
        """
        try:
            services = Service.query.filter_by(
                user_id=user_id,
                is_active=True
            ).all()
            
            service_list = []
            for service in services:
                service_dict = service.to_dict(
                    include_password=include_passwords,
                    master_password=master_password
                )
                service_list.append(service_dict)
                
            return service_list
            
        except Exception as e:
            logger.error(f"Error getting services for user {user_id}: {e}")
            return []

    @staticmethod
    def get_service_password(service_id: int, user_id: int, master_password: str) -> Optional[str]:
        """
        Get decrypted password for service
        
        Args:
            service_id (int): Service ID
            user_id (int): User ID
            master_password (str): Master password for decryption
            
        Returns:
            str: Decrypted password or None if error
        """
        try:
            service = Service.query.get(service_id)
            
            if not service or service.user_id != user_id or not service.is_active:
                return None
                
            return service.get_service_password(master_password)
            
        except Exception as e:
            logger.error(f"Error getting password for service {service_id}: {e}")
            return None 