from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import Trip, BudgetExpense
from datetime import date

def get_budget_summary(db: Session, trip_id: int) -> Dict[str, Any]:
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise ValueError("Trip not found")
        
    expenses = db.query(BudgetExpense).filter(BudgetExpense.trip_id == trip_id).all()
    
    total_spent = sum((e.amount or 0) for e in expenses)
    est_budget = trip.estimated_budget or 0.0
    remaining = est_budget - total_spent
    pct_used = (total_spent / est_budget * 100) if est_budget > 0 else 0.0
    
    status = "ON_TRACK"
    if pct_used > 100:
        status = "OVER_BUDGET"
    elif pct_used >= 80:
        status = "WARNING"
        
    days = 1
    if trip.start_date and trip.end_date:
        days = (trip.end_date - trip.start_date).days + 1
    days = max(1, days)
    avg_per_day = total_spent / days
    
    spending_by_day = {}
    for e in expenses:
        if e.date:
            d_str = e.date.isoformat()
            spending_by_day[d_str] = spending_by_day.get(d_str, 0) + (e.amount or 0)
            
    days_over_avg = sum(1 for amount in spending_by_day.values() if amount > avg_per_day)
    
    categories = {}
    for e in expenses:
        if e.category:
            categories[e.category] = categories.get(e.category, 0) + (e.amount or 0)
        
    return {
        "total_budget": float(est_budget),
        "total_spent": float(total_spent),
        "remaining": float(remaining),
        "percentage_used": round(pct_used, 2),
        "status": status,
        "average_per_day": round(avg_per_day, 2),
        "days_over_average": days_over_avg,
        "categories": [{"category": k, "amount": float(v)} for k, v in categories.items()]
    }

def add_expense(db: Session, trip_id: int, user_id: int, expense_data: Dict[str, Any]) -> BudgetExpense:
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if not trip:
        raise ValueError("Trip not found or unauthorized")
        
    expense = BudgetExpense(trip_id=trip_id, **expense_data)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def update_expense(db: Session, expense_id: int, user_id: int, expense_data: Dict[str, Any]) -> BudgetExpense:
    expense = db.query(BudgetExpense).join(Trip).filter(BudgetExpense.id == expense_id, Trip.user_id == user_id).first()
    if not expense:
        raise ValueError("Expense not found or unauthorized")
        
    for k, v in expense_data.items():
        if hasattr(expense, k):
            setattr(expense, k, v)
            
    db.commit()
    db.refresh(expense)
    return expense

def delete_expense(db: Session, expense_id: int, user_id: int) -> bool:
    expense = db.query(BudgetExpense).join(Trip).filter(BudgetExpense.id == expense_id, Trip.user_id == user_id).first()
    if not expense:
        return False
        
    db.delete(expense)
    db.commit()
    return True

def get_category_breakdown(db: Session, trip_id: int) -> List[Dict[str, Any]]:
    results = db.query(
        BudgetExpense.category, 
        func.sum(BudgetExpense.amount).label("total")
    ).filter(BudgetExpense.trip_id == trip_id).group_by(BudgetExpense.category).all()
    
    return [{"category": r.category, "amount": float(r.total)} for r in results if r.category]
