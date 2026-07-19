class Task:
    def __init__(self,id,title,text,status,created_at,priority,everyday,deadline) -> None:
        self.id = id
        self.title = title
        self.text = text
        self.status = status
        self.created_at = created_at
        self.priority = priority
        self.everyday = everyday
        self.deadline = deadline

    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "text": self.text,
        "status": self.status,
        "created_at": self.created_at,
        "priority": self.priority,
        "everyday": self.everyday,
        "deadline": self.deadline
    }
    @classmethod
    def from_dict(cls,task):
        return cls(
            task["id"],
            task["title"],
            task["text"],
            task["status"],
            task["created_at"],
            task["priority"],
            task["everyday"],
            task["deadline"]
    )

class Note:
    def __init__(self,id,title,text,priority) -> None:
        self.id = id
        self.title = title
        self.text = text
        self.priority = priority

    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "text": self.text,
        "priority": self.priority,
    }
    @classmethod
    def from_dict(cls,task):
        return cls(
            task["id"],
            task["title"],
            task["text"],
            task["priority"]
    )
        
    