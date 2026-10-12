from datetime import date
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db, limiter
from ..models import Task
from ..utils.validators import validate_task_data
from ..utils.responses import success_response, error_response

def current_user_id():
    return int(get_jwt_identity())

class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = current_user_id()
        page = max(request.args.get("page", 1, type=int), 1)
        per_page = min(max(request.args.get("per_page", 10, type=int), 1), 50)

        query = Task.query.filter_by(user_id=user_id)
        status = request.args.get("status")
        priority = request.args.get("priority")
        category = request.args.get("category")
        sort_by = request.args.get("sort_by", "created_at")
        sort_order = request.args.get("sort_order", "desc")

        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if category:
            query = query.filter_by(category=category)

        allowed_sort = {
            "created_at": Task.created_at,
            "updated_at": Task.updated_at,
            "due_date": Task.due_date,
            "priority": Task.priority,
            "title": Task.title
        }
        column = allowed_sort.get(sort_by, Task.created_at)
        query = query.order_by(column.asc() if sort_order == "asc" else column.desc())

        paginated = db.paginate(query.statement, page=page, per_page=per_page, error_out=False)

        return success_response({
            "tasks": [task.to_dict() for task in paginated.items],
            "pagination": {
                "page": paginated.page,
                "per_page": paginated.per_page,
                "total_pages": paginated.pages,
                "total_items": paginated.total,
                "has_next": paginated.has_next,
                "has_prev": paginated.has_prev
            }
        })

    @jwt_required()
    @limiter.limit("30 per minute")
    def post(self):
        data = request.get_json(silent=True) or {}
        errors = validate_task_data(data)
        if errors:
            return error_response("Validation failed", 400, errors)

        due_date = date.fromisoformat(data["due_date"]) if data.get("due_date") else None
        task = Task(
            title=data["title"].strip(),
            description=data.get("description", ""),
            status=data.get("status", "pending"),
            priority=data.get("priority", "medium"),
            category=data.get("category", "general"),
            due_date=due_date,
            user_id=current_user_id()
        )
        db.session.add(task)
        db.session.commit()
        return success_response({
            "message": "Task created successfully",
            "task": task.to_dict()
        }, status_code=201)

class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id):
        task = Task.query.filter_by(id=task_id, user_id=current_user_id()).first()
        if not task:
            return error_response("Task not found", 404)
        return success_response({"task": task.to_dict()})

    @jwt_required()
    def put(self, task_id):
        task = Task.query.filter_by(id=task_id, user_id=current_user_id()).first()
        if not task:
            return error_response("Task not found", 404)

        data = request.get_json(silent=True) or {}
        errors = validate_task_data(data, update=True)
        if errors:
            return error_response("Validation failed", 400, errors)

        for field in ("title", "description", "status", "priority", "category"):
            if field in data:
                setattr(task, field, data[field].strip() if isinstance(data[field], str) else data[field])
        if "due_date" in data:
            task.due_date = date.fromisoformat(data["due_date"]) if data["due_date"] else None

        db.session.commit()
        return success_response({
            "message": "Task updated successfully",
            "task": task.to_dict()
        })

    @jwt_required()
    def patch(self, task_id):
        return self.put(task_id)

    @jwt_required()
    def delete(self, task_id):
        task = Task.query.filter_by(id=task_id, user_id=current_user_id()).first()
        if not task:
            return error_response("Task not found", 404)
        db.session.delete(task)
        db.session.commit()
        return success_response(message="Task deleted successfully")

class TaskSearchResource(Resource):
    @jwt_required()
    def get(self):
        q = request.args.get("q", "").strip()
        if not q:
            return error_response("Search query 'q' is required", 400)
        pattern = f"%{q}%"
        tasks = Task.query.filter(
            Task.user_id == current_user_id(),
            db.or_(Task.title.ilike(pattern), Task.description.ilike(pattern), Task.category.ilike(pattern))
        ).all()
        return success_response({"tasks": [t.to_dict() for t in tasks]})

task_ns = {
    "list": TaskListResource,
    "single": TaskResource,
    "search": TaskSearchResource
}
