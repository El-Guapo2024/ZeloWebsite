from flask_caching import Cache 

class CacheManager:
    def __init__(self, cache_instance):
        self.cache = cache_instance 

    def set_active_searching(self,state: bool):
        """Set the active_searching flag in the cache."""
        self.cache.set('active_searching', state)

    def get_active_searching(self):
        """Get the active_searching flag from the cache."""
        return self.cache.get('active_searching')
    
    def set_selected_bikes(self, bikes: list):
        """Set the selected_bikes list in the cache."""
        self.cache.set('selected_bikes', bikes)

    def get_selected_bikes(self):
        """Get the selected_bikes from the cache."""
        return self.cache.get('selected_bikes')
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear 