from peewee import *
from abc import ABC, abstractmethod

db = SqliteDatabase(None)


class Observer(ABC):
    """Base Observer interface for the Observable pattern."""
    @abstractmethod
    def update(self, observable: 'Observable', event_type: str, **context) -> None:
        """Called when the observed object is changed."""
        pass


class Observable:
    observable_name = "observable"

    """Base Observable class for the Observable pattern."""
    def __init__(self):
        self._observers: list[Observer] = []

    def add_observer(self, observer: Observer) -> None:
        """Add an observer to the list."""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        """Remove an observer from the list."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event_type: str, **context) -> None:
        """Notify all observers about an event."""
        for observer in self._observers:
            observer.update(self, event_type, **context)


class DBOserver(Observer):
    def __init__(self):
        self._observers: list[Observable] = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def clean_observers(self):
        self._observers.clear()

    def update(self, observable: 'Observable', event_type: str, **context) -> None:
        for observer in self._observers:
            func_names = [f"db_{event_type}_{observable.observable_name}", f"db_{event_type}"]
            for func_name in func_names:
                if hasattr(observer, func_name):
                    getattr(observer, func_name)(observable)


db_observer = DBOserver()


class ObservableModel(Model, Observable):
    """A base model that implements the Observable pattern with Peewee ORM."""
    observable_name = "observable_model"
    
    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        Observable.__init__(self)
        self.add_observer(db_observer)
        
    def save(self, *args, **kwargs):
        """Override save to notify observers when a model is saved."""
        is_new = not bool(self._pk)
        result = super().save(*args, **kwargs)
        event_type = 'insert' if is_new else 'update'
        self.notify_observers(event_type)
        return result
        
    def delete_instance(self, *args, **kwargs):
        """Override delete_instance to notify observers when a model is deleted."""
        result = super().delete_instance(*args, **kwargs)
        self.notify_observers('delete')
        return result
        
    class Meta:
        database = db


class ProjectType(ObservableModel):
    observable_name = "project_type"
    name = CharField(unique=True)
    description = TextField()


class Project(ObservableModel):
    observable_name = "project"
    title = CharField()
    description = TextField()
    type = ForeignKeyField(ProjectType, backref='projects')


class SubProject(ObservableModel):
    observable_name = "sub_project"
    title = CharField()
    description = TextField()
    project = ForeignKeyField(Project, backref='sub_projects')
