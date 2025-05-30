import requests
from fake_useragent import UserAgent

import time


class Capsolver:
    def __init__(self, api_key: str, proxy: str = None):
        self.api_key: str = api_key
        self.proxy: str | None = self._proxy_format(proxy) if proxy else None
        self.base_url: str = 'https://api.capsolver.com'
        self.user_agent: str = UserAgent().chrome
        
        
    def _proxy_format(self, proxy: str) -> str:
        if not proxy:
            return None
        if '@' in proxy:
            return proxy
        return proxy
        
       
    def create_turnstile_task(self, site_url: str, site_key: str,):
        
        """Create a task to get the TaskId"""
        
        data = {
            "clientKey": self.api_key,
            "task": {
                "type": "AntiTurnstileTaskProxyLess",
                "websiteURL": site_url,
                "websiteKey": site_key,
                "metadata": {
                    "action": ""
                }
            }
        }
        
        headers = {
            "Content-Type": "application/json",
        }
            
        try:
            
            response = requests.post(
                url=f"{self.base_url}/createTask",
                headers=headers,
                json=data
                ).json()
            
            task_id = response.get('taskId')
            return task_id
        
        except Exception:
            return None
        
        
    def get_result_task(self, task_id: str) -> str:
        
        """Get the captcha token"""
        
        if not task_id:
            return None
        
        data = {
            "clientKey": self.api_key,
            "taskId": task_id
        }
        
        headers = {
            "Content-Type": "application/json",
        }
        
        max_attempts = 30
        for _ in range(max_attempts):
            time.sleep(1)
            
            try:
                
                response = requests.post(
                    url=f"{self.base_url}/getTaskResult",
                    headers=headers,
                    json=data
                ).json()
                
                status = response.get('status')
                
                if status == 'ready':
                    return response.get('solution', {}).get('token')
                if status == 'failed' or response.get("errorId"):
                    return None
                
            except Exception:
                return None
         
        return None   
         
            
    def get_solve_turnstile(self, site_url: str, site_key: str,) -> str:
        
        """Captcha solving function"""
        
        task_id = self.create_turnstile_task(
            site_url=site_url, 
            site_key=site_key
            )
        
        if not task_id:
            print("Eror getting TaskId")
            return None
        
        return self.get_result_task(task_id=task_id)