class BlogDBRouter:
    app_names = ['myapp']
    models_to_route = ['Company', 'files']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.app_names and model.__name__ in self.models_to_route:
            return 'company_db'
        return None
    
    def db_for_write(self,model,**hints):
        if model._meta.app_label in self.app_names and model.__name__ in self.models_to_route:
            return 'company_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        db_set = {'default', 'company_db'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.app_names and model_name in [model.lower() for model in self.models_to_route]:
            return db == 'company_db'
        return db == 'default'