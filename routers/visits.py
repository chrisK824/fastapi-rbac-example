import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, paginate
from datetime import date
from typing import List

from src.authentication import PermissionChecker
from src.permissions.models_permissions import Visits
from src.database import get_db
from src.database_crud import visit_db_crud as db_crud
from src.schemas import VisitIn, Visit, VisitsAnalytics

router = APIRouter(prefix="/v1")


@router.post("/visits",
             dependencies=[Depends(PermissionChecker([Visits.permissions.CREATE]))],
             response_model=Visit, summary="Create a new visit", tags=["Visits"])
def create_visit(visit_in: VisitIn, db: Session = Depends(get_db)):
    """
    Creates a new visit.
    """
    try:
        visit_created = db_crud.create_visit(db, visit_in)
        return visit_created
    except ValueError as e:
        raise HTTPException(
            status_code=404, detail=f"{e}")
    except db_crud.DuplicateError as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.get("/visits",
            dependencies=[Depends(PermissionChecker([Visits.permissions.VIEW_LIST, Visits.permissions.VIEW_DETAILS]))],
            response_model=Page[Visit], summary="Get all visits", tags=["Visits"])
def get_visits(db: Session = Depends(get_db), operation_id: int = None, beneficiary_id: int = None,
               start_date: date = None, end_date: date = None):
    """
    Returns all visits.
    """
    try:
        visits = db_crud.get_visits(db, operation_id, beneficiary_id, start_date, end_date)
        return paginate(visits)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.delete("/visits/{visit_id}",
               dependencies=[Depends(PermissionChecker([Visits.permissions.DELETE]))],
               summary="Delete a visit", tags=["Visits"])
def delete_visit(visit_id: int, db: Session = Depends(get_db)):
    """
    Deletes a visit.
    """
    try:
        db_crud.delete_visit(db, visit_id)
        return {"result": f"Visit with ID {visit_id} has been deleted successfully!"}
    except ValueError as e:
        raise HTTPException(
            status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.get("/visits/analytics/count",
            dependencies=[Depends(PermissionChecker([Visits.permissions.VIEW_ANALYTICS]))],
            summary="Get count visits for a given timespan and/or operating spot",
            tags=["Visits analytics"])
def get_visits_count(start_date: date, end_date: date, db: Session = Depends(get_db), operating_spot_id: int = None):
    """
    Returns all visits.
    """
    try:
        visits = db_crud.get_visits_count(db, operating_spot_id, start_date, end_date)
        return {"result": visits}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.get("/visits/analytics/count_per_operating_spot",
            dependencies=[Depends(PermissionChecker([Visits.permissions.VIEW_ANALYTICS]))],
            response_model=List[VisitsAnalytics],
            summary="Get number of visits for a given timespan per operating spot", tags=["Visits analytics"])
def get_visits_count_per_operating_spot(start_date: date, end_date: date, db: Session = Depends(get_db)):
    """
    Returns number of visits for a given timespan per operating spot.
    """
    try:
        visits_per_operating_spots = db_crud.get_visits_count_per_operating_spot(db, start_date, end_date)
        return visits_per_operating_spots
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")
