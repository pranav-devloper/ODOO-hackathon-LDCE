from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user_required
from app.schemas.budget import ExpenseCreate, ExpenseUpdate
from app.services import budget_service, trip_service
from app.database.models import User

router = APIRouter(prefix="/api", tags=["budget"])

@router.get("/trips/{trip_id}/budget")
def get_budget(trip_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        trip = trip_service.get_trip(db, trip_id)
        if not trip or trip.user_id != user.id:
            return {"success": False, "data": None, "error": {"code": "UNAUTHORIZED", "message": "Trip not found or unauthorized"}}
        summary = budget_service.get_budget_summary(db, trip_id)
        return {"success": True, "data": {"budget": summary}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "FETCH_BUDGET_FAILED", "message": str(e)}}

@router.post("/trips/{trip_id}/expenses")
def add_expense(trip_id: int, request: ExpenseCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        expense_data = request.model_dump(exclude_unset=True)
        expense = budget_service.add_expense(db, trip_id, user.id, expense_data)
        return {"success": True, "data": {
            "id": expense.id,
            "category": expense.category,
            "amount": expense.amount,
            "description": expense.description,
            "date": str(expense.date) if expense.date else None
        }, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "ADD_EXPENSE_FAILED", "message": str(e)}}

@router.patch("/expenses/{expense_id}")
def update_expense(expense_id: int, request: ExpenseUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        expense_data = request.model_dump(exclude_unset=True, exclude_none=True)
        expense = budget_service.update_expense(db, expense_id, user.id, expense_data)
        return {"success": True, "data": {
            "id": expense.id,
            "category": expense.category,
            "amount": expense.amount,
            "description": expense.description
        }, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "UPDATE_EXPENSE_FAILED", "message": str(e)}}

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        success = budget_service.delete_expense(db, expense_id, user.id)
        if not success:
            return {"success": False, "data": None, "error": {"code": "NOT_FOUND", "message": "Expense not found"}}
        return {"success": True, "data": None, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "DELETE_EXPENSE_FAILED", "message": str(e)}}
