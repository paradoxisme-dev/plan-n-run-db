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


class DBObserver(Observer):
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


db_observer = DBObserver()


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


class HistorisedContent(ObservableModel):
    observable_name = "historised_content"
    history = ForeignKeyField('self', backref='history')
    content = TextField()
    change_description = TextField(null=True)
    changed_at = DateTimeField()

    class Meta:
        indexes = (
            (('content', 'changed_at'), False),  # Index on content and changed_at
        )


class RessourceType(ObservableModel):
    observable_name = "ressource_type"
    name = CharField()
    description = ForeignKeyField(HistorisedContent, backref='ressource_types')


class Ressource(ObservableModel):
    observable_name = "ressource"
    name = CharField()
    type = ForeignKeyField(RessourceType, backref='ressources')
    description = ForeignKeyField(HistorisedContent, backref='ressources')


class RessourceNote(ObservableModel):
    observable_name = "ressource_note"
    ressource = ForeignKeyField(Ressource, backref='notes')
    content = ForeignKeyField(HistorisedContent, backref='ressource_notes')


class ProjectType(ObservableModel):
    observable_name = "project_type"
    name = CharField(unique=True)
    description = ForeignKeyField(HistorisedContent, backref='project_types')


class Project(ObservableModel):
    observable_name = "project"
    parent_project = ForeignKeyField('self', backref='sub_projects', null=True)
    title = CharField()
    description = ForeignKeyField(HistorisedContent, backref='projects')
    type = ForeignKeyField(ProjectType, backref='projects')
    ressources = ForeignKeyField(Ressource, backref='projects')


class Element(ObservableModel):
    observable_name = "element"
    parent_element = ForeignKeyField('self', backref='child_elements', null=True)
    order = IntegerField()
    name = CharField()
    description = ForeignKeyField(HistorisedContent, backref='elements')
    project = ForeignKeyField(Project, backref='elements')
    ressources = ForeignKeyField(Ressource, backref='elements')

    def change_order(self, new_order):
        """Change the order of the element within its sub_project and parent_element context."""
        if new_order is None or new_order == self.order:
            return
        old_order = self.order
        self.order = new_order
        self.save()
        if old_order < new_order:
            siblings = (
                Element.select()
                .where(
                    (Element.project == self.project) &
                    (Element.parent_element == self.parent_element) &
                    (Element.order > old_order) &
                    (Element.order <= new_order) &
                    (Element.id != self.id)
                )
            )
            for sibling in siblings:
                sibling.order -= 1
                sibling.save()
        else:
            siblings = (
                Element.select()
                .where(
                    (Element.project == self.project) &
                    (Element.parent_element == self.parent_element) &
                    (Element.order < old_order) &
                    (Element.order >= new_order) &
                    (Element.id != self.id)
                )
            )
            for sibling in siblings:
                sibling.order += 1
                sibling.save()

    def save(self, *args, **kwargs):
        """Override save to ensure the order is set correctly within the sub_project and parent_element context."""
        if self.order is None:
            max_order = (
                Element.select(fn.MAX(Element.order))
                .where(
                    (Element.project == self.project) &
                    (Element.parent_element == self.parent_element)
                )
                .scalar()
            )
            self.order = (max_order or 0) + 1
        return super().save(*args, **kwargs)

    def delete_instance(self, *args, **kwargs):
        """Override delete_instance to adjust the order of sibling elements when an element is deleted."""
        if self.order is not None:
            siblings = (
                Element.select()
                .where(
                    (Element.project == self.project) &
                    (Element.parent_element == self.parent_element) &
                    (Element.order > self.order)
                )
            )
            for sibling in siblings:
                sibling.order -= 1
                sibling.save()
        return super().delete_instance(*args, **kwargs)

    class Meta:
        indexes = (
            (('parent_element', 'project', 'order'), True),  # Unique index on parent_element, project, and order
        )


class Record(ObservableModel):
    observable_name = "record"
    file_path = CharField()


class ElementInRecord(ObservableModel):
    observable_name = "element_in_record"
    record = ForeignKeyField(Record, backref="elements")
    element = ForeignKeyField(Element, backref="record_elements")
    start_time =  IntegerField(null=True) # en secondes
    end_time = IntegerField(null=True)

    class Meta:
        indexes = (
            (('record', 'element'), True),  # Unique index on record and element
        )


class RecordingNote(ObservableModel):
    observable_name = "recording_note"
    element = ForeignKeyField(ElementInRecord, backref='notes')
    timestamp = IntegerField()  # en secondes
    content = TextField()
    ressources = ForeignKeyField(Ressource, backref='projects')


class UpdateOBSInputSetting(ObservableModel):
    observable_name = "update_obs_input_setting"
    element = ForeignKeyField(Element, backref='obs_input_settings')
    name = CharField()
    settings = TextField()


models = [
    HistorisedContent,
    RessourceType,
    Ressource,
    RessourceNote,
    ProjectType,
    Project,
    Element,
    Record,
    ElementInRecord,
    RecordingNote,
    UpdateOBSInputSetting,
]


def init_database(db_path: str):
    """Create the database and tables."""
    db.init(db_path)
    db.connect()
    db.create_tables(models)
